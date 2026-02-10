import streamlit as st
import cv2
import requests
from PIL import Image
import numpy as np
import io

st.title("Webcam DIAL Inference App")

# Capture webcam frame
img_file = st.camera_input("Take a snapshot!")

if img_file:
    # Show the image
    img = Image.open(img_file)
    st.image(img, caption="Your frame", use_column_width=True)

    # Prepare image bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)

    # Send to local DIAL inference server
    with st.spinner("Running inference..."):
        files = {'image': ('snapshot.jpg', img_bytes, 'image/jpeg')}
        response = requests.post("http://localhost:5000/predict", files=files)   # Change port if needed
        if response.ok:
            result = response.json()
            st.success("Insight returned:")
            st.json(result)
        else:
            st.error("DIAL inference error.")