 # modules/image_generator.py

import json
import os
from openai import OpenAI
import requests
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import os
from huggingface_hub import login
from modules import blog_generator
from modules.scraper import scrape_all_sources
from modules.utils import log
import streamlit as st

# hf_token = config.get("huggingface", {}).get("token")

# Set your OpenAI API key
openai_api_key = st.secrets["openai"]["api_key"]

image_key = st.secrets["image"]["key"]
if not openai_api_key:
    raise ValueError("OpenAI API key not found in config.")
client = OpenAI(api_key=openai_api_key)
# if hf_token:
#     login(hf_token)
#     log("Logged into Hugging Face successfully.")
# else:
#     log("Hugging Face token not found in config.")

# Load Stable Diffusion (run once at module level for efficiency)
# pipe = StableDiffusionPipeline.from_pretrained(
#     "sd-legacy/stable-diffusion-v1-5",
#     torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
#     height=256,  # Lower resolution for faster generation
#     width=256
# )
# pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

def generate_image(prompt, images_count):
    try:
        url = "https://modelslab.com/api/v6/realtime/text2img"

        payload = json.dumps({
            "key" : image_key,
            "prompt": prompt,
            "negative_prompt": "bad quality",
            "width": "512",
            "height": "512",
            "safety_checker": False,
            "seed": None,
            "samples": images_count,
            "base64":False,
            "webhook": None,
            "track_id": None
        })

        headers = {
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()
    except Exception as e:
        print(f"Error generating image: {e}")
        return None
    
import requests
import os

def generate_image_from_topic(topic, image_focus=None, images_count=1):
    prompt = image_focus or f"a general visual representation of {topic}"
    log(f"Combined prompt: {prompt}")

    # Generate all images at once
    image_response = generate_image(prompt, images_count)
    if not image_response:
        log("Failed to generate images.")
        return None

    image_urls = image_response.get("output", [])
    if not image_urls:
        log("No image URLs returned.")
        return None

    os.makedirs("outputs/images", exist_ok=True)
    image_filepaths = []

    for i, image_url in enumerate(image_urls):
        log(f"Processing image {i+1}/{len(image_urls)}...")
        image_filepath = f"outputs/images/{topic.replace(' ', '_')}_{i+1}.png"
        try:
            image = requests.get(image_url).content
            with open(image_filepath, "wb") as image_file:
                image_file.write(image)
            log(f"Image saved as {image_filepath}")
            image_filepaths.append(image_filepath)
        except Exception as e:
            log(f"Error downloading or saving image {i+1}: {e}")

    if image_filepaths:
        return image_filepaths
    else:
        log("No images were saved.")
        return None
