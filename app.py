import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import base64

st.title("GIF Generator 🌀")
st.write("Upload images, add optional text, and convert them into a GIF!")

uploaded_files = st.file_uploader(
    "Upload PNG or JPG images",
    accept_multiple_files=True,
    type=["png", "jpg", "jpeg"]
)

duration = st.slider("Frame duration (ms)", 100, 1000, 300)

text_overlay = st.text_input("Add text to GIF (optional):")

if st.button("Create GIF"):
    if uploaded_files:
        frames = []

        for file in uploaded_files:
            img = Image.open(file).convert("RGB")
            draw = ImageDraw.Draw(img)

            if text_overlay:
                # Adaptive font size: 5% of image width
                font_size = int(img.width * 0.05)

                # Try using a truetype font
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)

                text = text_overlay

                # Correct text size calc
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                # Center bottom
                x = (img.width - text_width) / 2
                y = img.height - text_height - (font_size // 2)

                # Stroke for visibility
                stroke = max(3, font_size // 20)

                for dx in range(-stroke, stroke+1):
                    for dy in range(-stroke, stroke+1):
                        draw.text((x+dx, y+dy), text, font=font, fill="black")

                draw.text((x, y), text, font=font, fill="white")

            frames.append(img)

        # Create GIF
        gif_bytes = io.BytesIO()
        frames[0].save(
            gif_bytes,
            format="GIF",
            append_images=frames[1:],
            save_all=True,
            duration=duration,
            loop=0
        )
        gif_bytes.seek(0)

        st.success("GIF created successfully!")

        # Base64 Animated Preview
        gif_data = gif_bytes.getvalue()
        gif_base64 = base64.b64encode(gif_data).decode("utf-8")

        st.markdown("### 🔥 GIF Preview")
        st.markdown(
            f"""
            <div style="display:flex;justify-content:center;">
                <img src="data:image/gif;base64,{gif_base64}" 
                style="max-width:90%;border-radius:10px;"/>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.download_button(
            label="Download GIF",
            data=gif_bytes,
            file_name="mygif.gif",
            mime="image/gif"
        )

    else:
        st.error("Please upload at least one image.")
