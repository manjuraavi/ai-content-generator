# Updated modules/scraper.py

import requests
from bs4 import BeautifulSoup
import praw
import re
import urllib.parse
import wikipedia
import streamlit as st
from modules.utils import log

# Reddit Config
REDDIT_CLIENT_ID = st.secrets["reddit"]["client_id"]
REDDIT_CLIENT_SECRET = st.secrets["reddit"]["client_secret"]
REDDIT_USER_AGENT = st.secrets["reddit"]["user_agent"]

# --- Reddit Scraper ---
def scrape_reddit_posts(keyword, limit=10):
    log(f"Scraping Reddit for: {keyword}")
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent=REDDIT_USER_AGENT
    )
    posts = []
    for submission in reddit.subreddit("all").search(keyword, limit=limit, sort='new'):
        if not submission.stickied:
            posts.append(submission.title + " - " + submission.selftext[:200])
    if not posts:
        posts.append("No relevant Reddit posts found.")
    return posts

def scrape_wikipedia_articles(keyword, limit=5):
    log(f"Scraping Wikipedia for: {keyword}")
    
    # Initialize the Wikipedia API
    
    # Search for the keyword in Wikipedia
    search_results = wikipedia.search(keyword, results=limit)
    log(f"Wikipedia search results: {search_results}")
    
    # Fetch the summaries of the search results
    articles = []
    for result in search_results:
        try:
            result_title = result.strip()
            # Get the summary of the page
            summary = wikipedia.summary(result_title, sentences=2)  # Limit summary to 2 sentences
            articles.append(f"Title: {result_title}\nSummary: {summary}")
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation if needed
            options = e.options[:5]
            articles.append(f"Title: {result}\nSummary: Disambiguation required, options: {e.options}")
        except wikipedia.exceptions.PageError:
            # Handle case where no page is found
            articles.append(f"Title: {result_title}\nSummary: No page found.")
        
        except wikipedia.exceptions.HTTPTimeoutError:
            # Handle timeout errors
            articles.append(f"Title: {result_title}\nSummary: Request timed out.")
        
        except wikipedia.exceptions.RequestException as e:
            # Catch any other request-related errors
            articles.append(f"Title: {result_title}\nSummary: Error with Wikipedia request: {e}")


    if not articles:
        articles.append("No relevant Wikipedia articles found.")
    
    return articles

# --- Pinterest Scraper ---
def scrape_pinterest_pins(keyword, limit=5):
    log(f"Scraping Pinterest for: {keyword}")
    query = urllib.parse.quote(keyword)
    search_url = f"https://www.pinterest.com/search/pins/?q={query}"
    log(f"Pinterest search URL: {search_url}")
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }
    try:
        response = requests.get(search_url, headers=headers, timeout=20)
        response.raise_for_status()
    except Exception as e:
        log(f"Pinterest request failed: {e}")
        return ["No Pinterest pins found."]

    soup = BeautifulSoup(response.text, "html.parser")
    pins = []
    for div in soup.find_all("div", string=re.compile(r".+")):
        text = div.get_text(strip=True)
        if text and len(text) > 30:
            pins.append(text)
            if len(pins) >= limit:
                break

    if not pins:
        pins.append("No Pinterest pins found.")
    return pins

def get_relevant_stackexchange_sites(keyword):
    """Returns only StackExchange sites relevant to the keyword."""    
    # Map keywords to relevant sites
    topic_to_sites = {
        "cooking": ["cooking"],
        "programming": ["stackoverflow", "askubuntu"],
        "math": ["math"],
        "gaming": ["gaming"],
        # Add more mappings as needed
    }
    
    # Check if keyword matches a known topic
    for topic, sites in topic_to_sites.items():
        if topic in keyword.lower():
            return [f"{site}.stackexchange.com" for site in sites]
    
    # Default: Only search general sites (meta, stackoverflow, etc.)
    return ["stackoverflow", "superuser", "serverfault"]
    
# --- StackExchange General Scraper ---
def scrape_stackexchange_answers(keyword, limit=5):
    sites = get_relevant_stackexchange_sites(keyword)  # Only relevant sites
    
    snippets = []
    for site in sites:
        print(f"Searching in site: {site}")
        
        search_url = "https://api.stackexchange.com/2.3/search/advanced"
        params = {
            "order": "desc",
            "sort": "relevance",
            "q": keyword,
            "site": site,
            "filter": "!9Z(-wz0fP",
            "pagesize": limit
        }
        
        try:
            response = requests.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            for item in data['items']:
                question_title = item['title']
                question_link = item['link']
                answer_count = item.get('answer_count', 0)

                snippet = f"Question: {question_title}\nLink: {question_link}\nAnswers: {answer_count} answers"
                snippets.append(snippet)

        except Exception as e:
            print(f"Error fetching data from site {site}: {e}")
            continue

    if not snippets:
        snippets.append("No relevant StackExchange answers found.")
    
    return snippets

def scrape_all_sources(topic):
    reddit_snippets = scrape_reddit_posts(topic)
    wikipedia_snippets = scrape_wikipedia_articles(topic)
    stackexchange_snippets = scrape_stackexchange_answers(topic)
    pinterest_snippets = scrape_pinterest_pins(topic)

    all_snippets = reddit_snippets + wikipedia_snippets + stackexchange_snippets + pinterest_snippets
    return all_snippets