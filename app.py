import streamlit as st
import feedparser
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="The Daily Bubble",
    page_icon="🫧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS (Forces Light Mode & Public Styling) ---
st.markdown("""
    <style>
    /* Force background to white and text to dark grey */
    .stApp {
        background-color: #ffffff;
        color: #333333;
    }
    .main {
        background-color: #ffffff;
    }
    /* Force all standard text to be dark */
    p, li, .stMarkdown {
        color: #333333 !important;
    }
    h1, h2, h3 {
        color: #2E8B57 !important; /* SeaGreen */
    }
    /* Card Styling */
    .news-card {
        padding: 20px;
        background-color: #f0fdf4; 
        border-radius: 10px;
        border: 1px solid #bbf7d0;
        margin-bottom: 15px;
    }
    .source-tag {
        font-size: 0.8em;
        color: #15803d;
        font-weight: bold;
    }
    /* Hide the default Streamlit menu slightly for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Public View) ---
with st.sidebar:
    st.image("https://via.placeholder.com/150x50?text=V2MMG", use_container_width=True)
    st.header("Dashboard Controls") # Renamed from Production Suite
    st.write("Customize your news feed:")
    st.write("---")
    keywords = st.multiselect(
        "Filter Stories By:",
        ["Community", "Sustainability", "Grant", "Volunteer", "St. Louis"],
        default=["Community", "St. Louis"]
    )
    st.write("---")
    st.info("ℹ️ Updates every 24 hours")

# --- MAIN APP ---
st.title("🫧 The Daily Bubble")
st.subheader("Positive News Aggregator for St. Louis (Last 7 Days)")

# --- NEWS FETCHING FUNCTION ---
def get_stl_news():
    # RSS Feed for St. Louis News (Google News) - FILTERED FOR LAST 7 DAYS
    rss_url = "https://news.google.com/rss/search?q=St.+Louis+community+good+news+when:7d&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(rss_url)
    return feed.entries

# --- DISPLAY NEWS ---
if st.button("🔄 Refresh News Feed"):
    st.rerun()

st.write("### 📰 Latest Headlines")

try:
    news_items = get_stl_news()
    
    # Create columns for a grid layout
    cols = st.columns(2)
    
    if not news_items:
        st.warning("No recent stories found in the last 7 days. Try removing the time filter or checking back later.")
    
    for index, item in enumerate(news_items[:10]): # Show top 10
        with cols[index % 2]:
            # Clean up the date
            published = item.get("published", "Recent")
            
            # HTML Card
            st.markdown(f"""
            <div class="news-card">
                <div class="source-tag">SOURCE: {item.source.title} | {published}</div>
                <h3>{item.title}</h3>
                <p><a href="{item.link}" target="_blank" style="text-decoration: none; color: #2E8B57;"><b>🔗 Read Full Story</b></a></p>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Could not load news feed: {e}")

# --- SCRIPT GENERATOR (Hidden for Public/Demo Mode) ---
st.write("---")
st.caption("Powered by V2MMG Technology | © 2025")
