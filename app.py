import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64

st.title("GIF Generator 🌀")
st.write("Upload images, add text, choose color & size, and create a GIF!")

uploaded_files = st.file_uploader(
    "Upload PNG or JPG images",
    accept_multiple_files=True,
    type=["png", "jpg", "jpeg"]
)

duration = st.slider("Frame duration (ms)", 100, 1000, 300)

# NEW UI CONTROLS
text_overlay = st.text_input("Add text to GIF (optional):")
font_color = st.color_picker("Choose text color", "#FFFFFF")
font_size_user = st.slider("Text size (px)", 20, 200, 60)

if st.button("Create GIF"):
    if uploaded_files:
        frames = []

        # Base size from first image
        first_img = Image.open(uploaded_files[0]).convert("RGB")
        base_width, base_height = first_img.size

        def resize_keep_ratio(img, target_w, target_h):
            img_ratio = img.width / img.height
            target_ratio = target_w / target_h

            if img_ratio > target_ratio:
                new_w = target_w
                new_h = int(target_w / img_ratio)
            else:
                new_h = target_h
                new_w = int(target_h * img_ratio)

            return img.resize((new_w, new_h))

        for file in uploaded_files:
            img = Image.open(file).convert("RGB")

            # Resize image to first image size
            img = resize_keep_ratio(img, base_width, base_height)

            # Add black canvas to center image
            canvas = Image.new("RGB", (base_width, base_height), "black")
            x = (base_width - img.width) // 2
            y = (base_height - img.height) // 2
            canvas.paste(img, (x, y))
            img = canvas

            if text_overlay:
                draw = ImageDraw.Draw(img)

                # Try to load a bigger font
                try:
                    font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size_user)
                except:
                    font = ImageFont.load_default()

                text = text_overlay

                # Get text size using textbbox
                bbox = draw.textbbox((0, 0), text, font=font)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]

                # Bottom center position
                tx = (base_width - text_w) / 2
                ty = base_height - text_h - 40

                # Black stroke (adapt to font size)
                stroke = max(2, font_size_user // 15)

                for dx in range(-stroke, stroke + 1):
                    for dy in range(-stroke, stroke + 1):

