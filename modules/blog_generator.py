 # modules/blog_generator.py

import os
from openai import OpenAI
from modules.utils import log
import streamlit as st

# Set your OpenAI API key
openai_api_key = st.secrets["openai"]["api_key"]
client = OpenAI(api_key=openai_api_key)


def generate_blog(topic, content_style=None, tone=None, image_focus=None, snippets=None):
    content_style = content_style or "How-to Guide"
    tone = tone or "Friendly and Casual"
    image_focus = image_focus or f"a general visual representation of {topic}"
    prompt = (
    f"""Using Reddit and Google scraped content: {snippets}, write a blog post on the topic: {topic}.
        Format the blog in the style of a {content_style}.
        The tone should be {tone}.
        Rewrite the information originally — do not copy-paste. Make it feel fresh, human, and engaging.
        Structure the blog with headings, subheadings, and short paragraphs.

        Output the blog content in text format, ready to be saved as a downloadable .doc file."""
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a content generator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )

    blog_text = response.choices[0].message.content.strip()
    save_blog(topic, blog_text)
    return blog_text

def save_blog(topic, content):
    os.makedirs("outputs/blogs", exist_ok=True)
    filename = f"outputs/blogs/{topic.replace(' ', '_')}.doc"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    log(f"Blog saved as {filename}")

