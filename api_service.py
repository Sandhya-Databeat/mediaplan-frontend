"""
API Service for Spotify Media Plan Frontend
Python equivalent of api.ts from the React frontend
Centralizes all API communication with the backend
"""

import requests
from typing import Dict, List, Any, Optional, Tuple
import streamlit as st
from io import BytesIO
import json
import os


# API Configuration
try:
    # Try to get from Streamlit secrets (when deployed)
    API_BASE_URL = st.secrets.get("API_BASE_URL", "https://mediaplan-backend.onrender.com")
except Exception:
    # Fallback for local development

    API_BASE_URL = os.getenv("API_BASE_URL", "https://mediaplan-backend.onrender.com")



# Request timeout settings
DEFAULT_TIMEOUT = 30  # 30 seconds
LONG_TIMEOUT = 60     # 60 seconds for report generation


class APIService:
    """
    Centralized API service for all backend communications
    Mirrors the TypeScript ApiService class structure
    """

    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.timeout = DEFAULT_TIMEOUT

    def _handle_error(self, error: Exception, operation: str) -> Dict[str, Any]:
        """Centralized error handling"""
        error_msg = str(error)
        status_code = None

        if hasattr(error, 'response') and error.response is not None:
            status_code = error.response.status_code
            try:
                error_detail = error.response.json().get('detail', error_msg)
                error_msg = error_detail
            except:
                error_msg = error.response.text or error_msg

        # Log to console for debugging
        print(f"API Error during {operation}:")
        print(f"  Status Code: {status_code}")
        print(f"  Error Message: {error_msg}")
        print(f"  Full Error: {error}")

        st.error(f"Error {operation}: {error_msg}")
        if status_code:
            st.error(f"HTTP Status Code: {status_code}")

        return {
            "success": False,
            "message": f"Error {operation}",
            "errors": [error_msg],
            "status_code": status_code
        }

    # ============================================================
    # PREVIEW & REPORT GENERATION
    # ============================================================

    def preview_file(self, file) -> Dict[str, Any]:
        """Preview uploaded file"""
        try:
            files = {'file': file}
            response = requests.post(
                f"{self.base_url}/preview/file",
                files=files,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, "previewing file")

    def get_report_types(self) -> Dict[str, Any]:
        """Get available report types"""
        try:
            response = requests.get(
                f"{self.base_url}/preview/report-types",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, "getting report types")

    def generate_report(self, file, report_type: str, file_id: Optional[str] = None) -> Tuple[Optional[bytes], Optional[str]]:
        """Generate report and return blob + filename"""
        try:
            files = {'file': file}
            data = {}
            if file_id:
                data['file_id'] = file_id

            endpoint_map = {
                'wrap-up-pdf': '/wrapup/pdf',
                'wrap-up-email': '/wrapup/email',
                'mid-campaign-pdf': '/midcampaign/pdf',
                'mid-campaign-email': '/midcampaign/email',
                'campaign-pacing': '/pacing/email',
                'media-plan': '/mediaplan/structure',
            }

            endpoint = endpoint_map.get(report_type)
            if not endpoint:
                raise ValueError(f"Unknown report type: {report_type}")

            response = requests.post(
                f"{self.base_url}{endpoint}",
                files=files,
                data=data,
                timeout=LONG_TIMEOUT
            )
            response.raise_for_status()

            # Extract filename from Content-Disposition header
            content_disposition = response.headers.get('content-disposition', '')
            filename = 'report'
            if 'filename=' in content_disposition:
                filename = content_disposition.split('filename=')[1].replace('"', '').replace("'", "").strip()

            return response.content, filename

        except Exception as e:
            self._handle_error(e, f"generating {report_type} report")
            return None, None

    def download_report(self, file, report_type: str, file_id: Optional[str] = None) -> Tuple[Optional[bytes], Optional[str]]:
        """Download report blob"""
        try:
            files = {'file': file}
            data = {}
            if file_id:
                data['file_id'] = file_id

            download_endpoint_map = {
                'wrap-up-pdf': '/wrapup/pdf',
                'wrap-up-email': '/wrapup/email',
                'mid-campaign-pdf': '/midcampaign/pdf',
                'mid-campaign-email': '/midcampaign/email',
                'campaign-pacing': '/pacing/email',
                'media-plan': '/mediaplan/report',
            }

            endpoint = download_endpoint_map.get(report_type)
            if not endpoint:
                raise ValueError(f"Download not available for report type: {report_type}")

            response = requests.post(
                f"{self.base_url}{endpoint}",
                files=files,
                data=data,
                timeout=LONG_TIMEOUT
            )
            response.raise_for_status()

            # Extract filename
            content_disposition = response.headers.get('content-disposition', '')
            filename = f"{report_type.replace('-', '_')}_report.txt"
            if content_disposition:
                import re
                match = re.search(r'filename[^;=\n]*=(([\'"]).*?\2|[^;\n]*)', content_disposition)
                if match and match.group(1):
                    filename = match.group(1).replace('"', '').replace("'", "")

            return response.content, filename

        except Exception as e:
            self._handle_error(e, f"downloading {report_type} report")
            return None, None

    # ============================================================
    # HEALTH CHECK
    # ============================================================

    def check_health(self) -> Dict[str, Any]:
        """Check API health status"""
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, "checking health")

    # ============================================================
    # MEDIA PLAN INSIGHTS & FORM
    # ============================================================

    def get_media_plan_insights(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get media plan insights from form data"""
        try:
            response = requests.post(
                f"{self.base_url}/mediaplan/insights",
                json=form_data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, "getting media plan insights")

    def generate_media_plan_report(self, form_data: Dict[str, Any]) -> Optional[bytes]:
        """Generate media plan report"""
        try:
            response = requests.post(
                f"{self.base_url}/mediaplan/report",
                json=form_data,
                timeout=LONG_TIMEOUT
            )
            response.raise_for_status()
            return response.content
        except Exception as e:
            self._handle_error(e, "generating media plan report")
            return None

    def get_media_plan_form_schema(self) -> Dict[str, Any]:
        """Get form schema for media plan"""
        try:
            response = requests.get(
                f"{self.base_url}/mediaplan/form-schema",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, "getting form schema")

    def get_estimate_bid(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get bid estimate"""
        try:
            response = requests.post(
                f"{self.base_url}/mediaplan/estimate-bid",
                json=form_data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, "getting bid estimate")

    def get_sensitive_topics(self) -> Dict[str, Any]:
        """Get sensitive topics list"""
        try:
            response = requests.get(
                f"{self.base_url}/mediaplan/sensitive-topics",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, "getting sensitive topics")

    # ============================================================
    # DYNAMIC SEARCH METHODS
    # ============================================================

    def search_artists(self, query: str) -> Dict[str, Any]:
        """Search for artists"""
        try:
            response = requests.get(
                f"{self.base_url}/mediaplan/search/artists",
                params={"q": query},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, f"searching artists for '{query}'")

    def search_interests(self, query: str) -> Dict[str, Any]:
        """Search for interests"""
        try:
            response = requests.get(
                f"{self.base_url}/mediaplan/search/interests",
                params={"q": query},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, f"searching interests for '{query}'")

    def search_geo(self, query: str) -> Dict[str, Any]:
        """Search for geo locations"""
        try:
            response = requests.get(
                f"{self.base_url}/mediaplan/search/geo",
                params={"q": query},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, f"searching geo for '{query}'")

    def search_playlists(self, query: str) -> Dict[str, Any]:
        """Search for playlists"""
        try:
            response = requests.get(
                f"{self.base_url}/mediaplan/search/playlists",
                params={"q": query},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, f"searching playlists for '{query}'")

    def search_podcast_topics(self, query: str) -> Dict[str, Any]:
        """Search for podcast topics"""
        try:
            response = requests.get(
                f"{self.base_url}/mediaplan/search/podcast-topics",
                params={"q": query},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, f"searching podcast topics for '{query}'")

    # ============================================================
    # MEDIA PLAN DRAFTS API METHODS
    # ============================================================

    def create_draft(self, draft_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new media plan draft"""
        try:
            response = requests.post(
                f"{self.base_url}/mediaplan/drafts/create",
                json=draft_data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, "creating draft")

    def list_drafts(self) -> Dict[str, Any]:
        """List all drafts"""
        try:
            response = requests.get(
                f"{self.base_url}/mediaplan/drafts/list",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, "listing drafts")

    def get_draft(self, draft_id: str) -> Dict[str, Any]:
        """Get a specific draft by ID"""
        try:
            response = requests.get(
                f"{self.base_url}/mediaplan/drafts/get/{draft_id}",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, f"getting draft {draft_id}")

    def update_draft(self, draft_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing draft"""
        try:
            response = requests.put(
                f"{self.base_url}/mediaplan/drafts/update/{draft_id}",
                json=updates,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, f"updating draft {draft_id}")

    def delete_draft(self, draft_id: str) -> Dict[str, Any]:
        """Delete a draft"""
        try:
            response = requests.delete(
                f"{self.base_url}/mediaplan/drafts/delete/{draft_id}",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, f"deleting draft {draft_id}")

    def finalize_drafts(self, selected_drafts: Dict[str, str]) -> Dict[str, Any]:
        """Finalize selected drafts"""
        try:
            response = requests.post(
                f"{self.base_url}/mediaplan/drafts/finalize",
                json={"selected_drafts": selected_drafts},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, "finalizing drafts")

    def get_finalized_plans(self) -> Dict[str, Any]:
        """Get all finalized plans"""
        try:
            response = requests.get(
                f"{self.base_url}/mediaplan/drafts/finalized",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, "getting finalized plans")

    def get_draft_stats(self) -> Dict[str, Any]:
        """Get draft statistics"""
        try:
            response = requests.get(
                f"{self.base_url}/mediaplan/drafts/stats",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, "getting draft statistics")

    def get_campaign_suggestions(self, campaign_name: str) -> Dict[str, Any]:
        """Get campaign naming suggestions"""
        try:
            response = requests.get(
                f"{self.base_url}/mediaplan/drafts/campaigns/suggestions/{campaign_name}",
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, "getting campaign suggestions")

    def get_budget_level_suggestions(self, campaign_name: str, budget_input: str = "") -> Dict[str, Any]:
        """Get budget level suggestions for a campaign"""
        try:
            response = requests.get(
                f"{self.base_url}/mediaplan/drafts/budget-suggestions/{campaign_name}",
                params={"budget_input": budget_input},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return self._handle_error(e, "getting budget suggestions")

    def download_finalized_report(self) -> Tuple[Optional[bytes], Optional[str]]:
        """Download Excel report of all finalized drafts"""
        try:
            response = requests.get(
                f"{self.base_url}/drafts/download_report",
                timeout=LONG_TIMEOUT
            )
            response.raise_for_status()

            # Extract filename from Content-Disposition header
            content_disposition = response.headers.get('content-disposition', '')
            filename = 'finalized_media_plans.xlsx'
            if 'filename=' in content_disposition:
                filename = content_disposition.split('filename=')[1].replace('"', '').replace("'", "").strip()

            return response.content, filename

        except Exception as e:
            self._handle_error(e, "downloading finalized report")
            return None, None


# Create singleton instance
api_service = APIService()


# Convenience functions for backward compatibility
def get_insights(form_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Get media plan insights - convenience function"""
    response = api_service.get_media_plan_insights(form_data)
    if response.get("success"):
        return response.get("insights")
    return None


def get_bid_estimate(form_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Get bid estimate - convenience function"""
    response = api_service.get_estimate_bid(form_data)
    if response.get("success"):
        return response
    return None


def generate_report(form_data: Dict[str, Any]) -> Optional[bytes]:
    """Generate media plan report - convenience function"""
    return api_service.generate_media_plan_report(form_data)
