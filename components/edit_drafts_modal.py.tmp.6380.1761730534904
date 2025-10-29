import streamlit as st
from typing import Dict, Any, List
from datetime import datetime

# Campaign objectives
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

GENDER_OPTIONS = [
    {"value": "MALE", "label": "Male"},
    {"value": "FEMALE", "label": "Female"},
    {"value": "NON_BINARY", "label": "Non-Binary"}
]

BID_STRATEGY_OPTIONS = [
    {"value": "COST_PER_RESULT", "label": "Cost Per Result"},
    {"value": "MAX_BID", "label": "Max Bid"}
]

PLACEMENT_TYPES = [
    {"value": "MUSIC", "label": "Music"},
    {"value": "PODCAST", "label": "Podcast"}
]


def edit_draft_modal(draft: Dict[str, Any], api_service, on_close_callback):
    """
    Render the edit draft modal in Streamlit.
    Allows editing all draft fields except budget level and asset format (which are read-only).
    """

    st.markdown("### Edit Draft")
    st.markdown("**Budget Level and Asset Format are locked and cannot be changed**")

    # Display read-only information
    st.markdown("---")
    st.markdown("#### Draft Information (Read-only)")

    col1, col2 = st.columns(2)
    with col1:
        budget_level = draft.get('budget_level', 'N/A')
        if isinstance(budget_level, int):
            budget_display = f"${budget_level / 1000000:.0f}k"
        else:
            budget_display = budget_level
        st.info(f"**Budget Level:** {budget_display}")

    with col2:
        asset_format = draft.get('asset_format', 'N/A')
        st.info(f"**Asset Format:** {asset_format}")

    st.markdown("---")

    # Initialize form data from draft
    if 'edit_form_data' not in st.session_state:
        st.session_state.edit_form_data = draft.get('form_data', {}).copy()

    form_data = st.session_state.edit_form_data

    # Tabs for organized editing
    tab1, tab2, tab3, tab4 = st.tabs(["Basic Info", "Targeting", "Delivery", "Schedule"])

    # TAB 1: Basic Information
    with tab1:
        st.markdown("#### Campaign Details")

        campaign_name = st.text_input(
            "Campaign Name *",
            value=form_data.get('campaign_name', ''),
            key="edit_campaign_name"
        )
        form_data['campaign_name'] = campaign_name

        objective_labels = {obj['value']: obj['label'] for obj in CAMPAIGN_OBJECTIVES}
        current_objective = form_data.get('campaign_objective', 'REACH')
        objective_index = [obj['value'] for obj in CAMPAIGN_OBJECTIVES].index(current_objective) if current_objective in [obj['value'] for obj in CAMPAIGN_OBJECTIVES] else 0

        campaign_objective = st.selectbox(
            "Campaign Objective *",
            options=[obj['value'] for obj in CAMPAIGN_OBJECTIVES],
            format_func=lambda x: objective_labels[x],
            index=objective_index,
            key="edit_campaign_objective"
        )
        form_data['campaign_objective'] = campaign_objective

        language = st.text_input(
            "Language",
            value=form_data.get('language', 'en'),
            key="edit_language",
            help="e.g., en, es, fr"
        )
        form_data['language'] = language

        bid_strategy_labels = {b['value']: b['label'] for b in BID_STRATEGY_OPTIONS}
        current_bid = form_data.get('bid_strategy', 'MAX_BID')
        bid_index = [b['value'] for b in BID_STRATEGY_OPTIONS].index(current_bid) if current_bid in [b['value'] for b in BID_STRATEGY_OPTIONS] else 0

        bid_strategy = st.selectbox(
            "Bid Strategy",
            options=[b['value'] for b in BID_STRATEGY_OPTIONS],
            format_func=lambda x: bid_strategy_labels[x],
            index=bid_index,
            key="edit_bid_strategy"
        )
        form_data['bid_strategy'] = bid_strategy

    # TAB 2: Targeting
    with tab2:
        st.markdown("#### Geographic & Device Targeting")

        # Countries
        country_labels = {c['code']: c['name'] for c in COUNTRIES}
        current_country = form_data.get('countries', 'US')
        if isinstance(current_country, list):
            current_country = current_country[0] if current_country else 'US'
        country_index = [c['code'] for c in COUNTRIES].index(current_country) if current_country in [c['code'] for c in COUNTRIES] else 0

        selected_country = st.selectbox(
            "Country *",
            options=[c['code'] for c in COUNTRIES],
            format_func=lambda x: country_labels[x],
            index=country_index,
            key="edit_country"
        )
        form_data['countries'] = selected_country

        st.markdown("**Devices **")
        current_devices = form_data.get('devices', ['DESKTOP'])
        if not isinstance(current_devices, list):
            current_devices = [current_devices]

        selected_devices = []
        cols = st.columns(3)
        for idx, device in enumerate(DEVICES):
            with cols[idx]:
                if st.checkbox(
                    device['label'],
                    value=device['value'] in current_devices,
                    key=f"edit_device_{device['value']}"
                ):
                    selected_devices.append(device['value'])
        form_data['devices'] = selected_devices

        st.markdown("#### Demographics")

        st.markdown("**Gender**")
        current_gender = form_data.get('gender', ['MALE', 'FEMALE', 'NON_BINARY'])
        if not isinstance(current_gender, list):
            current_gender = [current_gender]

        selected_gender = []
        cols = st.columns(3)
        for idx, gender in enumerate(GENDER_OPTIONS):
            with cols[idx]:
                if st.checkbox(
                    gender['label'],
                    value=gender['value'] in current_gender,
                    key=f"edit_gender_{gender['value']}"
                ):
                    selected_gender.append(gender['value'])
        form_data['gender'] = selected_gender

        st.markdown("**Placement Types**")
        current_placements = form_data.get('placement_types', ['MUSIC', 'PODCAST'])
        if not isinstance(current_placements, list):
            current_placements = [current_placements]

        selected_placements = []
        cols = st.columns(2)
        for idx, placement in enumerate(PLACEMENT_TYPES):
            with cols[idx]:
                if st.checkbox(
                    placement['label'],
                    value=placement['value'] in current_placements,
                    key=f"edit_placement_{placement['value']}"
                ):
                    selected_placements.append(placement['value'])
        form_data['placement_types'] = selected_placements

    # TAB 3: Delivery
    with tab3:
        st.markdown("#### Frequency Caps")
        st.caption("Set the maximum number of times a user can see your ad")

        freq_caps = form_data.get('frequency_caps', {
            'day': {'max_impressions': 5, 'frequency_period': 1},
            'week': {'max_impressions': 35, 'frequency_period': 1},
            'month': {'max_impressions': 50, 'frequency_period': 1}
        })

        col1, col2, col3 = st.columns(3)

        with col1:
            freq_day = st.number_input(
                "Daily Cap",
                min_value=1,
                max_value=10,
                value=freq_caps.get('day', {}).get('max_impressions', 5),
                key="edit_freq_day"
            )
            freq_caps['day'] = {'max_impressions': freq_day, 'frequency_period': 1}

        with col2:
            freq_week = st.number_input(
                "Weekly Cap",
                min_value=1,
                max_value=50,
                value=freq_caps.get('week', {}).get('max_impressions', 35),
                key="edit_freq_week"
            )
            freq_caps['week'] = {'max_impressions': freq_week, 'frequency_period': 1}

        with col3:
            freq_month = st.number_input(
                "Monthly Cap",
                min_value=1,
                max_value=100,
                value=freq_caps.get('month', {}).get('max_impressions', 50),
                key="edit_freq_month"
            )
            freq_caps['month'] = {'max_impressions': freq_month, 'frequency_period': 1}

        form_data['frequency_caps'] = freq_caps

    # TAB 4: Schedule
    with tab4:
        st.markdown("#### Campaign Schedule")

        col1, col2 = st.columns(2)

        with col1:
            start_date_str = form_data.get('start_date', '')
            start_date_val = None
            if start_date_str:
                try:
                    start_date_val = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                except:
                    pass

            start_date = st.date_input(
                "Start Date *",
                value=start_date_val,
                key="edit_start_date"
            )
            if start_date:
                form_data['start_date'] = start_date.strftime('%Y-%m-%d')

        with col2:
            end_date_str = form_data.get('end_date', '')
            end_date_val = None
            if end_date_str:
                try:
                    end_date_val = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                except:
                    pass

            end_date = st.date_input(
                "End Date *",
                value=end_date_val,
                min_value=start_date if start_date else None,
                key="edit_end_date"
            )
            if end_date:
                form_data['end_date'] = end_date.strftime('%Y-%m-%d')

        if form_data.get('bid_micro_amount'):
            bid_amount_display = form_data['bid_micro_amount'] / 1000000
            bid_amount = st.number_input(
                "Bid Amount (per 1,000 impressions)",
                min_value=0.0,
                value=bid_amount_display,
                step=0.01,
                format="%.2f",
                key="edit_bid_amount"
            )
            form_data['bid_micro_amount'] = int(bid_amount * 1000000)

    # Update session state
    st.session_state.edit_form_data = form_data

    # Action buttons
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Cancel", use_container_width=True, key="edit_cancel"):
            st.session_state.editing_draft = None
            if 'edit_form_data' in st.session_state:
                del st.session_state.edit_form_data
            on_close_callback()
            st.rerun()

    with col2:
        if st.button("Save Changes", type="primary", use_container_width=True, key="edit_save"):
            # Validation
            errors = []
            if not form_data.get('campaign_name', '').strip():
                errors.append("Campaign name is required")
            if not form_data.get('campaign_objective'):
                errors.append("Campaign objective is required")
            if not form_data.get('start_date'):
                errors.append("Start date is required")
            if not form_data.get('end_date'):
                errors.append("End date is required")
            if not form_data.get('devices'):
                errors.append("At least one device must be selected")

            if errors:
                st.error("Please fix the following errors: " + ", ".join(errors))
            else:
                # Update draft
                updated_data = {
                    'form_data': form_data,
                    'updated_at': datetime.now().isoformat()
                }

                with st.spinner("Updating draft..."):
                    response = api_service.update_draft(draft['id'], updated_data)
                    if response.get('success'):
                        st.success("Draft updated successfully!")
                        st.session_state.editing_draft = None
                        if 'edit_form_data' in st.session_state:
                            del st.session_state.edit_form_data
                        on_close_callback()
                        st.rerun()
                    else:
                        st.error(f"Failed to update draft: {response.get('message', 'Unknown error')}")
