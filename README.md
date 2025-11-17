## GIF Creator Script (Python)
This script converts all PNG/JPG images in the folder into a GIF.  
Download the script below and run it in the same folder as your images.

### Website
click on the link https://m6ulaxvw5hwcohz6ybgbsu.streamlit.app/

### 📥 Download Script
Click the link below to download the Python file:

➡️ **[Download gif_creator.py](gif_creation.py)**

---

### 🧪 How to Use

1. Put `gif_creator.py` in a folder containing your images.
2. Make sure images are named in a sortable order (ex: 1.png, 2.png, 3.png…)
3. Run the script:

```bash
python gif_creator.py
from PIL import Image
import os

frames = []

# Collect all PNG or JPG files in sorted order
for file in sorted(os.listdir()):
    if file.lower().endswith((".png", ".jpg", ".jpeg")):
        img = Image.open(file).convert("RGB")  # Convert to RGB to remove alpha issues
        frames.append(img)

if frames:
    frames[0].save(
        "mygif.gif",
        format="GIF",
        append_images=frames[1:],
        save_all=True,
        duration=300,  # milliseconds per frame
        loop=0
    )
    print("✅ GIF created successfully as mygif.gif!")
else:
    print("⚠️ No PNG or JPG images found in this folder.")
