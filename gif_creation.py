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
