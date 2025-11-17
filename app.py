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
            
            # Add text overlay if user typed anything
            if text_overlay:
                draw = ImageDraw.Draw(img)
                font = ImageFont.load_default()
                
                text = text_overlay
                text_width, text_height = draw.textsize(text, font=font)
                x = (img.width - text_width) / 2
                y = img.height - text_height - 10  

                draw.text((x, y), text, font=font, fill="white")

            frames.append(img)

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

        # 🔥 Animated GIF Preview (base64)
        gif_data = gif_bytes.getvalue()
        gif_base64 = base64.b64encode(gif_data).decode("utf-8")

        st.markdown("### 🔥 GIF Preview (Animated)")
        st.markdown(
            f"""
            <div style="display:flex; justify-content:center;">
                <img src="data:image/gif;base64,{gif_base64}" style="max-width:90%; border-radius:10px;" />
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

