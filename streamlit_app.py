import streamlit as st
from figma_utils import list_top_frames, get_frame_image_url
from openai_utils import visual_llm_extract

st.set_page_config(page_title="Figma ➜ Code Requirements Generator", layout='wide')

st.title("Figma to Code/Requirements Generator (with Visual LLM)")

st.sidebar.header("Figma Setup")
figma_token = st.sidebar.text_input("Figma API Token", type="password")
file_key = st.sidebar.text_input("Figma File Key (from file URL)")
go_list = st.sidebar.button("List Frames")

if 'frames' not in st.session_state:
    st.session_state['frames'] = []
if 'frame_images' not in st.session_state:
    st.session_state['frame_images'] = {}

if go_list and figma_token and file_key:
    with st.spinner("Fetching Figma frames..."):
        try:
            frames = list_top_frames(figma_token, file_key)
            st.session_state.frames = frames
            st.success(f"Found {len(frames)} frames")
        except Exception as e:
            st.error(f"Could not fetch frames: {e}")
else:
    frames = st.session_state.get('frames', [])

if frames:
    selected = st.selectbox(
        "Select frame to analyze", options=frames, format_func=lambda f: f"{f['page']} / {f['name']}"
    )
    if selected:
        frame_id = selected['id']
        if frame_id not in st.session_state['frame_images']:
            with st.spinner("Getting frame image..."):
                img_url = get_frame_image_url(figma_token, file_key, frame_id)
                st.session_state['frame_images'][frame_id] = img_url
        img_url = st.session_state['frame_images'][frame_id]
        st.image(img_url, caption=f"Frame: {selected['name']} ({selected['page']})", use_column_width=True)

        # --- OpenAI Visual LLM integration ---
        st.markdown("## Visual LLM Code/Requirement Extraction")
        openai_key = st.text_input("OpenAI API Key", type="password", key="oai")
        task = st.selectbox("Extraction task", [
            "Generate requirements / user stories",
            "Generate Streamlit UI code (Python)",
            "Generate React component code"
        ])
        prompt = ""
        if task == "Generate requirements / user stories":
            prompt = "Please describe the requirements and main UI functionalities shown in this design image, suitable for agile development."
        elif task == "Generate Streamlit UI code (Python)":
            prompt = "Please generate Streamlit (Python) code that implements the visual layout in this image. Include basic interactivity if present."
        else:
            prompt = "Please generate a React component (JSX) implementing this layout with placeholder data and UI elements as appropriate."

        if st.button("Send image to Visual LLM") and openai_key:
            with st.spinner("Querying Visual LLM (GPT-4V)..."):
                try:
                    result = visual_llm_extract(img_url, prompt, openai_key)
                    st.subheader("LLM Output:")
                    st.code(result if "code" in task.lower() else "", language="python" if "Streamlit" in task else "jsx" if "React" in task else "")
                    if not ("code" in task.lower()):
                        st.markdown(result)
                except Exception as e:
                    st.error(f"LLM extraction failed: {e}")
        st.info("Output can be adjusted or pasted directly into your codebase.")

    # --- Optionally: Show all frames as gallery ---
    with st.expander("Show all frames as gallery"):
        for f in frames:
            st.write(f"{f['page']} / {f['name']}")
else:
    st.markdown("➡️ Enter your Figma API token and File Key, then click **List Frames**.")

st.sidebar.markdown("---")
st.sidebar.markdown("Get Figma tokens at https://www.figma.com/developers/api")
st.sidebar.markdown("Get file key from the file URL: https://www.figma.com/file/**FILE_KEY**/...")