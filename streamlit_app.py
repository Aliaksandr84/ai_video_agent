import streamlit as st
import requests
from PIL import Image
import io

st.title("Webcam DIAL Inference App + Agent & Enrichment")

# ---- Webcam and DIAL Inference ----

img_file = st.camera_input("Take a snapshot!")

insight = None

if img_file:
    img = Image.open(img_file)
    st.image(img, caption="Your frame", use_column_width=True)

    # Convert image to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)

    with st.spinner("Running inference..."):
        files = {'image': ('snapshot.jpg', img_bytes, 'image/jpeg')}
        try:
            response = requests.post("http://localhost:5000/predict", files=files)
            if response.ok:
                insight = response.json()
                st.success("AI Insight returned:")
                st.json(insight)
            else:
                st.error("DIAL inference error.")
        except Exception as e:
            st.error(f"Error communicating with inference server: {e}")

# ---- Enrichment via Wikipedia API ----

def enrich_object_info(object_name):
    """
    Queries Wikipedia API for an object and returns the summary.
    """
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{object_name}"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        title = data.get('title', object_name)
        desc = data.get('extract', 'No info found.')
        page_url = data.get('content_urls', {}).get('desktop', {}).get('page', '')
        return f"**{title}**\n\n{desc}\n\n[Read more]({page_url})"
    return f"No information available for {object_name}."


if insight and "objects" in insight:
    st.header("Detected Objects and Enrichment")
    for obj in insight["objects"]:
        st.subheader(obj)
        with st.spinner(f"Looking up {obj}..."):
            enrich_info = enrich_object_info(obj)
            st.markdown(enrich_info)
elif insight:
    st.info("No objects found in this frame for enrichment.")

# ---- Simple Chat Agent ----

st.markdown("---")
st.header("Ask the Analysis Agent 🧑‍💻")

if 'agent_chat' not in st.session_state:
    st.session_state.agent_chat = []

user_input = st.text_input("Type your analysis question, suggestion, or prompt here:")

if st.button("Send") and user_input:
    # Simple agent logic with context
    if insight and "objects" in insight and len(insight["objects"]) > 0:
        detected_list = ", ".join(insight["objects"])
        answer = (
            f"In your latest snapshot, the detected objects are: {detected_list}.\n\n"
            f"Use the enrichment section to learn more about them."
        )
    elif "how to" in user_input.lower():
        answer = (
            "You can capture a webcam image above. "
            "After capturing, an AI summary and object enrichment will appear. "
            "Try asking about specific objects in your scene!"
        )
    else:
        answer = (
            "I'm here to help with AI-based analysis. "
            "Take a snapshot and I'll give you insights!"
        )
    st.session_state.agent_chat.append({"user": user_input, "agent": answer})

for chat in st.session_state.agent_chat:
    st.markdown(f"**You:** {chat['user']}")
    st.markdown(f"**Agent:** {chat['agent']}")