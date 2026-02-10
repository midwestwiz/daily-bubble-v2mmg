import streamlit as st
import feedparser
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="The Daily Bubble",
    page_icon="🫧",
    layout="wide",
    initial_sidebar_state="collapsed" # Hide sidebar for full immersion
)

# V2MMG: HEARTBEAT
# Refresh every 10 minutes (600,000 ms) to keep news and clock fresh
st_autorefresh(interval=10 * 60 * 1000, key="daily_bubble_pulse")

# --- 2. V2MMG STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    
    /* Big Header for Distance Reading */
    .header-box {
        background-color: #2E7D32;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        color: white;
    }
    
    /* The News Cards */
    .news-card {
        background-color: #f1f8e9; /* Very light green */
        padding: 20px;
        border-radius: 12px;
        border-left: 8px solid #2E7D32;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s; /* Smooth animation */
    }
    .news-card:hover {
        transform: scale(1.02); /* Pop out slightly on hover */
    }
    
    .news-title {
        color: #1b5e20;
        font-size: 1.5rem; /* Larger font for distance */
        font-weight: 800;
        font-family: 'Helvetica', sans-serif;
        text-decoration: none;
        display: block;
        margin-bottom: 10px;
    }
    
    .news-meta {
        color: #558b2f;
        font-size: 1rem;
        font-weight: bold;
    }
    
    /* Footer Timestamp */
    .footer-time {
        text-align: center;
        color: #9e9e9e;
        font-size: 0.9rem;
        margin-top: 40px;
        border-top: 1px solid #eee;
        padding-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. LOGIC ---

def get_news():
    # St. Louis + Positive Keywords
    rss_url = "https://news.google.com/rss/search?q=St.+Louis+Missouri+community+OR+grant+OR+success&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    return feed.entries[:5] # Only get top 5 to keep it clean

# --- 4. LAYOUT ---

# A. Header (The "TV Screen" Look)
current_time = datetime.now().strftime("%I:%M %p")
current_date = datetime.now().strftime("%A, %B %d")

st.markdown(f"""
<div class="header-box">
    <h1 style='color: white; margin:0;'>🫧 THE DAILY BUBBLE</h1>
    <h3 style='color: #a5d6a7; margin:0;'>V2MMG NEWS DASHBOARD</h3>
</div>
""", unsafe_allow_html=True)

# B. The Ticker (Simple Marquee)
st.markdown("""
<div style="background-color: #000; color: #0f0; padding: 10px; font-family: monospace; overflow: hidden; white-space: nowrap;">
    <marquee behavior="scroll" direction="left">Creating sustainable narratives for St. Louis...  •  Voyage 2 Mecca Media Group  •  Reporting on The Ville, Kingsway, and beyond...</marquee>
</div>
<br>
""", unsafe_allow_html=True)

# C. The News Feed
news = get_news()

if not news:
    st.error("Waiting for connection...")
else:
    for item in news:
        # Clean up date format if possible
        pub_date = item.published.split(',')[1].split('+')[0].strip() if ',' in item.published else "Today"
        
        st.markdown(f"""
        <div class="news-card">
            <a href="{item.link}" target="_blank" class="news-title">{item.title}</a>
            <div class="news-meta">
                SOURCE: {item.source.title if 'source' in item else 'Google News'} • {pub_date}
            </div>
        </div>
        """, unsafe_allow_html=True)

# D. Footer
st.markdown(f"""
<div class="footer-time">
    LAST UPDATED: {current_time} on {current_date} <br>
    POWERED BY VOYAGE 2 MECCA MEDIA GROUP
</div>
""", unsafe_allow_html=True)
