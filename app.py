import streamlit as st
import numpy as np
import cv2
from PIL import Image
import tempfile

st.title("Portrait Colorizer")
st.write("Upload a black and white portrait to colorize it using AI!")

uploaded_file = st.file_uploader("Choose a black & white portrait", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file).convert("RGB")
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Convert PIL Image to OpenCV
    img_np = np.array(img)
    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    # Placeholder for colorization
    st.write("Colorizing... (placeholder, model integration needed)")
    colorized = img_cv  # TODO: Replace with actual colorization

    colorized_rgb = cv2.cvtColor(colorized, cv2.COLOR_BGR2RGB)
    st.image(colorized_rgb, caption="Colorized Image", use_column_width=True)

    # Download button
    result = Image.fromarray(colorized_rgb)
    tmp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    result.save(tmp_file.name)
    with open(tmp_file.name, "rb") as file:
        btn = st.download_button(
            label="Download Colorized Image",
            data=file,
            file_name="colorized.png",
            mime="image/png"
        )
