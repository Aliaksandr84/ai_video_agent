import streamlit as st
import requests
from PIL import Image
import io

st.title("Webcam DIAL Inference App + Agent")

img_file = st.camera_input("Take a snapshot!")

# --- Existing code for webcam and inference ---
insight = None
if img_file:
    img = Image.open(img_file)
    st.image(img, caption="Your frame", use_column_width=True)

    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)

    with st.spinner("Running inference..."):
        files = {'image': ('snapshot.jpg', img_bytes, 'image/jpeg')}
        try:
            response = requests.post("http://localhost:5000/predict", files=files)
            if response.ok:
                insight = response.json()
                st.success("Insight returned:")
                st.json(insight)
            else:
                st.error("DIAL inference error.")
        except Exception as e:
            st.error(f"Error communicating with server: {e}")

# --- Simple Agent/Helper Chat Box ---
st.markdown("---")
st.header("Ask the Analysis Agent 🧑‍💻")

if 'agent_chat' not in st.session_state:
    st.session_state.agent_chat = []

user_input = st.text_input("Type your analysis question, suggestion, or prompt here:")

if st.button("Send") and user_input:
    # Simple agent logic: respond based on input or latest insight
    if 'insight' in locals() and insight:
        answer = f"I see you've just taken a snapshot. Here's the latest insight: {insight}"
    elif "how to" in user_input.lower():
        answer = "You can capture a webcam image, and I'll analyze it for you! Try describing what you want to analyze."
    else:
        answer = "I'm here to help! Take a snapshot and I'll give you an AI-powered insight."
    st.session_state.agent_chat.append({"user": user_input, "agent": answer})

for chat in st.session_state.agent_chat:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**Agent:** {chat['agent']}")