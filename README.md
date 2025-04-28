# 📝 AI Content Generator

**AI Content Generator** is a Python-based project that automatically:
- Scrapes fresh information from Reddit, Pinterest, StackExchange, and Wikipedia.
- Generates full blog articles using OpenAI's GPT models.
- Creates beautiful AI images related to the blog topic.
- Saves the output as `.doc` blog files and `.png` images.
- Provides a full Web App using Streamlit!

This tool is perfect for bloggers, marketers, and content creators who want to automate content production!

---

## 🚀 Features

- 🔎 **Data Scraping**:
  - Reddit posts
  - Wikipedia articles
  - StackExchange answers
  - Pinterest pins (basic scraping)

- ✍️ **Blog Writing**:
  - Uses OpenAI GPT-3.5 to generate fresh, human-like blog posts.
  - Supports different writing tones and content styles.
  - Formats text with headings, subheadings, and short paragraphs.

- 🗾️ **Image Generation**:
  - Uses an external text-to-image API (ModelsLab) to generate visual content.
  - Option to generate multiple images per blog.

- 🧹 **Utilities**:
  - Text cleaning and filename sanitization.
  - Simple timestamped logging to track progress and issues.

- 📈 **Streamlit App**:
  - Easy-to-use web interface for content generation.
  - Select content options via dropdowns and text inputs.
  - Download generated blogs and images.

---

## 📁 Project Structure

```
ai_content_generator/
│
├── modules/
│   ├── __init__.py           # Module loader
│   ├── blog_generator.py     # Blog creation logic using OpenAI
│   ├── image_generator.py    # Image generation logic
│   ├── scraper.py            # Web scraping logic
│   └── utils.py              # Common utilities (logging, config loading, cleaning)
│
├── config/
│   └── config.yaml           # API keys and configuration file
│
├── outputs/
│   ├── blogs/                # Saved blog documents (.doc)
│   └── images/               # Generated images (.png)
│
├── logs/
│   └── app.log               # Activity logs
│
├── app.py                    # Streamlit web app
├── README.md                  # Project documentation (you're reading it!)
├── requirements.txt           # Python dependencies
└── .gitignore                 # Git ignored files (optional)
```

---

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/manjuraavi/ai-content-generator.git
   cd ai-content-generator
   ```

2. **Create a virtual environment (recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup your API keys**:

   Create a `config/config.yaml` file like this:

   ```yaml
   openai:
     api_key: "your-openai-api-key"

   image:
     key: "your-modelslab-api-key"

   reddit:
     client_id: "your-reddit-client-id"
     client_secret: "your-reddit-client-secret"
     user_agent: "your-user-agent"
   ```

---

## 📚 Usage

### 🌈 1. Run via Streamlit App (Recommended)

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser!

Inside the app, you can:
- Enter a topic (e.g., "Women Fashion", "Egg Recipes")
- Choose options:
  - Only Blog
  - Only Images
  - Both
- Select:
  - Blog style (How-to Guide, Listicle, Story)
  - Blog tone (Friendly, Professional, Inspirational)
  - Focus description for the images (optional)
  - Number of images
- Download `.doc` blog and `.png` images

### 🧬 2. Run Programmatically (Advanced)

```python
from modules import blog_generator, image_generator, scraper

topic = "Women Fashion"

snippets = scraper.scrape_all_sources(topic)
blog_generator.generate_blog(topic, snippets=snippets)
image_generator.generate_image_from_topic(topic, images_count=3)
```

---

## ⚙️ Configuration Options

- **Topic**: The subject for which the blog and images will be created.
- **Content Style**: e.g., "How-to Guide", "Listicle", "Storytelling".
- **Tone**: e.g., "Friendly", "Professional", "Inspirational".
- **Images Count**: Number of images to generate per blog.

You can customize these parameters inside the app or programmatically!

---

## ✅ Requirements

- Python 3.8 or higher
- Internet connection (for API access)

Key Python libraries used:
- `openai`
- `requests`
- `beautifulsoup4`
- `praw`
- `wikipedia`
- `pyyaml`
- `python-dotenv`
- `streamlit`

(Already included in `requirements.txt`.)

---

## 📸 Example Output

- Blog saved at: `outputs/blogs/women_fashion.doc`
- Images saved at: `outputs/images/women_fashion_1.png`, `women_fashion_2.png`, etc.

---

## 💡 Future Improvements

- Add Hugging Face integration for fallback if OpenAI fails.
- Advanced Pinterest scraping using Selenium.
- More blog styles like "Personal Story", "Ultimate Guide."
- User authentication for the app.

---

## 🙏 Credits

- OpenAI API for text generation.
- ModelsLab API for image generation.
- StackExchange, Reddit, Wikipedia for providing real-world content.

---

## 📜 License

MIT License

Copyright (c) 2025 Manjusha

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

# 🔥 Ready to Create Content Automatically? Let's Go! 🚀

