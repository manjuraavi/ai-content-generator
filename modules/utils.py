 # modules/utils.py

import yaml
import os
import re
from datetime import datetime

# Basic text cleaner
def clean_text(text):
    text = re.sub(r"\s+", " ", text)          # Remove extra spaces/newlines
    text = re.sub(r"http\S+", "", text)       # Remove URLs
    text = text.strip()
    return text

# Simple logger
def log(message):
    os.makedirs("logs", exist_ok=True)
    with open("logs/app.log", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        f.write(f"{timestamp} {message}\n")
    print(f"{timestamp} {message}")

import re

def sanitize_filename(filename):
    """Convert a string to a valid filename."""
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    return filename.strip()

