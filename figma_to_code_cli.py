# figma_to_code_cli.py
from figma_utils import get_frame_image_url
from openai_utils import visual_llm_extract

figma_token = input("Figma API Token: ")
file_key = input("Figma File Key: ")
frame_id = input("Frame ID: ")
img_url = get_frame_image_url(figma_token, file_key, frame_id)

prompt = "Please generate Streamlit Python code for the UI shown in this image."
openai_key = input("OpenAI API Key: ")
out = visual_llm_extract(img_url, prompt, openai_key)
print(out)