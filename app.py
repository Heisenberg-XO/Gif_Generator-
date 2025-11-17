import streamlit as st
from PIL import Image
import io

st.title("GIF Generator 🌀")
st.write("Upload images and I will convert them into a GIF for you!")

uploaded_files = st.file_uploader(
    "Upload PNG or JPG images",
    accept_multiple_files=True,
    type=["png", "jpg", "jpeg"]
)

duration = st.slider("Frame duration (ms)", 100, 1000, 300)

if st.button("Create GIF"):
    if uploaded_files:
        frames = []

        for file in uploaded_files:
            img = Image.open(file).convert("RGB")
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
        st.image(gif_bytes, caption="Generated GIF")

        st.download_button(
            label="Download GIF",
            data=gif_bytes,
            file_name="mygif.gif",
            mime="image/gif"
        )
    else:
        st.error("Please upload at least one image.")
