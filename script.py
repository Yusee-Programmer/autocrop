import argparse
import os
import cv2
import numpy as np
import torch

from segment_anything import sam_model_registry, SamAutomaticMaskGenerator


# ----------------------------
# Utilities
# ----------------------------
def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def save_crop(img, box, output_path, fmt):
    x, y, w, h = box
    crop = img[y:y+h, x:x+w]
    cv2.imwrite(f"{output_path}.{fmt}", crop)


def show_preview(img, boxes):
    preview = img.copy()
    for (x, y, w, h) in boxes:
        cv2.rectangle(preview, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Preview - Press any key", preview)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ----------------------------
# Merge overlapping boxes
# ----------------------------
def merge_boxes(boxes, iou_threshold=0.3):
    def iou(box1, box2):
        x1, y1, w1, h1 = box1
        x2, y2, w2, h2 = box2

        xa = max(x1, x2)
        ya = max(y1, y2)
        xb = min(x1+w1, x2+w2)
        yb = min(y1+h1, y2+h2)

        inter = max(0, xb-xa) * max(0, yb-ya)
        union = w1*h1 + w2*h2 - inter
        return inter / union if union > 0 else 0

    merged = []
    for box in boxes:
        added = False
        for i, m in enumerate(merged):
            if iou(box, m) > iou_threshold:
                x = min(box[0], m[0])
                y = min(box[1], m[1])
                w = max(box[0]+box[2], m[0]+m[2]) - x
                h = max(box[1]+box[3], m[1]+m[3]) - y
                merged[i] = (x, y, w, h)
                added = True
                break
        if not added:
            merged.append(box)
    return merged


# ----------------------------
# GRID MODE (icon sheets)
# ----------------------------
def grid_crop(image, rows, cols):
    h, w, _ = image.shape
    cell_h = h // rows
    cell_w = w // cols

    boxes = []
    for r in range(rows):
        for c in range(cols):
            x = c * cell_w
            y = r * cell_h
            boxes.append((x, y, cell_w, cell_h))
    return boxes


# ----------------------------
# SAM MODE (universal)
# ----------------------------
def sam_boxes(image, sam, min_size):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    mask_generator = SamAutomaticMaskGenerator(sam)
    masks = mask_generator.generate(image_rgb)

    boxes = []
    for m in masks:
        seg = m["segmentation"]
        ys, xs = np.where(seg)

        if len(xs) == 0 or len(ys) == 0:
            continue

        x1, x2 = xs.min(), xs.max()
        y1, y2 = ys.min(), ys.max()

        w, h = x2 - x1, y2 - y1

        if w >= min_size and h >= min_size:
            boxes.append((x1, y1, w, h))

    return boxes


# ----------------------------
# Process single image
# ----------------------------
def process_image(path, args, sam=None):
    image = cv2.imread(path)
    if image is None:
        print(f"❌ Failed: {path}")
        return

    name = os.path.splitext(os.path.basename(path))[0]
    out_dir = os.path.join(args.output, name)
    ensure_dir(out_dir)

    # Choose mode
    if args.grid_mode:
        boxes = grid_crop(image, args.rows, args.cols)
    else:
        boxes = sam_boxes(image, sam, args.min_size)

    if args.merge:
        boxes = merge_boxes(boxes)

    if args.preview:
        show_preview(image, boxes)

    # Save
    for i, box in enumerate(boxes):
        save_crop(image, box, os.path.join(out_dir, f"{i}"), args.format)

    print(f"✅ {len(boxes)} objects saved from {name}")


# ----------------------------
# Main CLI
# ----------------------------
def main():
    parser = argparse.ArgumentParser("🔥 Advanced AutoCrop CLI")

    parser.add_argument("input", help="Image or folder path")
    parser.add_argument("-o", "--output", default="outputs")

    parser.add_argument("--batch", action="store_true",
                        help="Process folder of images")

    parser.add_argument("--grid-mode", action="store_true")
    parser.add_argument("--rows", type=int, default=4)
    parser.add_argument("--cols", type=int, default=5)

    parser.add_argument("--merge", action="store_true")
    parser.add_argument("--preview", action="store_true")

    parser.add_argument("--format", default="png",
                        choices=["png", "jpg", "webp"])

    parser.add_argument("--min-size", type=int, default=40)

    parser.add_argument("--checkpoint", help="SAM model path")
    parser.add_argument("--model-type", default="vit_b")

    args = parser.parse_args()

    # Load SAM only if needed
    sam = None
    if not args.grid_mode:
        if not args.checkpoint:
            raise ValueError("❌ SAM mode requires --checkpoint")

        print("🧠 Loading SAM...")
        sam = sam_model_registry[args.model_type](checkpoint=args.checkpoint)
        sam.to("cuda" if torch.cuda.is_available() else "cpu")

    # Batch or single
    if args.batch:
        for file in os.listdir(args.input):
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                process_image(os.path.join(args.input, file), args, sam)
    else:
        process_image(args.input, args, sam)


if __name__ == "__main__":
    main()