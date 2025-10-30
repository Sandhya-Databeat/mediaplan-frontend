import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import json

# Add parent directory to path to import api_service
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from api_service import api_service
from components.edit_drafts_modal import edit_draft_modal
from components.finalised_plan_modal import finalized_plans_modal

# Page configuration
st.set_page_config(
    page_title="Media Plan Drafts",
    page_icon="📁",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f9fafb;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 500;
    }
    .spotify-button {
        background-color: #1DB954 !important;
        color: white !important;
    }
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .stat-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
    }
    .draft-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        margin-bottom: 0.75rem;
        transition: all 0.2s;
    }
    .draft-card:hover {
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        background-color: #f9fafb;
    }
    .draft-card-selected {
        border-color: #1DB954;
        background-color: #1DB9541a;
    }
    .campaign-button {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        cursor: pointer;
        transition: all 0.2s;
    }
    .campaign-button:hover {
        border-color: #d1d5db;
        background-color: #f9fafb;
    }
    .campaign-button-active {
        border-color: #1DB954;
        background-color: #1DB9541a;
    }
    .format-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    .format-audio {
        background-color: #dbeafe;
        color: #1e40af;
    }
    .format-video {
        background-color: #f3e8ff;
        color: #6b21a8;
    }
    .format-display {
        background-color: #d1fae5;
        color: #065f46;
    }
    .stSelectbox > div > div {
        background-color: white !important;
        color: black !important;
        border: 2px solid #191414 !important;
        border-radius: 8px !important;
    }
    .stSelectbox > div > div > div {
        color: black !important;
        background-color: white !important;
    }
    [data-baseweb="select"] {
        background-color: white !important;
        color: black !important;
        border: 2px solid #191414 !important;
        border-radius: 8px !important;
    }
    [data-baseweb="select"] > div {
        background-color: white !important;
        color: black !important;
        border: 2px solid #191414 !important;
        border-radius: 8px !important;
    }
    [data-baseweb="select"] input {
        color: black !important;
        background-color: white !important;
    }
    [data-baseweb="select"] svg {
        color: black !important;
    }
    div[data-baseweb="popover"] {
        background-color: white !important;
    }
    div[role="listbox"] {
        background-color: white !important;
    }
    div[role="option"] {
        background-color: white !important;
        color: black !important;
    }
    div[role="option"]:hover {
        background-color: #f3f4f6 !important;
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)


# Session state initialization
if 'selected_drafts' not in st.session_state:
    st.session_state.selected_drafts = {}
if 'active_campaign' not in st.session_state:
    st.session_state.active_campaign = ""
if 'active_budget' not in st.session_state:
    st.session_state.active_budget = ""
if 'show_finalized_modal' not in st.session_state:
    st.session_state.show_finalized_modal = False
if 'editing_draft' not in st.session_state:
    st.session_state.editing_draft = None
if 'pending_finalize' not in st.session_state:
    st.session_state.pending_finalize = False
if 'pending_finalize_drafts' not in st.session_state:
    st.session_state.pending_finalize_drafts = {}

# Helper Functions
def transform_drafts_data(raw_drafts: Dict) -> Dict:
    """Transform draft data into campaign -> budget -> format structure"""
    transformed_drafts = {}

    if not raw_drafts:
        return transformed_drafts

    keys = list(raw_drafts.keys())
    if not keys:
        return transformed_drafts

    first_key = keys[0]
    first_value = raw_drafts[first_key]

    # Check if data is already in correct format
    if isinstance(first_value, dict):
        inner_keys = list(first_value.keys())
        is_already_correct = any(
            isinstance(first_value.get(key), dict) and
            any(isinstance(v, list) for v in first_value.get(key, {}).values())
            for key in inner_keys
        )

        if is_already_correct:
            return raw_drafts

        # Transform from budget-keyed to campaign-keyed
        for budget_level, budget_data in raw_drafts.items():
            if isinstance(budget_data, dict):
                for asset_format, drafts in budget_data.items():
                    if isinstance(drafts, list):
                        for draft in drafts:
                            campaign_name = draft.get('campaign_name', 'Unknown Campaign')
                            budget_name = draft.get('budget_name') or (
                                '5k Budget' if draft.get('budget_level') == '5k' else
                                '3k Budget' if draft.get('budget_level') == '3k' else
                                f"{budget_level} Budget"
                            )

                            if campaign_name not in transformed_drafts:
                                transformed_drafts[campaign_name] = {}
                            if budget_name not in transformed_drafts[campaign_name]:
                                transformed_drafts[campaign_name][budget_name] = {}
                            if asset_format not in transformed_drafts[campaign_name][budget_name]:
                                transformed_drafts[campaign_name][budget_name][asset_format] = []

                            transformed_drafts[campaign_name][budget_name][asset_format].append(draft)

    return transformed_drafts

def get_asset_format_icon(format_type: str) -> str:
    """Get emoji icon for asset format"""
    icons = {
        "AUDIO": "🎵",
        "VIDEO": "🎥",
        "DISPLAY": "🖥️"
    }
    return icons.get(format_type, "📄")

def get_asset_format_color(format_type: str) -> str:
    """Get CSS class for asset format"""
    colors = {
        "AUDIO": "format-audio",
        "VIDEO": "format-video",
        "DISPLAY": "format-display"
    }
    return colors.get(format_type, "")

def format_date(date_string: str) -> str:
    """Format date string to readable format"""
    try:
        date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return date_obj.strftime("%Y-%m-%d")
    except:
        return date_string

def get_total_drafts_count(drafts_data: Dict) -> int:
    """Calculate total number of drafts"""
    total = 0
    for campaign_data in drafts_data.values():
        for budget_data in campaign_data.values():
            for format_drafts in budget_data.values():
                if isinstance(format_drafts, list):
                    total += len(format_drafts)
    return total

def get_campaign_description(campaign_data: Dict) -> str:
    """Get description for campaign"""
    budgets = list(campaign_data.keys())
    total_drafts = 0
    for budget_data in campaign_data.values():
        for format_drafts in budget_data.values():
            if isinstance(format_drafts, list):
                total_drafts += len(format_drafts)
    return f"{len(budgets)} budget{'s' if len(budgets) != 1 else ''}, {total_drafts} total draft{'s' if total_drafts != 1 else ''}"

def get_budget_description(budget_data: Dict) -> str:
    """Get description for budget"""
    total_drafts = sum(len(drafts) for drafts in budget_data.values() if isinstance(drafts, list))
    formats = list(budget_data.keys())
    return f"{total_drafts} draft{'s' if total_drafts != 1 else ''} across {len(formats)} format{'s' if len(formats) != 1 else ''}"

# Main Application
def main():
    # CRITICAL: Check for pending finalize action BEFORE any other UI/API calls
    if 'pending_finalize' in st.session_state and st.session_state.pending_finalize:
        drafts_to_finalize = st.session_state.get('pending_finalize_drafts', {})
        st.session_state.pending_finalize = False

        if drafts_to_finalize:
            st.write("🚀 EXECUTING FINALIZE ACTION...")
            st.write(f"📋 Drafts: {drafts_to_finalize}")
            print(f"===== FINALIZE EXECUTING - Drafts: {drafts_to_finalize} =====")

            try:
                response = api_service.finalize_drafts(drafts_to_finalize)
                st.write(f"📥 Response: {response}")
                print(f"===== FINALIZE RESPONSE: {response} =====")

                if response.get("success"):
                    st.success(f"✅ Successfully finalized {response.get('total_finalized', 0)} media plans!")
                    st.session_state.selected_drafts = {}
                    st.session_state.pending_finalize_drafts = {}
                    st.balloons()
                    import time
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(f"❌ Failed: {response.get('message', 'Unknown error')}")
            except Exception as e:
                st.error(f"❌ Exception: {str(e)}")
                print(f"===== FINALIZE ERROR: {e} =====")

            st.stop()  # Stop execution here to show results

    # Header
    col1, col2 = st.columns([1, 10])
    with col1:
        if st.button("← Back", key="back_button"):
            st.switch_page("media_plan_form_streamlit.py")
    with col2:
        st.title("📁 Media Plan Drafts")
        st.caption("Manage and organize your drafts by campaign, budget and format")

    st.markdown("---")

    # Load data
    with st.spinner("Loading drafts..."):
        drafts_response = api_service.list_drafts()
        stats_response = api_service.get_draft_stats()

    if not drafts_response.get("success", False):
        st.error("Failed to load drafts")
        return

    raw_drafts = drafts_response.get("drafts", {})
    drafts_data = transform_drafts_data(raw_drafts)
    stats = stats_response.get("stats", {}) if stats_response.get("success") else {}

    # Statistics Section
    if stats:
        st.subheader("📊 Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <h2 style="color: #2563eb; margin: 0;">📄 {stats.get('total_drafts', 0)}</h2>
                <p style="color: #6b7280; margin: 0.5rem 0 0 0;">Total Drafts</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <h2 style="color: #16a34a; margin: 0;">💰 {len(stats.get('by_budget', {}))}</h2>
                <p style="color: #6b7280; margin: 0.5rem 0 0 0;">Budget Levels</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <h2 style="color: #9333ea; margin: 0;">⚙️ {stats.get('by_status', {}).get('draft', 0)}</h2>
                <p style="color: #6b7280; margin: 0.5rem 0 0 0;">Draft Status</p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <h2 style="color: #1DB954; margin: 0;">✅ {stats.get('by_status', {}).get('finalized', 0)}</h2>
                <p style="color: #6b7280; margin: 0.5rem 0 0 0;">Finalized</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

    campaigns = list(drafts_data.keys())
    total_drafts = get_total_drafts_count(drafts_data)

    # Action buttons in header
    col1, col2, col3 = st.columns([3, 1, 1])
    with col2:
        if st.button("👁️ View Finalized Plans", use_container_width=True):
            st.session_state.show_finalized_modal = True

            
    st.write("DEBUG - selected_drafts:", st.session_state.selected_drafts)
    st.write("DEBUG - API Base URL:", api_service.base_url)

    with col3:
        if len(st.session_state.selected_drafts) > 0:
            if st.button(
                f"✅ Finalize Selected ({len(st.session_state.selected_drafts)})",
                use_container_width=True,
                type="primary",
                key="finalize_header"
            ):
                # Set pending finalize flag and store drafts
                st.session_state.pending_finalize = True
                st.session_state.pending_finalize_drafts = st.session_state.selected_drafts.copy()
                print(f"===== BUTTON CLICKED - Setting pending_finalize flag =====")
                print(f"===== Drafts stored: {st.session_state.pending_finalize_drafts} =====")
                st.rerun()


    if not campaigns:
        st.info("📁 No Drafts Found")
        st.write("Create your first media plan draft by generating insights and clicking 'Create Draft'")
        if st.button("Create Media Plan", type="primary"):
            st.switch_page("media_plan_form_streamlit.py")
        return

    # Campaign Selector
    st.subheader("🎯 Select Campaign")
    st.caption(f"{len(campaigns)} campaign{'s' if len(campaigns) != 1 else ''} with {total_drafts} total draft{'s' if total_drafts != 1 else ''}")

    # Initialize active campaign if not set
    if not st.session_state.active_campaign and campaigns:
        st.session_state.active_campaign = campaigns[0]
        budgets = list(drafts_data[campaigns[0]].keys())
        if budgets:
            st.session_state.active_budget = budgets[0]

    # Display campaigns as a dropdown for better UX
    campaign_options = {campaign: get_campaign_description(drafts_data[campaign]) for campaign in campaigns}
    selected_campaign = st.selectbox(
        "Choose a campaign",
        options=campaigns,
        format_func=lambda x: f"{x} - {campaign_options[x]}",
        index=campaigns.index(st.session_state.active_campaign) if st.session_state.active_campaign in campaigns else 0,
        key="campaign_selector"
    )

    if selected_campaign != st.session_state.active_campaign:
        st.session_state.active_campaign = selected_campaign
        budgets = list(drafts_data[selected_campaign].keys())
        if budgets:
            st.session_state.active_budget = budgets[0]
        st.rerun()

    st.markdown("---")

    # Budget Selector
    if st.session_state.active_campaign and st.session_state.active_campaign in drafts_data:
        campaign_data = drafts_data[st.session_state.active_campaign]
        budgets = list(campaign_data.keys())

        st.subheader(f"💰 Select Budget for {st.session_state.active_campaign}")
        st.caption("Choose a budget to view and manage your drafts")

        # Budget selection with columns
        cols = st.columns(min(len(budgets), 6))
        for idx, budget_name in enumerate(budgets):
            with cols[idx % 6]:
                budget_data = campaign_data[budget_name]
                total_drafts_budget = sum(len(drafts) for drafts in budget_data.values() if isinstance(drafts, list))

                is_active = st.session_state.active_budget == budget_name
                button_type = "primary" if is_active else "secondary"

                if st.button(
                    f"{budget_name}\n{total_drafts_budget} draft{'s' if total_drafts_budget != 1 else ''}",
                    key=f"budget_{budget_name}",
                    use_container_width=True,
                    type=button_type
                ):
                    st.session_state.active_budget = budget_name
                    st.rerun()

        st.markdown("---")

        # Display Selected Budget Content
        if st.session_state.active_budget and st.session_state.active_budget in campaign_data:
            budget_data = campaign_data[st.session_state.active_budget]

            st.subheader(f"📋 {st.session_state.active_budget} - {st.session_state.active_campaign}")
            st.caption(get_budget_description(budget_data))

            # Finalize button at top of content
            if len(st.session_state.selected_drafts) > 0:
                if st.button(
                    f"✅ Finalize ({len(st.session_state.selected_drafts)})",
                    type="primary",
                    key="finalize_top"
                ):
                    # Set pending finalize flag and store drafts
                    st.session_state.pending_finalize = True
                    st.session_state.pending_finalize_drafts = st.session_state.selected_drafts.copy()
                    print(f"===== BUTTON CLICKED (TOP) - Setting pending_finalize flag =====")
                    print(f"===== Drafts stored: {st.session_state.pending_finalize_drafts} =====")
                    st.rerun()

            # Display drafts by asset format
            format_cols = st.columns(min(len(budget_data), 3))

            for idx, (asset_format, drafts) in enumerate(budget_data.items()):
                with format_cols[idx % 3]:
                    # Format header
                    icon = get_asset_format_icon(asset_format)
                    st.markdown(f"""
                    <div style="margin-bottom: 1rem;">
                        <h3>{icon} {asset_format}</h3>
                        <p style="color: #6b7280; margin: 0;">{len(drafts)} draft{'s' if len(drafts) != 1 else ''}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    # Draft cards
                    for draft in drafts:
                        draft_id = draft['id']
                        key = f"{st.session_state.active_budget}:{asset_format}"
                        is_selected = st.session_state.selected_drafts.get(key) == draft_id

                        with st.container():
                            st.markdown(f"""
                            <div class="draft-card {'draft-card-selected' if is_selected else ''}">
                                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 0.5rem;">
                                    <div>
                                        <h4 style="margin: 0;">{draft.get('budget_name', 'N/A')}</h4>
                                        <p style="color: #6b7280; margin: 0.25rem 0;">{draft.get('form_data', {}).get('campaign_objective', 'No objective')}</p>
                                    </div>
                                    <span class="format-badge">{draft.get('status', 'draft')}</span>
                                </div>
                            """, unsafe_allow_html=True)

                            # Key metrics
                            if draft.get('insights', {}).get('audience_estimates'):
                                estimates = draft['insights']['audience_estimates'][0]
                                reach_min = estimates.get('estimated_reach_min', 0) / 1000
                                reach_max = estimates.get('estimated_reach_max', 0) / 1000

                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("Est. Reach", f"{reach_min:.0f}K - {reach_max:.0f}K")
                                with col2:
                                    st.metric("Created", format_date(draft.get('created_at', '')))

                            # Actions
                            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                            with col1:
                                if st.checkbox("Select for finalization", key=f"select_{draft_id}", value=is_selected):
                                    st.session_state.selected_drafts[key] = draft_id
                                else:
                                    if key in st.session_state.selected_drafts and st.session_state.selected_drafts[key] == draft_id:
                                        del st.session_state.selected_drafts[key]

                            with col2:
                                if st.button("✏️", key=f"edit_{draft_id}", help="Edit draft"):
                                    st.session_state.editing_draft = draft
                                    st.rerun()

                            with col3:
                                if st.button("🗑️", key=f"delete_{draft_id}", help="Delete draft"):
                                    response = api_service.delete_draft(draft_id)
                                    if response.get("success"):
                                        st.success("Draft deleted successfully")
                                        st.rerun()

                            st.markdown("</div>", unsafe_allow_html=True)

    # Finalized Plans Modal
    if st.session_state.show_finalized_modal:
        st.markdown("---")
        with st.container():
            def close_finalized():
                st.session_state.show_finalized_modal = False

            finalized_plans_modal(api_service, close_finalized)

    # Edit Draft Modal
    if st.session_state.editing_draft:
        st.markdown("---")
        with st.container():
            def close_edit():
                st.session_state.editing_draft = None

            edit_draft_modal(st.session_state.editing_draft, api_service, close_edit)

if __name__ == "__main__":
    main()
