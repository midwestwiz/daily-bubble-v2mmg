import streamlit as st
import feedparser
import pytz  # <--- New Tool for Timezones
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="The Daily Bubble",
    page_icon="🫧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# V2MMG: HEARTBEAT (10 mins)
st_autorefresh(interval=10 * 60 * 1000, key="daily_bubble_pulse")

# --- 2. V2MMG STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    
    /* Header Box */
    .header-box {
        background-color: #2E7D32;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        color: white;
    }
    
    /* News Cards */
    .news-card {
        background-color: #f1f8e9;
        padding: 20px;
        border-radius: 12px;
        border-left: 8px solid #2E7D32;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .news-card:hover {
        transform: scale(1.02);
    }
    
    .news-title {
        color: #1b5e20;
        font-size: 1.5rem;
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
    
    /* Ticker Styling */
    .ticker-wrap {
        width: 100%;
        background-color: #000;
        padding-top: 10px;
        padding-bottom: 10px;
        margin-bottom: 20px;
        border-bottom: 4px solid #2E7D32;
    }
    .ticker-text {
        color: #00ff00; 
        font-family: 'Courier New', monospace;
        font-size: 1.2rem;
        font-weight: bold;
    }

    /* Footer */
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

def get_st_louis_time():
    """Get the current time specifically for St. Louis (Central Time)"""
    utc_now = datetime.now(pytz.utc)
    st_louis_tz = pytz.timezone('America/Chicago')
    return utc_now.astimezone(st_louis_tz)

def get_news():
    # St. Louis + Positive Keywords
    rss_url = "https://news.google.com/rss/search?q=St.+Louis+Missouri+community+OR+grant+OR+success&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    return feed.entries[:5]

# --- 4. LAYOUT ---

# Get accurate time
now_stl = get_st_louis_time()
current_time = now_stl.strftime("%I:%M %p")
current_date = now_stl.strftime("%A, %B %d, %Y")

# A. Header
st.markdown(f"""
<div class="header-box">
    <h1 style='color: white; margin:0;'>🫧 THE DAILY BUBBLE</h1>
    <h3 style='color: #a5d6a7; margin:0;'>V2MMG NEWS DASHBOARD</h3>
</div>
""", unsafe_allow_html=True)

# B. The Ticker (Correct Neighborhoods)
st.markdown("""
<div class="ticker-wrap">
    <marquee class="ticker-text" behavior="scroll" direction="left" scrollamount="10">
    🔴 LIVE: Reporting for Kingsway East, The Ville, and Greater Ville  •  Voyage 2 Mecca Media Group  •  Building Sustainable Narratives for St. Louis  •  Community First  •  
    </marquee>
</div>
""", unsafe_allow_html=True)

# C. News Feed
news = get_news()

if not news:
    st.error("Waiting for connection...")
else:
    for item in news:
        # Clean date logic
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
