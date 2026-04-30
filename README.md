# 🔥 AutoCrop Pro

**AutoCrop Pro** is a powerful CLI tool for automatically extracting objects or assets from images.

It supports both:
- 🧠 **AI-powered detection (SAM – Segment Anything Model)**
- 🧩 **Grid-based cropping (perfect for icon sheets & UI assets)**

Designed for developers, designers, and dataset builders.

---

## ✨ Features

- ✅ Universal object detection using AI (SAM)
- ✅ Grid-based slicing for structured layouts (icons, UI kits)
- ✅ Batch processing (process entire folders)
- ✅ Merge overlapping detections
- ✅ Export in multiple formats (`png`, `jpg`, `webp`)
- ✅ Preview detections before saving

---

## 📦 Installation

To install AutoCrop Pro, run the following command:

```bash
pip install autocrop-pro
```

## 🚀 Usage

To use AutoCrop Pro, simply run:

```bash
autocrop --input <input_directory> --output <output_directory>
```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
- ✅ Fast and flexible CLI interface

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/autocrop-pro.git
cd autocrop-pro
```

### 2. Install dependencies
```bash
pip install opencv-python numpy torch torchvision
pip install git+https://github.com/facebookresearch/segment-anything.git
```

### 3. Download AI Model (SAM)
```bash
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth
```

## 🚀 Usage

### Basic (AI mode)
```bash
python autocrop_pro.py image.png --checkpoint sam_vit_b_01ec64.pth
```

### Grid Mode (Perfect for Icon Sheets)
```bash
python autocrop_pro.py icons.png --grid-mode --rows 4 --cols 5
```

### Preview Before Saving
```bash
python autocrop_pro.py image.png \
  --checkpoint sam_vit_b_01ec64.pth \
  --preview
```

### Batch Processing
```bash
python autocrop_pro.py images/ \
  --batch \
  --checkpoint sam_vit_b_01ec64.pth
```

### Export Format (JPG / WEBP)
```bash
python autocrop_pro.py image.png \
  --checkpoint sam_vit_b_01ec64.pth \
  --format webp
```

### Merge Overlapping Objects
```bash
python autocrop_pro.py image.png \
  --checkpoint sam_vit_b_01ec64.pth \
  --merge
```

## ⚙️ CLI Options

Option | Description
--- | ---
`input` | Input image or folder
`--output` | Output directory (default: outputs/)
`--batch` | Process a folder of images
`--grid-mode` | Enable grid slicing
`--rows` | Number of grid rows
`--cols` | Number of grid columns
`--merge` | Merge overlapping boxes
`--preview` | Show detection preview
`--format` | Output format (`png`, `jpg`, `webp`)
`--min-size` | Minimum object size
`--checkpoint` | Path to SAM model
`--model-type` | SAM model (`vit_b`, `vit_l`, `vit_h`)

## 📁 Output Structure

```text
outputs/
 ├── image1/
 │    ├── 0.png
 │    ├── 1.png
 │    └── ...
 ├── image2/
 │    └── ...
```

🧠 How It Works
AI Mode (Default)

Uses Meta's Segment Anything Model (SAM) to:

Detect objects automatically
Generate segmentation masks
Convert them into bounding boxes
Crop and export each object
Grid Mode

Splits image into equal rows & columns:

Ideal for icon packs
Perfect precision when layout is structured
⚠️ Limitations
AI mode may:
Split one object into multiple parts
Detect too many small regions
Grid mode requires correct row/column input
Large models may require GPU for best performance
💡 Use Cases
🎨 Extract UI assets & icons
📦 Generate datasets for AI training
🌐 Prepare images for web apps
🧪 Research & computer vision experiments
🔥 Roadmap
 GUI (desktop app)
 Web interface (upload & crop)
 Auto grid detection
 YOLO integration (object-specific detection)
 pip package (pip install autocrop-pro)
🤝 Contributing

Pull requests are welcome!

If you’d like to improve performance, add features, or fix bugs:

Fork the repo
Create a new branch
Submit a PR
📜 License

MIT License

👤 Author

Built by Yusee Habibu
Founder of Python Niger 🇳🇪 | Python Hausa | Haske Framework

⭐ Support

If you find this useful:

Star the repo ⭐
Share with others 🚀