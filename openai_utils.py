import openai
import base64
import requests
import os

def image_url_to_base64(img_url):
    # Download image from URL, return as base64
    resp = requests.get(img_url)
    resp.raise_for_status()
    img_bytes = resp.content
    return base64.b64encode(img_bytes).decode("utf-8")

def visual_llm_extract(image_url, prompt, openai_api_key):
    # Use GPT-4 Vision through OpenAI API
    img_b64 = image_url_to_base64(image_url)
    openai.api_key = openai_api_key
    result = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": f"data:image/png;base64,{img_b64}"}
                ]
            }
        ],
        max_tokens=1024,
    )
    # OpenAI returns result in slightly varying structures
    return result.choices[0].message.content

def visual_llm_extract_with_llava(image_url, prompt, llava_api_url="http://localhost:8000"):
    data = {
        "image_url": image_url,
        "prompt": prompt
    }
    response = requests.post(f"{llava_api_url}/v1/vision", json=data)
    response.raise_for_status()
    return response.json()["output"]