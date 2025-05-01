import streamlit as st
from modules import scraper, blog_generator, image_generator, utils
import openai
import os

# Load config
openai.api_key = st.secrets["openai"]["api_key"]

# Streamlit UI
st.set_page_config(page_title="AI Content Generator", layout="centered")
st.title("AI Content Generator")

# Step 1: Topic input
topic = st.text_input("Enter a topic:")

# Step 2: Content type selection
option = st.selectbox("Choose what to generate:", ["Only Blog", "Only Images", "Both"])

# Conditional options based on selection
if option in ["Only Blog", "Both"]:
    content_style = st.selectbox("Choose a Content Style:", 
                               ["Listicle", "How-to Guide", "Story", "In-depth Explainer", "Quick Tips"])
    tone = st.selectbox("Choose a Tone:", 
                       ["Friendly and Casual", "Professional and Informative", "Fun and Quirky", "Emotional/Storytelling"])

if option in ["Only Images", "Both"]:
    image_focus = st.text_input("Describe what the image should show:", 
                               help="Be specific for better results (e.g. 'a futuristic robot chef preparing sushi')")
    image_count = st.number_input("Number of images to generate:", min_value=1, max_value=10, value=1)

generate_btn = st.button("Generate")

if generate_btn and topic:
    utils.log(f"Generating content for: {topic}")
    st.info(f"Gathering data for **{topic}**...")

    blog_file_path = None
    image_paths = []

    # Blog generation
    if option in ["Only Blog", "Both"]:
        with st.spinner("Researching and writing blog content..."):
            # Scrape snippets
            all_snippets = scraper.scrape_all_sources(topic)
            all_snippets = [utils.clean_text(s) for s in all_snippets if s.strip()]
            
            st.subheader("📝 Generated Blog")
            blog = blog_generator.generate_blog(topic, content_style, tone, image_focus if option == "Both" else "", all_snippets)
            st.markdown(blog)
            
            # Save and offer download
            os.makedirs("outputs/blogs", exist_ok=True)
            blog_file_path = f"outputs/blogs/{utils.sanitize_filename(topic)}.doc"
            with open(blog_file_path, "w", encoding="utf-8") as f:
                f.write(blog)
            with open(blog_file_path, "rb") as f:
                st.download_button("📄 Download Blog", f, file_name=os.path.basename(blog_file_path), mime="application/msword")

    # Image generation
    if option in ["Only Images", "Both"]:
        with st.spinner("Generating images..."):
            st.subheader("🖼️ Generated Images")
            image_paths = image_generator.generate_image_from_topic(
                topic, 
                image_focus if image_focus else topic,
                images_count=image_count
            )
            
            if not image_paths:
                st.warning("No images generated.")
            else:
                st.success(f"Generated {len(image_paths)} images!")
                
                # Display images with download buttons
                cols = st.columns(3)
                for i, img_path in enumerate(image_paths):
                    with cols[i % 3]:
                        st.image(img_path, caption=f"Image {i+1}")
                        with open(img_path, "rb") as img_file:
                            st.download_button(
                                f"⬇️ Download Image {i+1}", 
                                img_file, 
                                file_name=os.path.basename(img_path), 
                                mime="image/png"
                            )

elif generate_btn:
    st.warning("Please enter a topic.")