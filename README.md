⚙️ How to Use
1. Install dependencies
pip install opencv-python numpy torch torchvision
pip install git+https://github.com/facebookresearch/segment-anything.git
2. Download model
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth
3. Run the CLI
python autocrop.py input.png --checkpoint sam_vit_b_01ec64.pth
🔧 Advanced usage
python autocrop.py image.jpg \
  --checkpoint sam_vit_b_01ec64.pth \
  --output results \
  --model-type vit_b \
  --min-size 60 \
  --device cpu
🔥 Optional upgrades (I can add for you)
--grid-mode → perfect for icon sheets (like your image)
--merge → combine small segments into one object
--format jpg/png/webp
--preview → show bounding boxes before saving
--batch folder/ → process multiple images