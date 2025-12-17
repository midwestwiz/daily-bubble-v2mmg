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

# --- CUSTOM CSS (Green & White Theme) ---
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .stApp {
        background-color: #ffffff;
    }
    h1, h2, h3 {
        color: #2E8B57; /* SeaGreen */
    }
    .news-card {
        padding: 20px;
        background-color: #f0fdf4; /* Very light green */
        border-radius: 10px;
        border: 1px solid #bbf7d0;
        margin-bottom: 15px;
    }
    .source-tag {
        font-size: 0.8em;
        color: #15803d;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://via.placeholder.com/150x50?text=V2MMG", use_container_width=True)
    st.header("Production Suite")
    st.write("Welcome, Tyrone.")
    st.write("---")
    keywords = st.multiselect(
        "Filter News By:",
        ["Community", "Sustainability", "Grant", "Volunteer", "St. Louis"],
        default=["Community", "St. Louis"]
    )
    st.write("---")
    st.info("Status: System Online")

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

# --- SCRIPT GENERATOR (Placeholder for Phase 2) ---
st.write("---")
st.header("🎙️ Broadcast Script Generator")
st.write("Select stories above to generate your daily script.")
if st.button("Generate Script (AI)"):
    st.success("AI Script Generation coming in Phase 2! (Requires API Key)")
    st.text_area("Script Preview", "Welcome to The Daily Bubble! I'm Tyrone Johnson. Today in St. Louis...", height=150)
