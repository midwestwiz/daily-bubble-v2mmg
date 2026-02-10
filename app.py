import streamlit as st
import pandas as pd
import feedparser
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURATION & HEARTBEAT ---
st.set_page_config(
    page_title="The Daily Bubble",
    page_icon="🫧",
    layout="wide"
)

# V2MMG: Heartbeat - Auto-refresh every 15 minutes to keep app awake
# This prevents the app from "sleeping" on the free tier
st_autorefresh(interval=15 * 60 * 1000, key="daily_bubble_refresh")

# --- 2. V2MMG STYLING (Green & White) ---
st.markdown("""
    <style>
    /* Main Background to White */
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    
    /* V2MMG Green Accents */
    h1, h2, h3 {
        color: #2E7D32 !important; 
        font-family: 'Helvetica', sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #f0fdf4; /* Light mint green */
        border-right: 2px solid #2E7D32;
    }
    
    /* Cards for News Items */
    .news-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .news-title {
        color: #1b5e20;
        font-size: 1.2rem;
        font-weight: bold;
        text-decoration: none;
    }
    .news-meta {
        color: #666;
        font-size: 0.9rem;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. FUNCTIONS ---

def fetch_st_louis_news():
    """Fetches news from Google News RSS for St. Louis"""
    # URL for Google News search: "St. Louis" + "Good News" (optimistic filter)
    rss_url = "https://news.google.com/rss/search?q=St.+Louis+Missouri+when:7d&hl=en-US&gl=US&ceid=US:en"
    
    feed = feedparser.parse(rss_url)
    news_items = []
    
    for entry in feed.entries:
        news_items.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.published,
            'summary': entry.get('summary', 'No summary available.')
        })
    
    return news_items

# --- 4. MAIN APP LAYOUT ---

# Sidebar Controls
with st.sidebar:
    st.image("https://placehold.co/200x100/2E7D32/ffffff?text=V2MMG", use_container_width=True)
    st.header("Dashboard Controls")
    
    # Keyword Filter
    filter_options = ["All", "Community", "Sustainability", "Grant", "Volunteer", "Arts", "Business"]
    selected_filter = st.selectbox("Filter News By:", filter_options)
    
    st.markdown("---")
    st.write("Logged in as: **Tyrone Johnson**")
    st.caption(f"Last Updated: {datetime.now().strftime('%I:%M %p')}")

# Main Feed
st.title("The Daily Bubble 🫧")
st.subheader("St. Louis Positive News Feed")

# Load Data
news_data = fetch_st_louis_news()

# Display News
if not news_data:
    st.warning("No news found at the moment. Check your connection.")
else:
    count = 0
    for item in news_data:
        # Filter Logic
        show_item = True
        if selected_filter != "All":
            # Check if filter keyword is in the title (case insensitive)
            if selected_filter.lower() not in item['title'].lower():
                show_item = False
        
        # Render Card
        if show_item:
            count += 1
            st.markdown(f"""
            <div class="news-card">
                <a href="{item['link']}" target="_blank" class="news-title">{item['title']}</a>
                <div class="news-meta">📅 {item['published']}</div>
            </div>
            """, unsafe_allow_html=True)

    if count == 0:
        st.info(f"No stories found matching '{selected_filter}'. Try selecting 'All'.")
