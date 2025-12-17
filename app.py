import streamlit as st
import feedparser
import time
# ------------------------------------------------------------------
# Scraper Logic
# ------------------------------------------------------------------
def fetch_st_louis_news():
    """
    Fetches news from Google News RSS for St. Louis, MO
    and filters for positive keywords.
    """
    # Google News RSS URL for St. Louis, MO
    rss_url = "https://news.google.com/rss/search?q=St.+Louis+Missouri&hl=en-US&gl=US&ceid=US:en"
    
    feed = feedparser.parse(rss_url)
    
    keywords = [
        "Community", "Sustainability", "Kingsway East", 
        "Grant", "Volunteer", "Charity", "Donation",
        "Green", "Park", "School", "Education", "Fundraiser"
    ]
    
    filtered_news = []
    
    for entry in feed.entries:
        title = entry.get('title', '')
        summary = entry.get('summary', '') # Summary often contains HTML
        link = entry.get('link', '')
        source = entry.get('source', {}).get('title', 'Unknown Source')
        published = entry.get('published', '')
        # Check for keywords (case-insensitive)
        text_to_search = (title + " " + summary).lower()
        
        # We want to find AT LEAST one keyword
        if any(k.lower() in text_to_search for k in keywords):
            filtered_news.append({
                "title": title,
                "link": link,
                "source": source,
                "published": published,
                "summary": summary
            })
            
    return filtered_news
# ------------------------------------------------------------------
# Streamlit App UI
# ------------------------------------------------------------------
# Page Config
st.set_page_config(
    page_title="The Daily Bubble",
    page_icon="🫧",
    layout="centered"
)
# Custom CSS for Green/White Theme
st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background-color: #f8fdf9; /* Very light green hint usually works well for "white" */
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1b5e20; /* Dark Green */
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Buttons */
    .stButton>button {
        color: white;
        background-color: #2e7d32; /* Green */
        border: none;
        border-radius: 20px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
    }
    
    /* Card-like containers for news */
    .news-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 5px solid #4caf50; /* Green accent */
    }
    
    .news-source {
        color: #666;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .news-title {
        color: #2c3e50;
        font-size: 1.2rem;
        font-weight: bold;
        margin: 10px 0;
        text-decoration: none;
    }
    
    .news-title:hover {
        color: #2e7d32;
        text-decoration: underline;
    }
    
    </style>
""", unsafe_allow_html=True)
# Application Header
st.title("🫧 The Daily Bubble")
st.markdown("### Positive St. Louis News")
# Sidebar
with st.sidebar:
    st.header("About")
    st.write("Welcome back! Here's your daily dose of positive news from St. Louis.")
    st.write("Keywords:")
    st.markdown("- Community\\n- Sustainability\\n- Kingsway East\\n- Grant\\n- Volunteer")
# Main Content
if st.button("Refresh News 🔄"):
    st.cache_data.clear()
with st.spinner("Blowing bubbles... (Fetching news)"):
    try:
        news_items = fetch_st_louis_news()
        
        if not news_items:
            st.info("No news found matching your positive keywords right now. Check back later!")
        else:
            st.success(f"Found {len(news_items)} positive stories!")
            
            for item in news_items:
                st.markdown(f"""
                <div class="news-card">
                    <div class="news-source">{item['source']} • {item['published'][:16]}</div>
                    <a href="{item['link']}" target="_blank" class="news-title">{item['title']}</a>
                    <p>{item['summary'].split('<')[0]}...</p>  <!-- Simple HTML strip attempt for summary preview -->
                </div>
                """, unsafe_allow_html=True)
                
    except Exception as e:
        st.error(f"Oof! Pop! Something went wrong: {e}")
# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #888;'>Made with 💚 for St. Louis</div>", unsafe_allow_html=True)

