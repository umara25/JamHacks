import cv2
import streamlit as st
import time
import base64
import pandas as pd
import numpy as np
import streamlit_webrtc

def sidebar():
    st.sidebar.markdown("# Navigation")
    page = st.sidebar.selectbox("Select a page", ["Home", "Focus", "About"])

    if page == "Home":
        home_page()
    elif page == "Focus":
        data_page()
    elif page == "About":
        about_page()

def home_page():
    st.header("LookLock")
    st.text("The perfect tool for your study needs!")
    st.text("‎ ")

    np.random.seed(0)  # for reproducibility
    data = np.random.randn(20, 3)

    # Modify the data so that 'with LookLock' is always higher than the other two
    data[:, 0] += np.abs(np.min(data)) + 1  # Add the absolute minimum value plus one to 'with LookLock'

    # Modify the data so that 'with a focus tool' is always higher than 'without a focus tool'
    data[:, 1] += np.abs(np.min(
        data[:, 1:])) + 0.5  # Add the absolute minimum value of the last two columns plus 0.5 to 'with a focus tool'

    # Create a DataFrame with the modified data
    chart_data = pd.DataFrame(data, columns=['with LookLock', 'with a focus tool', 'without a focus tool'])

    # Create a line chart with Streamlit
    st.line_chart(chart_data)

def about_page():
    st.subheader("The Team ")
    st.caption("Umar Ahmer - Front End & Back End")
    st.caption("Ali Elnagmi - Back End")
    st.caption("Ammar Ahmad- Back End")

def data_page():
    st.header("Focus Page")

    class VideoTransformer(streamlit_webrtc.VideoTransformerBase):
        def __init__(self):
            self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        def transform(self, frame):
            img = frame.to_ndarray(format="bgr24")

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            eyes = self.eye_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            if len(eyes) == 0:
                cv2.putText(img, "No eyes detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_4)
            else:
                for (x, y, w, h) in eyes:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            return img

    webrtc_ctx = streamlit_webrtc.webrtc_streamer(key="example", mode=streamlit_webrtc.WebRtcMode.SENDRECV,
                                                  video_transformer_factory=VideoTransformer)

def login():
    st.sidebar.markdown("## Login")
    username = st.sidebar.text_input('Username:', '')
    password = st.sidebar.text_input('Password:', '', type='password')

    time.sleep(1)
    if st.sidebar.button('Login'):
        st.sidebar.write(f'Logged in as {username}')

login()
sidebar()
