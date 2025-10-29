import streamlit as st
import streamlit.components.v1 as components
from datetime import date, datetime
from typing import Dict, List, Any, Optional
import json
from api_service import api_service
from components.create_draft_modal import create_draft_modal
# Configuration
API_BASE_URL = "http://localhost:8000"

# Spotify Colors
SPOTIFY_GREEN = "#1DB954"
SPOTIFY_BLACK = "#191414"
SPOTIFY_WHITE = "#FFFFFF"
SPOTIFY_LIGHT_GRAY = "#F6F6F6"
SPOTIFY_DARK_GRAY = "#535353"

# Tab names and order
TAB_NAMES = ["Objective", "Targeting", "Format", "Delivery", "Budget", "Bidding"]

# Static data
CAMPAIGN_OBJECTIVES = [
    {"value": "REACH", "label": "Reach"},
    {"value": "EVEN_IMPRESSION_DELIVERY", "label": "Even Impression Delivery"},
    {"value": "CLICKS", "label": "Clicks"},
    {"value": "VIDEO_VIEWS", "label": "Video Views"},
    {"value": "PODCAST_STREAMS", "label": "Podcast Streams"},
    {"value": "APP_INSTALLS", "label": "App Installs"},
    {"value": "WEBSITE_VISITS", "label": "Website Visits"}
]

COUNTRIES = [
    {"code": "US", "name": "United States"},
    {"code": "CA", "name": "Canada"},
    {"code": "MX", "name": "Mexico"},
    {"code": "BR", "name": "Brazil"},
    {"code": "DE", "name": "Germany"},
    {"code": "DK", "name": "Denmark"},
    {"code": "ES", "name": "Spain"},
    {"code": "FI", "name": "Finland"},
    {"code": "FR", "name": "France"},
    {"code": "IT", "name": "Italy"},
    {"code": "NL", "name": "Netherlands"},
    {"code": "NO", "name": "Norway"},
    {"code": "SE", "name": "Sweden"},
    {"code": "GB", "name": "United Kingdom"},
    {"code": "AU", "name": "Australia"},
    {"code": "NZ", "name": "New Zealand"},
    {"code": "IN", "name": "India"}
]

DEVICES = [
    {"value": "IOS", "label": "iOS"},
    {"value": "ANDROID", "label": "Android"},
    {"value": "DESKTOP", "label": "Desktop"}
]

ASSET_FORMATS = [
    {"value": "AUDIO", "label": "Audio"},
    {"value": "VIDEO", "label": "Video"},
    {"value": "IMAGE", "label": "Display"}
]

GENDER_OPTIONS = [
    {"value": "MALE", "label": "Male"},
    {"value": "FEMALE", "label": "Female"},
    {"value": "NON_BINARY", "label": "Non-Binary"}
]

BID_STRATEGY_OPTIONS = [
    {"value": "COST_PER_RESULT", "label": "Cost Per Result"},
    {"value": "MAX_BID", "label": "Max Bid"}
]

AGE_RANGE_OPTIONS = [
    {"value": "all", "label": "All (13 - 65+)", "min": 13, "max": 65},
    {"value": "age_restricted", "label": "Age-restricted advertising (21+)", "min": 21, "max": 65},
    {"value": "13_15", "label": "13–15", "min": 13, "max": 15},
    {"value": "16_17", "label": "16–17", "min": 16, "max": 17},
    {"value": "18_24", "label": "18–24", "min": 18, "max": 24},
    {"value": "25_34", "label": "25–34", "min": 25, "max": 34},
    {"value": "35_44", "label": "35–44", "min": 35, "max": 44},
    {"value": "45_54", "label": "45–54", "min": 45, "max": 54},
    {"value": "55_64", "label": "55–64", "min": 55, "max": 64},
    {"value": "65_plus", "label": "65+", "min": 65, "max": 99}
]

PLACEMENT_TYPES = [
    {"value": "MUSIC", "label": "Music"},
    {"value": "PODCAST", "label": "Podcast"}
]

SENSITIVE_FILTER_LEVELS = [
    {"value": "standard", "label": "Standard"},
    {"value": "limited", "label": "Limited"},
    {"value": "partial", "label": "Partial"},
    {"value": "restricted", "label": "Restricted"}
]

BUDGET_TYPES = [
    {"value": "LIFETIME", "label": "Lifetime Budget"}
]

GENRES = [
    {"id": "alternative", "name": "Alternative"},
    {"id": "blues", "name": "Blues"},
    {"id": "christian", "name": "Christian"},
    {"id": "classical", "name": "Classical"},
    {"id": "country", "name": "Country"},
    {"id": "easylistening", "name": "Easy Listening"},
    {"id": "edm", "name": "EDM"},
    {"id": "electronica", "name": "Electronica"},
    {"id": "folk", "name": "Folk"},
    {"id": "funk", "name": "Funk"},
    {"id": "hiphop", "name": "Hip Hop"},
    {"id": "holiday", "name": "Holiday"},
    {"id": "house", "name": "House"},
    {"id": "indierock", "name": "Indie Rock"},
    {"id": "jazz", "name": "Jazz"},
    {"id": "latin", "name": "Latin"},
    {"id": "metal", "name": "Metal"},
    {"id": "newage", "name": "New Age"},
    {"id": "pop", "name": "Pop"},
    {"id": "punk", "name": "Punk"},
    {"id": "reggae", "name": "Reggae"},
    {"id": "rnb", "name": "RnB"},
    {"id": "rock", "name": "Rock"},
    {"id": "soundtrack", "name": "Soundtrack"},
    {"id": "spokenandaudio", "name": "Spoken and Audio"},
    {"id": "traditional", "name": "Traditional"}
]

PLAYLISTS = [
    {"id": "chill", "name": "Chill"},
    {"id": "cooking", "name": "Cooking"},
    {"id": "dinner", "name": "Dinner"},
    {"id": "focusstudy", "name": "Focus"},
    {"id": "gaming", "name": "Gaming"},
    {"id": "holidays", "name": "Holidays"},
    {"id": "party", "name": "Party"},
    {"id": "study", "name": "Study"},
    {"id": "travel", "name": "Travel"},
    {"id": "workout", "name": "Workout"}
]

PODCAST_EPISODE_TOPICS = [
    {"id": "automotive", "name": "Automotive"},
    {"id": "books-and-literature", "name": "Books and Literature"},
    {"id": "business-and-finance", "name": "Business and Finance"},
    {"id": "careers", "name": "Careers"},
    {"id": "education", "name": "Education"},
    {"id": "events-and-attractions", "name": "Events and Attractions"},
    {"id": "family-and-relationships", "name": "Family and Relationships"},
    {"id": "fine-art", "name": "Fine Art"},
    {"id": "food-and-drink", "name": "Food & Drink"},
    {"id": "healthy-living", "name": "Healthy Living"},
    {"id": "hobbies-and-interests", "name": "Hobbies & Interests"},
    {"id": "home-and-garden", "name": "Home & Garden"},
    {"id": "medical-health", "name": "Medical Health"},
    {"id": "movies", "name": "Movies"},
    {"id": "music-and-audio", "name": "Music and Audio"},
    {"id": "news-and-politics", "name": "News and Politics"},
    {"id": "personal-finance", "name": "Personal Finance"},
    {"id": "pets", "name": "Pets"},
    {"id": "pop-culture", "name": "Pop Culture"},
    {"id": "real-estate", "name": "Real Estate"},
    {"id": "religion-and-spirituality", "name": "Religion & Spirituality"},
    {"id": "science", "name": "Science"},
    {"id": "shopping", "name": "Shopping"},
    {"id": "sports", "name": "Sports"},
    {"id": "style-and-fashion", "name": "Style & Fashion"},
    {"id": "technology-and-computing", "name": "Technology & Computing"},
    {"id": "television", "name": "Television"},
    {"id": "travel", "name": "Travel"},
    {"id": "video-gaming", "name": "Video Gaming"}
]

LANGUAGES = [
    {"id": "en", "name": "English"},
    {"id": "fr", "name": "French"},
    {"id": "de", "name": "German"},
    {"id": "it", "name": "Italian"},
    {"id": "ja", "name": "Japanese"},
    {"id": "pt", "name": "Portuguese"},
    {"id": "es", "name": "Spanish"}
]


def apply_custom_css():
    """Apply custom CSS for Spotify branding."""
    st.markdown(f"""
        <style>
        /* Import better fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* Main app styling */
        .stApp {{
            background-color: {SPOTIFY_WHITE};
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        /* Remove ALL top padding/margin */
        .block-container {{
            padding-top: 0rem !important;
            margin-top: 0 !important;
        }}

        /* Ensure main container starts from very top */
        section.main > div:first-child {{
            margin-top: 0 !important;
            padding-top: 0 !important;
        }}

        /* Hide Streamlit header and footer for clean look */
        header, footer {{
            visibility: hidden;
            height: 0;
        }}

        /* Remove space above header */
        .main {{
            padding-top: 0 !important;
            margin-top: 0 !important;
        }}

        /* Remove default Streamlit padding */
        header {{
            padding-top: 0 !important;
        }}

        .stApp > header {{
            background-color: transparent !important;
            padding: 0 !important;
        }}

        /* Headers */
        h1, h2, h3, h4, h5, h6 {{
            color: {SPOTIFY_BLACK} !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
        }}

        h1 {{
            color: {SPOTIFY_GREEN} !important;
            font-size: 3rem !important;
            margin-bottom: 0.5rem !important;
        }}

        h2 {{
            font-size: 1.5rem !important;
            margin-top: 2rem !important;
            margin-bottom: 1rem !important;
        }}

        h3 {{
            font-size: 1.3rem !important;
            margin-top: 1.5rem !important;
            color: {SPOTIFY_DARK_GRAY} !important;
        }}

        /* Text and labels */
        p, .stMarkdown, label {{
            color: {SPOTIFY_BLACK} !important;
            font-size: 1.2rem !important;
            line-height: 1.6 !important;
        }}

        label {{
            font-weight: 500 !important;
            margin-bottom: 0.5rem !important;
        }}

        /* Input fields */
        .stTextInput input, .stSelectbox select, .stNumberInput input, .stDateInput input {{
            border: 2px solid {SPOTIFY_BLACK} !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            font-size: 1rem !important;
            background-color: {SPOTIFY_WHITE} !important;
            color: {SPOTIFY_BLACK} !important;
            transition: all 0.3s ease !important;
        }}

        .stTextInput input:focus, .stSelectbox select:focus, .stNumberInput input:focus {{
            border-color: {SPOTIFY_GREEN} !important;
            box-shadow: 0 0 0 2px rgba(29, 185, 84, 0.1) !important;
            outline: none !important;
        }}

        /* Number input styling */
        .stNumberInput > div > div {{
            border: 2px solid {SPOTIFY_BLACK} !important;
            border-radius: 8px !important;
        }}

        /* Date input styling */
        .stDateInput > div > div {{
            border: 2px solid {SPOTIFY_BLACK} !important;
            border-radius: 8px !important;
        }}

        /* Remove red focus outline */
        input:focus, select:focus, textarea:focus, button:focus {{
            outline: none !important;
            box-shadow: none !important;
        }}

        /* Dropdown/Selectbox comprehensive styling */
        .stSelectbox > div > div {{
            background-color: {SPOTIFY_WHITE} !important;
            color: {SPOTIFY_BLACK} !important;
            border: 2px solid {SPOTIFY_BLACK} !important;
            border-radius: 8px !important;
        }}

        .stSelectbox div[data-baseweb="select"] {{
            background-color: {SPOTIFY_WHITE} !important;
            border: 2px solid {SPOTIFY_BLACK} !important;
            border-radius: 8px !important;
        }}

        .stSelectbox div[data-baseweb="select"] > div {{
            background-color: {SPOTIFY_WHITE} !important;
            color: {SPOTIFY_BLACK} !important;
            border: 2px solid {SPOTIFY_BLACK} !important;
            border-radius: 8px !important;
        }}

        /* Dropdown menu when opened */
        [data-baseweb="popover"] {{
            background-color: {SPOTIFY_WHITE} !important;
            border: 2px solid {SPOTIFY_BLACK} !important;
            border-radius: 8px !important;
        }}

        [data-baseweb="menu"] {{
            background-color: {SPOTIFY_WHITE} !important;
            border: 2px solid {SPOTIFY_BLACK} !important;
            border-radius: 8px !important;
        }}

        [data-baseweb="menu"] ul {{
            background-color: {SPOTIFY_WHITE} !important;
        }}

        [data-baseweb="menu"] li {{
            background-color: {SPOTIFY_WHITE} !important;
            color: {SPOTIFY_BLACK} !important;
        }}

        [data-baseweb="menu"] li:hover {{
            background-color: {SPOTIFY_LIGHT_GRAY} !important;
        }}

        /* Option items */
        [role="option"] {{
            background-color: {SPOTIFY_WHITE} !important;
            color: {SPOTIFY_BLACK} !important;
        }}

        [role="option"]:hover {{
            background-color: {SPOTIFY_LIGHT_GRAY} !important;
        }}

        /* Selected value display */
        [data-baseweb="select"] span {{
            color: {SPOTIFY_BLACK} !important;
        }}

        /* Buttons */
        .stButton > button {{
            background-color: {SPOTIFY_GREEN} !important;
            color: {SPOTIFY_WHITE} !important;
            border: none !important;
            border-radius: 500px !important;
            padding: 14px 32px !important;
            font-size: 1.05rem !important;
            font-weight: 700 !important;
            letter-spacing: 1px !important;
            text-transform: uppercase !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 12px rgba(29, 185, 84, 0.3) !important;
        }}

        .stButton > button:hover {{
            background-color: #1ed760 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(29, 185, 84, 0.4) !important;
        }}

        .stButton > button:active {{
            transform: translateY(0px) !important;
        }}

        /* Secondary button style for Previous */
        .stButton > button[kind="secondary"] {{
            background-color: {SPOTIFY_WHITE} !important;
            color: {SPOTIFY_BLACK} !important;
            border: 2px solid {SPOTIFY_BLACK} !important;
            box-shadow: none !important;
        }}

        .stButton > button[kind="secondary"]:hover {{
            background-color: {SPOTIFY_LIGHT_GRAY} !important;
            border-color: {SPOTIFY_GREEN} !important;
            color: {SPOTIFY_GREEN} !important;
        }}

        /* Checkboxes */
        .stCheckbox {{
            padding: 8px 12px !important;
            border-radius: 8px !important;
            background-color: {SPOTIFY_WHITE} !important;
            transition: background-color 0.2s ease !important;
        }}

        .stCheckbox:hover {{
            background-color: {SPOTIFY_LIGHT_GRAY} !important;
        }}

        /* Checkbox input styling */
        input[type="checkbox"] {{
            accent-color: {SPOTIFY_GREEN} !important;
            width: 20px !important;
            height: 20px !important;
            cursor: pointer !important;
        }}

        /* Radio buttons */
        .stRadio > div {{
            background-color: {SPOTIFY_WHITE} !important;
            padding: 16px !important;
            border-radius: 12px !important;
            border: 2px solid #E0E0E0 !important;
        }}

        input[type="radio"] {{
            accent-color: {SPOTIFY_GREEN} !important;
            width: 20px !important;
            height: 20px !important;
            cursor: pointer !important;
        }}

        /* Tabs - hide default tabs since we're using custom navigation */
        .stTabs {{
            display: none !important;
        }}

        /* Progress bar container */
        .progress-container {{
            background-color: {SPOTIFY_LIGHT_GRAY};
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 32px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }}

        /* Progress steps */
        .progress-steps {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: relative;
            margin-bottom: 16px;
        }}

        .progress-step {{
            flex: 1;
            text-align: center;
            position: relative;
            z-index: 1;
        }}

        .progress-step-circle {{
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background-color: {SPOTIFY_WHITE};
            border: 3px solid #E0E0E0;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.1rem;
            color: {SPOTIFY_DARK_GRAY};
            margin-bottom: 8px;
            transition: all 0.3s ease;
        }}

        .progress-step-circle.active {{
            background-color: {SPOTIFY_GREEN};
            border-color: {SPOTIFY_GREEN};
            color: {SPOTIFY_WHITE};
            transform: scale(1.1);
            box-shadow: 0 4px 12px rgba(29, 185, 84, 0.4);
        }}

        .progress-step-circle.completed {{
            background-color: {SPOTIFY_GREEN};
            border-color: {SPOTIFY_GREEN};
            color: {SPOTIFY_WHITE};
        }}

        .progress-step-label {{
            font-size: 0.9rem;
            font-weight: 600;
            color: {SPOTIFY_DARK_GRAY};
        }}

        .progress-step-label.active {{
            color: {SPOTIFY_GREEN};
        }}

        /* Content card */
        .content-card {{
            background-color: {SPOTIFY_WHITE};
            border: 2px solid {SPOTIFY_LIGHT_GRAY};
            border-radius: 16px;
            padding: 32px;
            margin: 24px 0;
            box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        }}

        /* Section divider */
        .section-divider {{
            height: 3px;
            background: linear-gradient(90deg, {SPOTIFY_GREEN} 0%, transparent 100%);
            margin: 32px 0;
            border-radius: 2px;
        }}

        /* Navigation buttons container */
        .nav-buttons {{
            display: flex;
            justify-content: space-between;
            gap: 16px;
            margin-top: 32px;
            padding-top: 24px;
            border-top: 2px solid {SPOTIFY_LIGHT_GRAY};
        }}

        /* Info box */
        .info-box {{
            background-color: #E8F5E9;
            border-left: 4px solid {SPOTIFY_GREEN};
            padding: 16px 20px;
            border-radius: 8px;
            margin: 16px 0;
        }}

        .info-box p {{
            color: #2E7D32 !important;
            margin: 0 !important;
        }}

        /* Success message */
        .stSuccess {{
            background-color: #E8F5E9 !important;
            color: #2E7D32 !important;
            border-radius: 8px !important;
        }}

        /* Error message */
        .stError {{
            background-color: #FFEBEE !important;
            color: #C62828 !important;
            border-radius: 8px !important;
        }}

        /* Metrics */
        .stMetric {{
            background-color: {SPOTIFY_WHITE};
            padding: 16px;
            border-radius: 12px;
            border: 2px solid #E0E0E0;
        }}

        .stMetric label {{
            color: {SPOTIFY_BLACK} !important;
            font-weight: 600 !important;
        }}

        .stMetric [data-testid="stMetricValue"] {{
            color: {SPOTIFY_BLACK} !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
        }}

        .stMetric [data-testid="stMetricDelta"] {{
            color: {SPOTIFY_BLACK} !important;
        }}

        /* Expander styling */
        .streamlit-expanderHeader {{
            background-color: {SPOTIFY_WHITE} !important;
            border: 2px solid #E0E0E0 !important;
            border-radius: 8px !important;
            color: {SPOTIFY_BLACK} !important;
            font-weight: 600 !important;
        }}

        .streamlit-expanderHeader:hover {{
            border-color: {SPOTIFY_GREEN} !important;
        }}

        .streamlit-expanderHeader svg {{
            fill: {SPOTIFY_GREEN} !important;
        }}

        /* Calendar/Date picker styling */
        .stDateInput > div > div {{
            background-color: {SPOTIFY_WHITE} !important;
            border: 2px solid #E0E0E0 !important;
        }}

        /* Number input dropdown styling */
        .stNumberInput select {{
            background-color: {SPOTIFY_WHITE} !important;
            color: {SPOTIFY_BLACK} !important;
        }}

        /* All dropdown/select menus */
        select {{
            background-color: {SPOTIFY_WHITE} !important;
            color: {SPOTIFY_BLACK} !important;
        }}

        select option {{
            background-color: {SPOTIFY_WHITE} !important;
            color: {SPOTIFY_BLACK} !important;
        }}

        /* Caption text */
        .caption, small {{
            color: {SPOTIFY_DARK_GRAY} !important;
            font-size: 0.95rem !important;
        }}

        /* All div text should be larger and black */
        div, span {{
            color: {SPOTIFY_BLACK} !important;
            font-size: 1.05rem !important;
        }}

        /* Force all select dropdowns to have white background */
        .stSelectbox, .stSelectbox * {{
            background-color: {SPOTIFY_WHITE} !important;
            color: {SPOTIFY_BLACK} !important;
        }}

        /* Override any inherited styles */
        [class*="select"] {{
            background-color: {SPOTIFY_WHITE} !important;
            color: {SPOTIFY_BLACK} !important;
        }}

        /* Dropdown container */
        [class*="dropdown"] {{
            background-color: {SPOTIFY_WHITE} !important;
            color: {SPOTIFY_BLACK} !important;
        }}

        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 10px;
        }}

        ::-webkit-scrollbar-track {{
            background: {SPOTIFY_LIGHT_GRAY};
        }}

        ::-webkit-scrollbar-thumb {{
            background: {SPOTIFY_GREEN};
            border-radius: 5px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: #1ed760;
        }}
        </style>
    """, unsafe_allow_html=True)


# API Helper Functions
def search_api(endpoint: str, query: str) -> List[Dict[str, str]]:
    """Generic search function for API endpoints - now using centralized api_service."""
    # Map endpoint to api_service method
    if 'artists' in endpoint:
        result = api_service.search_artists(query)
    elif 'interests' in endpoint:
        result = api_service.search_interests(query)
    elif 'geo' in endpoint:
        result = api_service.search_geo(query)
    elif 'playlists' in endpoint:
        result = api_service.search_playlists(query)
    elif 'podcast-topics' in endpoint:
        result = api_service.search_podcast_topics(query)
    else:
        return []

    if result.get("success"):
        return result.get("results", [])
    return []


def get_sensitive_topics() -> List[Dict[str, str]]:
    """Fetch sensitive topics from API."""
    result = api_service.get_sensitive_topics()
    if result.get("success"):
        return result.get("sensitive_topics", [])

    # Fallback data
    return [
        {"id": "alcohol", "name": "Alcohol"},
        {"id": "gambling", "name": "Gambling"},
        {"id": "tobacco", "name": "Tobacco"},
        {"id": "weapons", "name": "Weapons"}
    ]


def get_bid_estimate(form_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Get bid estimate from API."""
    result = api_service.get_estimate_bid(form_data)
    if result.get("success"):
        return result
    return None


def get_insights(form_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Get media plan insights from API."""
    result = api_service.get_media_plan_insights(form_data)
    if result.get("success"):
        return result.get("insights")
    return None


def generate_report(form_data: Dict[str, Any]) -> Optional[bytes]:
    """Generate report from API."""
    return api_service.generate_media_plan_report(form_data)


def init_session_state():
    """Initialize all session state variables."""
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = 0

    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            'campaign_name': '',
            'campaign_objective': 'REACH',
            'countries': 'US',
            'artist_ids': [],
            'interest_ids': [],
            'geo_ids': [],
            'playlist_ids': [],
            'podcast_episode_topic_ids': [],
            'language': 'en',
            'devices': ['IOS', 'ANDROID', 'DESKTOP'],
            'age_ranges': ['all'],
            'age_min': 13,
            'age_max': 65,
            'gender': ['MALE', 'FEMALE', 'NON_BINARY'],
            'interests': [],
            'music_genres': [],
            'playlist_themes': [],
            'podcast_topics': [],
            'asset_formats': 'AUDIO',
            'placement_types': ['MUSIC', 'PODCAST'],
            'sensitive_topic_filter_type': 'global',
            'sensitive_topic_global_filter': 'standard',
            'sensitive_topic_filters': [],
            'frequency_caps': {
                'day': {'max_impressions': 5, 'frequency_period': 1},
                'week': {'max_impressions': 35, 'frequency_period': 1},
                'month': {'max_impressions': 50, 'frequency_period': 1}
            },
            'budget_type': 'LIFETIME',
            'micro_amount': None,
            'start_date': '',
            'end_date': '',
            'bid_strategy': 'MAX_BID',
            'bid_micro_amount': None
        }

    if 'bid_estimate' not in st.session_state:
        st.session_state.bid_estimate = None

    if 'insights' not in st.session_state:
        st.session_state.insights = None

    if 'sensitive_topics' not in st.session_state:
        st.session_state.sensitive_topics = get_sensitive_topics()

    if 'search_results' not in st.session_state:
        st.session_state.search_results = {}


def validate_current_tab() -> bool:
    """Validate if current tab has required fields filled."""
    current_tab = st.session_state.current_tab
    form_data = st.session_state.form_data

    if current_tab == 0:  # Objective
        return bool(form_data['campaign_name'] and form_data['campaign_objective'])
    elif current_tab == 1:  # Targeting
        return bool(form_data['countries'] and form_data['devices'])
    elif current_tab == 2:  # Format
        return bool(form_data['asset_formats'] and form_data['placement_types'])
    elif current_tab == 3:  # Delivery
        return True  # No required fields
    elif current_tab == 4:  # Budget
        return bool(form_data['budget_type'] and form_data['start_date'] and form_data['end_date'])
    elif current_tab == 5:  # Bidding
        return bool(st.session_state.bid_estimate)

    return True


def all_tabs_completed() -> bool:
    """Check if all required fields across all tabs are filled."""
    form_data = st.session_state.form_data
    return all([
        form_data['campaign_name'],
        form_data['campaign_objective'],
        form_data['countries'],
        form_data['devices'],
        form_data['asset_formats'],
        form_data['placement_types'],
        form_data['budget_type'],
        form_data['start_date'],
        form_data['end_date'],
        st.session_state.bid_estimate is not None,
        form_data['bid_micro_amount'] is not None
    ])


def render_progress_bar():
    """Render custom progress bar."""
    current = st.session_state.current_tab

    # Build progress steps HTML
    steps_html = ""
    for i, tab_name in enumerate(TAB_NAMES):
        circle_class = "progress-step-circle"
        label_class = "progress-step-label"

        if i < current:
            circle_class += " completed"
        elif i == current:
            circle_class += " active"
            label_class += " active"

        steps_html += f'<div class="progress-step"><div class="{circle_class}">{i + 1}</div><div class="{label_class}">{tab_name}</div></div>'

    progress_html = f'<div class="progress-container"><div class="progress-steps">{steps_html}</div></div>'
    st.markdown(progress_html, unsafe_allow_html=True)


def next_tab():
    """Navigate to next tab."""
    if validate_current_tab():
        if st.session_state.current_tab < len(TAB_NAMES) - 1:
            st.session_state.current_tab += 1
            # Add flag to scroll to top after rerun
            st.session_state.scroll_to_top = True
            st.rerun()
    else:
        st.error("Please fill in all required fields before proceeding.")


def previous_tab():
    """Navigate to previous tab."""
    if st.session_state.current_tab > 0:
        st.session_state.current_tab -= 1
        # Add flag to scroll to top after rerun
        st.session_state.scroll_to_top = True
        st.rerun()


def update_form_data(key: str, value: Any):
    """Update form data in session state."""
    st.session_state.form_data[key] = value


def searchable_multiselect(label: str, search_type: str, selected_ids: List[str], key: str):
    """Custom searchable multi-select component."""
    st.markdown(f"### {label}")

    search_query = st.text_input(
        f"Search {label.lower()}",
        key=f"search_{key}",
        placeholder="Type 2-3 letters to search...",
        label_visibility="collapsed"
    )

    if len(search_query) >= 2:
        if f"{search_type}_{search_query}" not in st.session_state.search_results:
            endpoint_map = {
                'artists': '/mediaplan/search/artists',
                'interests': '/mediaplan/search/interests',
                'geo': '/mediaplan/search/geo',
                'playlists': '/mediaplan/search/playlists',
                'podcast-topics': '/mediaplan/search/podcast-topics'
            }
            results = search_api(endpoint_map[search_type], search_query)
            st.session_state.search_results[f"{search_type}_{search_query}"] = results

        results = st.session_state.search_results.get(f"{search_type}_{search_query}", [])

        if results:
            st.caption(f"Found {len(results)} results:")
            for result in results:
                is_selected = result['id'] in selected_ids
                if st.checkbox(result['name'], value=is_selected, key=f"{key}_{result['id']}"):
                    if result['id'] not in selected_ids:
                        selected_ids.append(result['id'])
                else:
                    if result['id'] in selected_ids:
                        selected_ids.remove(result['id'])

    if selected_ids:
        st.success(f"✓ {len(selected_ids)} item(s) selected")

    return selected_ids




st.set_page_config(
    page_title="Spotify Media Plan Builder",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# ---- Scroll to Top Script ----
if 'scroll_to_top' in st.session_state and st.session_state.scroll_to_top:
    components.html(
        """
        <script>
            const mainSection = window.parent.document.querySelector('.main');
            if (mainSection) {
                mainSection.scrollTo({ top: 0, behavior: 'smooth' });
            }
        </script>
        """,
        height=0,
    )
    st.session_state.scroll_to_top = False

st.markdown("""
    <style>
        /* remove default Streamlit padding */
        .block-container {
            padding-top: 1rem !important;
        }

        /* optional - hide Streamlit header/footer */
        header, footer {
            visibility: hidden;
        }

        /* prevent double top margin when scroll script triggers */
        section.main > div:first-child {
            margin-top: 0 !important;
        }
    </style>
""", unsafe_allow_html=True)

def main():
    apply_custom_css()
    init_session_state()

    # Scroll to top PROPERLY when Next/Previous is clicked
    if st.session_state.get('scroll_to_top', False):
        components.html(
            """
            <script>
                window.parent.document.querySelector('section.main').scrollTo(0, 0);
            </script>
            """,
            height=0,
        )
        st.session_state.scroll_to_top = False

    # Header with button on the same line
    col_title, col_button = st.columns([7, 3])

    with col_title:
        st.markdown("""
            <div style="padding: 5px 0 10px 0; margin-top: 0;">
                <h1 style="margin-bottom: 8px; margin-top: 0;">🎵 Spotify Media Plan Builder</h1>
                <p style="font-size: 1.1rem; color: #535353; margin-top: 0;">
                    Create comprehensive media campaigns with advanced targeting and insights
                </p>
            </div>
        """, unsafe_allow_html=True)

    with col_button:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📁 Drafts", type="primary", key="nav_to_drafts", use_container_width=True):
            st.switch_page("pages/mediaplandrafts.py")

    # Progress bar
    render_progress_bar()

    # Main content area
    st.markdown('<div class="content-card">', unsafe_allow_html=True)

    current_tab = st.session_state.current_tab

    # TAB 0: OBJECTIVE
    if current_tab == 0:
        st.markdown("## 📋 Campaign Objective")
        st.markdown("Define your campaign's basic information and primary objective.")
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        campaign_name = st.text_input(
            "Campaign Name *",
            value=st.session_state.form_data['campaign_name'],
            placeholder="Enter a memorable campaign name",
            key="campaign_name_input",
            help="Choose a unique name to identify your campaign"
        )
        update_form_data('campaign_name', campaign_name)

        objective_labels = {obj['value']: obj['label'] for obj in CAMPAIGN_OBJECTIVES}
        campaign_objective = st.selectbox(
            "Campaign Objective *",
            options=[obj['value'] for obj in CAMPAIGN_OBJECTIVES],
            format_func=lambda x: objective_labels[x],
            index=[obj['value'] for obj in CAMPAIGN_OBJECTIVES].index(
                st.session_state.form_data['campaign_objective']
            ),
            key="campaign_objective_input",
            help="Select the primary goal for this campaign"
        )
        update_form_data('campaign_objective', campaign_objective)

        st.markdown('<div class="info-box"><p>💡 Tip: Your campaign objective will guide ad delivery optimization.</p></div>', unsafe_allow_html=True)

    # TAB 1: TARGETING
    elif current_tab == 1:
        st.markdown("## 🎯 Audience Targeting")
        st.markdown("Define who should see your ads with precise demographic and interest targeting.")
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        # Geographic & Language
        st.markdown("### 🌍 Geographic & Language")
        col1, col2 = st.columns(2)

        with col1:
            country_labels = {c['code']: c['name'] for c in COUNTRIES}
            country = st.selectbox(
                "Country *",
                options=[c['code'] for c in COUNTRIES],
                format_func=lambda x: country_labels[x],
                index=[c['code'] for c in COUNTRIES].index(st.session_state.form_data['countries']),
                key="country_input"
            )
            update_form_data('countries', country)

        with col2:
            lang_labels = {l['id']: l['name'] for l in LANGUAGES}
            language = st.selectbox(
                "Language",
                options=[l['id'] for l in LANGUAGES],
                format_func=lambda x: lang_labels[x],
                index=[l['id'] for l in LANGUAGES].index(st.session_state.form_data['language']),
                key="language_input"
            )
            update_form_data('language', language)

        st.markdown("### 📱 Devices *")
        devices = []
        for device in DEVICES:
            if st.checkbox(device['label'], value=device['value'] in st.session_state.form_data['devices'], key=f"device_{device['value']}"):
                devices.append(device['value'])
        update_form_data('devices', devices)

        st.markdown("### 👥 Demographics")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Age Ranges**")
            age_ranges = []
            for age_range in AGE_RANGE_OPTIONS[:5]:  # Show first 5
                if st.checkbox(age_range['label'], value=age_range['value'] in st.session_state.form_data['age_ranges'], key=f"age_{age_range['value']}"):
                    age_ranges.append(age_range['value'])

            with st.expander("Show more age ranges"):
                for age_range in AGE_RANGE_OPTIONS[5:]:
                    if st.checkbox(age_range['label'], value=age_range['value'] in st.session_state.form_data['age_ranges'], key=f"age_{age_range['value']}"):
                        age_ranges.append(age_range['value'])

            update_form_data('age_ranges', age_ranges)

            if age_ranges:
                if 'all' in age_ranges:
                    update_form_data('age_min', 13)
                    update_form_data('age_max', 65)
                else:
                    selected_ranges = [r for r in AGE_RANGE_OPTIONS if r['value'] in age_ranges]
                    if selected_ranges:
                        update_form_data('age_min', min(r['min'] for r in selected_ranges))
                        update_form_data('age_max', max(r['max'] for r in selected_ranges))

        with col2:
            st.markdown("**Gender**")
            genders = []
            for gender_opt in GENDER_OPTIONS:
                if st.checkbox(gender_opt['label'], value=gender_opt['value'] in st.session_state.form_data['gender'], key=f"gender_{gender_opt['value']}"):
                    genders.append(gender_opt['value'])
            update_form_data('gender', genders)

        st.markdown("### 🎨 Interest & Content Targeting")
        st.caption("Search and select specific artists, interests, or locations to target")

        col1, col2, col3 = st.columns(3)

        with col1:
            artist_ids = searchable_multiselect("Artists", "artists", st.session_state.form_data['artist_ids'], "artists")
            update_form_data('artist_ids', artist_ids)

        with col2:
            interest_ids = searchable_multiselect("Interests", "interests", st.session_state.form_data['interest_ids'], "interests")
            update_form_data('interest_ids', interest_ids)

        with col3:
            geo_ids = searchable_multiselect("Geo Targets", "geo", st.session_state.form_data['geo_ids'], "geo")
            update_form_data('geo_ids', geo_ids)

    # TAB 2: FORMAT
    elif current_tab == 2:
        st.markdown("## 🎨 Format and Placement")
        st.markdown("Choose your creative format and where your ads will appear.")
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        st.markdown("### 🎬 Creative Format & Placement")
        col1, col2 = st.columns(2)

        with col1:
            format_labels = {f['value']: f['label'] for f in ASSET_FORMATS}
            asset_format = st.selectbox(
                "Asset Format *",
                options=[f['value'] for f in ASSET_FORMATS],
                format_func=lambda x: format_labels[x],
                index=[f['value'] for f in ASSET_FORMATS].index(st.session_state.form_data['asset_formats']),
                key="asset_format_input"
            )
            update_form_data('asset_formats', asset_format)

        with col2:
            st.markdown("Placement Type *")
            placement_types = []
            for placement in PLACEMENT_TYPES:
                if st.checkbox(placement['label'], value=placement['value'] in st.session_state.form_data['placement_types'], key=f"placement_{placement['value']}"):
                    placement_types.append(placement['value'])
            update_form_data('placement_types', placement_types)

        st.markdown("### 🎵 Music & Content Targeting")

        col1, col2 = st.columns(2)

        with col1:
            with st.expander("🎸 Select Music Genres", expanded=False):
                music_genres = []
                for genre in GENRES:
                    if st.checkbox(genre['name'], value=genre['id'] in st.session_state.form_data['music_genres'], key=f"genre_{genre['id']}"):
                        music_genres.append(genre['id'])
                update_form_data('music_genres', music_genres)

                if music_genres:
                    st.success(f"✓ {len(music_genres)} genre(s) selected")

        with col2:
            with st.expander("📻 Select Playlist Themes", expanded=False):
                playlist_ids = []
                for playlist in PLAYLISTS:
                    if st.checkbox(playlist['name'], value=playlist['id'] in st.session_state.form_data['playlist_ids'], key=f"playlist_{playlist['id']}"):
                        playlist_ids.append(playlist['id'])
                update_form_data('playlist_ids', playlist_ids)

                if playlist_ids:
                    st.success(f"✓ {len(playlist_ids)} playlist(s) selected")

        with st.expander("🎙️ Select Podcast Topics", expanded=False):
            podcast_topic_ids = []
            cols = st.columns(3)
            for idx, topic in enumerate(PODCAST_EPISODE_TOPICS):
                with cols[idx % 3]:
                    if st.checkbox(topic['name'], value=topic['id'] in st.session_state.form_data['podcast_episode_topic_ids'], key=f"podcast_{topic['id']}"):
                        podcast_topic_ids.append(topic['id'])
            update_form_data('podcast_episode_topic_ids', podcast_topic_ids)

            if podcast_topic_ids:
                st.success(f"✓ {len(podcast_topic_ids)} topic(s) selected")

        st.markdown("### 🛡️ Content Safety & Filtering")

        filter_type = st.radio(
            "Filter Configuration",
            options=['global', 'individual'],
            format_func=lambda x: "Global Filter (Apply same level to all)" if x == 'global' else "Individual Filters (Customize per topic)",
            index=0 if st.session_state.form_data['sensitive_topic_filter_type'] == 'global' else 1,
            key="filter_type_input",
            horizontal=True
        )
        update_form_data('sensitive_topic_filter_type', filter_type)

        if filter_type == 'global':
            level_labels = {l['value']: l['label'] for l in SENSITIVE_FILTER_LEVELS}
            global_filter = st.selectbox(
                "Global Filter Level",
                options=[l['value'] for l in SENSITIVE_FILTER_LEVELS],
                format_func=lambda x: level_labels[x],
                index=[l['value'] for l in SENSITIVE_FILTER_LEVELS].index(st.session_state.form_data['sensitive_topic_global_filter']),
                key="global_filter_input"
            )
            update_form_data('sensitive_topic_global_filter', global_filter)
        else:
            with st.expander("Configure Individual Topic Filters", expanded=True):
                sensitive_filters = []
                for topic in st.session_state.sensitive_topics:
                    existing_filter = next((f for f in st.session_state.form_data['sensitive_topic_filters'] if f['topic_id'] == topic['id']), None)

                    col1, col2 = st.columns([3, 2])
                    with col1:
                        enabled = st.checkbox(topic['name'], value=existing_filter is not None, key=f"sensitive_{topic['id']}")

                    with col2:
                        if enabled:
                            level_labels = {l['value']: l['label'] for l in SENSITIVE_FILTER_LEVELS}
                            filter_level = st.selectbox("Level", options=[l['value'] for l in SENSITIVE_FILTER_LEVELS], format_func=lambda x: level_labels[x], index=0, key=f"sensitive_level_{topic['id']}", label_visibility="collapsed")
                            sensitive_filters.append({'topic_id': topic['id'], 'filter_level': filter_level})

                update_form_data('sensitive_topic_filters', sensitive_filters)

    # TAB 3: DELIVERY
    elif current_tab == 3:
        st.markdown("## 📊 Delivery Settings")
        st.markdown("Control how often users see your ads with frequency caps.")
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        st.markdown("### ⏱️ Frequency Caps")
        st.caption("Set the maximum number of times a user can see your ad within each time period")

        col1, col2, col3 = st.columns(3)

        with col1:
            freq_day = st.number_input("Daily Cap", min_value=1, max_value=10, value=st.session_state.form_data['frequency_caps']['day']['max_impressions'], key="freq_day_input", help="Max impressions per user per day (1-10)")
            st.session_state.form_data['frequency_caps']['day']['max_impressions'] = freq_day

        with col2:
            freq_week = st.number_input("Weekly Cap", min_value=1, max_value=50, value=st.session_state.form_data['frequency_caps']['week']['max_impressions'], key="freq_week_input", help="Max impressions per user per week (1-50)")
            st.session_state.form_data['frequency_caps']['week']['max_impressions'] = freq_week

        with col3:
            freq_month = st.number_input("Monthly Cap", min_value=1, max_value=100, value=st.session_state.form_data['frequency_caps']['month']['max_impressions'], key="freq_month_input", help="Max impressions per user per month (1-100)")
            st.session_state.form_data['frequency_caps']['month']['max_impressions'] = freq_month

        st.markdown('<div class="info-box"><p>💡 Default values (5 daily, 35 weekly, 50 monthly) are recommended for optimal reach and frequency balance.</p></div>', unsafe_allow_html=True)

    # TAB 4: BUDGET
    elif current_tab == 4:
        st.markdown("## 💰 Budget and Schedule")
        st.markdown("Set your campaign budget and schedule.")
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            budget_type_labels = {b['value']: b['label'] for b in BUDGET_TYPES}
            budget_type = st.selectbox("Budget Type *", options=[b['value'] for b in BUDGET_TYPES], format_func=lambda x: budget_type_labels[x], index=[b['value'] for b in BUDGET_TYPES].index(st.session_state.form_data['budget_type']), key="budget_type_input")
            update_form_data('budget_type', budget_type)

        with col2:
            bid_strategy_labels = {b['value']: b['label'] for b in BID_STRATEGY_OPTIONS}
            bid_strategy = st.selectbox("Bid Strategy *", options=[b['value'] for b in BID_STRATEGY_OPTIONS], format_func=lambda x: bid_strategy_labels[x], index=[b['value'] for b in BID_STRATEGY_OPTIONS].index(st.session_state.form_data['bid_strategy']), key="bid_strategy_input")
            update_form_data('bid_strategy', bid_strategy)

        st.markdown("### 💵 Budget Amount")
        budget_dollars = st.number_input("Budget Amount (USD) *", min_value=1.0, step=100.0, format="%.2f", key="budget_amount_input", help="Enter your total campaign budget in USD")
        if budget_dollars:
            micro_amount = int(budget_dollars * 1000000)
            update_form_data('micro_amount', micro_amount)
            st.success(f"Budget set: ${budget_dollars:,.2f} USD")

        st.markdown("### 📅 Campaign Schedule")
        col1, col2 = st.columns(2)

        with col1:
            start_date = st.date_input("Start Date *", key="start_date_input", help="When should your campaign begin?")
            if start_date:
                update_form_data('start_date', start_date.strftime('%Y-%m-%d'))

        with col2:
            end_date = st.date_input("End Date *", min_value=start_date if start_date else None, key="end_date_input", help="When should your campaign end?")
            if end_date:
                update_form_data('end_date', end_date.strftime('%Y-%m-%d'))

        if start_date and end_date:
            duration = (end_date - start_date).days
            st.info(f"📊 Campaign Duration: **{duration} days**")

    # TAB 5: BIDDING
    elif current_tab == 5:
        st.markdown("## 💵 Bidding Strategy")
        st.markdown("Get bid estimates and set your maximum bid to optimize campaign performance.")
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        if st.button("🎯 Get Bid Estimate", type="primary", use_container_width=False):
            with st.spinner("Loading bid estimates..."):
                bid_estimate = get_bid_estimate(st.session_state.form_data)
                if bid_estimate:
                    st.session_state.bid_estimate = bid_estimate
                    st.success("✓ Bid estimate loaded successfully!")
                    st.rerun()

        if st.session_state.bid_estimate:
            bid_data = st.session_state.bid_estimate

            st.markdown("### 📊 Recommended Bid Range")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Minimum CPM", f"{bid_data['currency']} {bid_data['bid_estimate_min'] / 1000000:.2f}")

            with col2:
                st.metric("Maximum CPM", f"{bid_data['currency']} {bid_data['bid_estimate_max'] / 1000000:.2f}")

            with col3:
                st.metric("Cost Model", bid_data['cost_model'])

            avg_bid = (bid_data['bid_estimate_min'] + bid_data['bid_estimate_max']) / 2

            st.markdown("### 💰 Set Your Bid Cap")
            bid_cap = st.number_input(
                "Bid cap per 1,000 impressions *",
                min_value=0.0,
                value=avg_bid / 1000000,
                step=0.01,
                format="%.2f",
                key="bid_cap_input",
                help=f"Recommended range: {bid_data['currency']} {bid_data['bid_estimate_min'] / 1000000:.2f} - {bid_data['currency']} {bid_data['bid_estimate_max'] / 1000000:.2f}"
            )

            if bid_cap:
                bid_micro_amount = int(bid_cap * 1000000)
                update_form_data('bid_micro_amount', bid_micro_amount)
                st.success(f"✓ Bid cap set to {bid_data['currency']} {bid_cap:.2f}")

        else:
            st.markdown('<div class="info-box"><p>📌 Click "Get Bid Estimate" to receive recommended bid ranges based on your campaign settings.</p></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Navigation buttons
    st.markdown('<div class="nav-buttons">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if current_tab > 0:
            if st.button("← Previous", key="prev_button", use_container_width=True):
                previous_tab()
                st.session_state.scroll_to_top = True


    with col3:
        if current_tab < len(TAB_NAMES) - 1:
            if st.button("Next →", key="next_button", type="primary", use_container_width=True):
                next_tab()
                st.session_state.scroll_to_top = True

    st.markdown('</div>', unsafe_allow_html=True)

    # Show final buttons only after all tabs are completed
    if all_tabs_completed():
        st.markdown("---")
        st.markdown("### 🎉 Ready to Generate!")

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            if st.button("🚀 Generate Insights", type="primary", use_container_width=True):
                with st.spinner("Generating campaign insights..."):
                    insights = get_insights(st.session_state.form_data)
                    if insights:
                        st.session_state.insights = insights
                        st.success("✓ Insights generated successfully!")
                        st.rerun()

        # Display Insights
        if st.session_state.insights:
            st.markdown("---")
            st.markdown("## 📊 Campaign Insights")

            insights = st.session_state.insights

            if 'likely_to_deliver_budget' in insights:
                likelihood = "High" if insights['likely_to_deliver_budget'] else "Moderate"
                if insights['likely_to_deliver_budget']:
                    st.success(f"✅ Budget Delivery Likelihood: **{likelihood}**")
                else:
                    st.warning(f"⚠️ Budget Delivery Likelihood: **{likelihood}**")

            if 'audience_estimates' in insights and insights['audience_estimates']:
                st.markdown("### 👥 Audience Forecast by Period")

                cols = st.columns(len(insights['audience_estimates']))

                for idx, forecast in enumerate(insights['audience_estimates']):
                    with cols[idx]:
                        st.markdown(f"**{forecast['forecast_type']}**")
                        st.metric("Impressions", f"{forecast['estimated_impressions_min']/1000:.0f}K - {forecast['estimated_impressions_max']/1000:.0f}K")
                        st.metric("Reach", f"{forecast['estimated_reach_min']/1000:.0f}K - {forecast['estimated_reach_max']/1000:.0f}K")
                        st.metric("Frequency", f"{forecast['estimated_frequency_min']:.1f} - {forecast['estimated_frequency_max']:.1f}")

                        if forecast.get('estimated_cpm_min') and forecast.get('estimated_cpm_max'):
                            st.metric("CPM", f"${forecast['estimated_cpm_min']/1000000:.2f} - ${forecast['estimated_cpm_max']/1000000:.2f}")

                        if forecast.get('projected_unique_users'):
                            st.metric("Projected Users", f"{forecast['projected_unique_users']/1000:.0f}K")

                        if forecast.get('recommendation_results'):
                            rec = forecast['recommendation_results']
                            st.metric("Recommended Budget", f"${rec['budget']['micro_amount']/1000000:.0f}")

            if 'bid_estimates' in insights:
                st.markdown("### 💵 Bid Estimates")
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Min CPM", f"${insights['bid_estimates']['bid_estimate_min']/1000000:.2f}")

                with col2:
                    st.metric("Max CPM", f"${insights['bid_estimates']['bid_estimate_max']/1000000:.2f}")

                with col3:
                    st.metric("Cost Model", insights['bid_estimates']['cost_model'])


            # Generate Draft Button
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])

            with col2:
                if st.button("📝 Generate Draft", type="primary", use_container_width=True):
                    # Directly call the create draft section inline (no popup)
                    from components.create_draft_modal import create_draft_modal
                    create_draft_modal()




if __name__ == "__main__":
    main()
