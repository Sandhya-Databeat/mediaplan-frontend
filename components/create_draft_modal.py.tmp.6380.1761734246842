import streamlit as st
from api_service import api_service

def create_draft_modal():
    """Generate Draft section - uses budget from form data"""

    st.markdown("### 📝 Create Media Plan Draft")
    st.markdown("Review your campaign setup and generate a draft below.")
    st.divider()

    # Ensure session data exists
    if "form_data" not in st.session_state or not st.session_state.form_data:
        st.warning("⚠️ Please fill out campaign details before creating a draft.")
        return

    form_data = st.session_state.form_data
    insights = st.session_state.get("insights")

    if not insights:
        st.warning("⚠️ Please generate insights before creating a draft.")
        return

    # Display campaign summary
    st.markdown("#### 📊 Campaign Summary")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(f"**Campaign:** {form_data.get('campaign_name', 'N/A')}")

    with col2:
        budget_amount = form_data.get('micro_amount', 0)
        budget_display = f"${budget_amount / 1000000:.2f}" if budget_amount else "Not Set"
        st.info(f"**Budget:** {budget_display}")

    with col3:
        asset_format = form_data.get('asset_formats', 'AUDIO')
        st.info(f"**Format:** {asset_format}")

    st.markdown("---")

    # Optional preview for debugging
    with st.expander("🔍 Preview Draft Data (Debug)", expanded=False):
        preview_data = {
            "campaign_name": form_data.get('campaign_name'),
            "budget": budget_amount,
            "asset_format": asset_format,
            "has_form_data": bool(form_data),
            "has_insights": bool(insights)
        }
        st.json(preview_data)

    # Create Draft Button
    st.markdown("Once everything looks fine, click below to generate your draft.")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("🚀 Create Draft", type="primary", use_container_width=True, key="create_draft_btn"):
            with st.spinner("Creating your draft..."):
                try:
                    # Get values from form data
                    campaign_name = form_data.get('campaign_name', 'Untitled Campaign')
                    asset_format = form_data.get('asset_formats', 'AUDIO')
                    budget_micro_amount = form_data.get('micro_amount', 100000000)  # Default 100 if not set

                    # Calculate budget level in 'k' format
                    budget_in_k = budget_micro_amount / 1000000
                    budget_level_str = f"{int(budget_in_k)}k"

                    # Prepare form_data with all required fields
                    prepared_form_data = {
                        **form_data,
                        'asset_formats': asset_format,
                        'countries': form_data.get('countries', 'US'),
                        'devices': form_data.get('devices', ['DESKTOP']),
                        'budget_type': form_data.get('budget_type', 'LIFETIME'),
                        'micro_amount': budget_micro_amount,
                        'draft_budget_amount': budget_micro_amount,
                        'draft_budget_name': campaign_name
                    }

                    # Prepare insights with integer bid estimates
                    bid_estimates = insights.get('bid_estimates', {})
                    prepared_insights = {
                        **insights,
                        'bid_estimates': {
                            'bid_estimate_min': int(bid_estimates.get('bid_estimate_min', 0)),
                            'bid_estimate_max': int(bid_estimates.get('bid_estimate_max', 0)),
                            'currency': bid_estimates.get('currency', 'USD'),
                            'cost_model': bid_estimates.get('cost_model', 'CPM')
                        }
                    }

                    # Create draft data matching the API structure
                    draft_data = {
                        'campaign_name': campaign_name,
                        'budget_name': campaign_name,
                        'budget_level': budget_level_str,
                        'asset_format': asset_format,
                        'form_data': prepared_form_data,
                        'insights': prepared_insights
                    }

                    st.info("📤 Sending draft to API...")
                    st.write(f"API Endpoint: {api_service.base_url}/mediaplan/drafts/create")

                    # Call API
                    response = api_service.create_draft(draft_data)

                    st.info("📥 Received response from API")
                    st.write(f"Response type: {type(response)}")
                    st.write(f"Response content: {response}")

                    # Check response
                    if response:
                        if response.get("success"):
                            st.success("✅ Draft created successfully!")
                            st.balloons()
                            st.session_state.draft_created = True
                            # Don't rerun immediately - show success message and buttons
                        else:
                            st.error("❌ Failed to create draft")
                            st.error(f"Message: {response.get('message', 'Unknown error')}")
                            if response.get('errors'):
                                st.error(f"Errors: {response.get('errors')}")
                            if response.get('status_code'):
                                st.error(f"Status Code: {response.get('status_code')}")
                            with st.expander("Full Response Details"):
                                st.json(response)
                    else:
                        st.error("❌ No response received from API")

                except Exception as e:
                    st.error(f"⚠️ Error creating draft: {str(e)}")
                    import traceback
                    with st.expander("🐛 Full Error Details"):
                        st.code(traceback.format_exc())

    # Post creation info
    if st.session_state.get("draft_created"):
        st.markdown("---")
        st.success("🎉 Draft Created Successfully!")
        st.info("Your draft has been saved. You can now:")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📁 View All Drafts", type="primary", use_container_width=True, key="view_drafts_btn"):
                st.session_state.draft_created = False
                st.switch_page("pages/mediaplandrafts.py")
        with col2:
            if st.button("➕ Create Another Draft", use_container_width=True, key="create_another_btn"):
                st.session_state.draft_created = False
                st.rerun()
