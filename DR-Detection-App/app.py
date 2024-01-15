#import libraries
from pathlib import Path
from PIL import Image
import streamlit as st
import base64

import config
from utils import load_model, infer_uploaded_image, infer_uploaded_video, infer_uploaded_webcam

# setting page layout
st.set_page_config(
    page_title="Diabetic Retinopathy Detection",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
    )

# main page heading
st.title("Diabetes Retinopathy Detection")
st.write("Welcome to the Diabetes Retinopathy Detection App!")
st.write("To get started, use the sidebar to configure the application settings and upload patient's retina scan to receive your results.")
# sidebar
st.sidebar.header("Application Configurations")


# model options
task_type = st.sidebar.selectbox(
    "Select Task",
    ["Detection"]
)

model_type = None
if task_type == "Detection":
    model_type = st.sidebar.selectbox(
        "Default Model",
        config.DETECTION_MODEL_LIST
    )
else:
    st.error("There is only one default model")

confidence = float(st.sidebar.slider(
    "Select Model Confidence", 30, 100, 50)) / 100

model_path = ""
if model_type:
    model_path = Path(config.DETECTION_MODEL_DIR, str(model_type))
else:
    st.error("Default model")

# load model
try:
    model = load_model(model_path)
except Exception as e:
    st.error(f"Unable to load model. Please check the specified path: {model_path}")

# image/video options
st.sidebar.header("Image Configurations")
source_selectbox = st.sidebar.selectbox(
    "Select Source",
    config.SOURCES_LIST
)

source_img = None
if source_selectbox == config.SOURCES_LIST[0]: # Image
    infer_uploaded_image(confidence, model)
elif source_selectbox == config.SOURCES_LIST[1]: # Webcam
    infer_uploaded_webcam(confidence, model)
else:
    st.error("Currently only 'Image' and 'Webcam' source are implemented")