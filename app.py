import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip
import io
import base64
import tempfile

st.title("Ultimate GIF Studio 🌀")
st.write("Upload IMAGES or a VIDEO → Add text → Choose colors → Generate GIF!")

# -----------------------------
# USER INPUTS
# -----------------------------
mode = st.selectbox("Choose Input Type:", ["Images", "Video"])

duration = st.slider("Frame duration (ms)", 100, 1000, 300)
text_overlay = st.text_input("Add text to GIF (optional):")
font_color = st.color_picker("Choose text color", "#FFFFFF")
font_size_user = st.slider("Text size (px)", 20, 200, 60)

# -----------------------------
# HELPER FUNCTION: Resize while keeping aspect ratio
# -----------------------------
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

# -----------------------------
# PROCESS IMAGES
# -----------------------------
if mode == "Images":
    uploaded_files = st.file_uploader(
        "Upload PNG/JPG images",
        accept_multiple_files=True,
        type=["png", "jpg", "jpeg"]
    )

    if st.button("Create GIF"):
        if uploaded_files and len(uploaded_files) > 0:

            frames = []
            first_img = Image.open(uploaded_files[0]).convert("RGB")
            base_width, base_height = first_img.size

            for file in uploaded_files:
                img = Image.open(file).convert("RGB")
                img = resize_keep_ratio(img, base_width, base_height)

                # Add black canvas
                canvas = Image.new("RGB", (base_width, base_height), "black")
                x = (base_width - img.width) // 2
                y = (base_height - img.height) // 2
                canvas.paste(img, (x, y))
                img = canvas

                # Add text
                if text_overlay:
                    draw = ImageDraw.Draw(img)

                    try:
                        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size_user)
                    except:
                        font = ImageFont.load_default()

                    bbox = draw.textbbox((0, 0), text_overlay, font=font)
                    text_w = bbox[2] - bbox[0]
                    text_h = bbox[3] - bbox[1]
                    tx = (base_width - text_w) / 2
                    ty = base_height - text_h - 40

                    stroke = max(2, font_size_user // 15)
                    for dx in range(-stroke, stroke + 1):
                        for dy in range(-stroke, stroke + 1):
                            draw.text((tx + dx, ty + dy), text_overlay, font=font, fill="black")

                    draw.text((tx, ty), text_overlay, font=font, fill=font_color)

                frames.append(img)

            # Save GIF
            gif_bytes = io.BytesIO()
            frames[0].save(
                gif_bytes,
                format="GIF",
                append_images=frames[1:],
                save_all=True,
                duration=duration,
                loop=0,
            )
            gif_bytes.seek(0)

            st.success("GIF created successfully! 🎉")

            # Preview GIF
            gif_b64 = base64.b64encode(gif_bytes.getvalue()).decode("utf-8")
            st.markdown(f"<img src='data:image/gif;base64,{gif_b64}' width='80%'/>",
                        unsafe_allow_html=True)

            st.download_button(
                label="Download GIF",
                data=gif_bytes,
                file_name="mygif.gif",
                mime="image/gif"
            )

        else:
            st.error("Please upload at least one image.")


# -----------------------------
# PROCESS VIDEO
# -----------------------------
else:
    uploaded_video = st.file_uploader("Upload MP4/MOV video", type=["mp4", "mov"])

    if st.button("Create GIF"):
        if uploaded_video:

            # Save uploaded video temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp:
                temp.write(uploaded_video.read())
                video_path = temp.name

            clip = VideoFileClip(video_path)

            frames = []
            base_width, base_height = clip.size

            for frame in clip.iter_frames():
                img = Image.fromarray(frame).convert("RGB")

                # Add text
                if text_overlay:
                    draw = ImageDraw.Draw(img)

                    try:
                        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size_user)
                    except:
                        font = ImageFont.load_default()

                    bbox = draw.textbbox((0, 0), text_overlay, font=font)
                    text_w = bbox[2] - bbox[0]
                    text_h = bbox[3] - bbox[1]
                    tx = (base_width - text_w) / 2
                    ty = base_height - text_h - 40

                    stroke = max(2, font_size_user // 15)
                    for dx in range(-stroke, stroke + 1):
                        for dy in range(-stroke, stroke + 1):
                            draw.text((tx + dx, ty + dy), text_overlay, font=font, fill="black")

                    draw.text((tx, ty), text_overlay, font=font, fill=font_color)

                frames.append(img)

            # Save GIF
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

            st.success("GIF created from video successfully! 🎬")

            gif_b64 = base64.b64encode(gif_bytes.getvalue()).decode("utf-8")
            st.markdown(f"<img src='data:image/gif;base64,{gif_b64}' width='80%'/>",
                        unsafe_allow_html=True)

            st.download_button(
                label="Download GIF",
                data=gif_bytes,
                file_name="video_to_gif.gif",
                mime="image/gif"
            )

        else:
            st.error("Please upload a video file.")


