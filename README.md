# 🎵 Spotify Media Plan - Streamlit Application

A complete media planning tool for Spotify advertising campaigns with draft management capabilities. This is a full-featured Streamlit application with centralized API integration and a modern UI.

## ✨ Features

### 📋 Media Plan Form
- **6-Step Wizard**: Objective → Targeting → Format → Delivery → Budget → Bidding
- **Campaign Objective Setup**: Define campaign name and objectives
- **Advanced Targeting**: Geographic, demographic, and interest-based targeting
- **Format & Placement**: Configure asset formats, placements, and content targeting
- **Delivery Settings**: Set frequency caps for impressions
- **Budget & Schedule**: Define budget type, amount, and campaign dates
- **Bidding**: Get bid estimates and set bid caps
- **Insights Generation**: Generate campaign insights with audience forecasts
- **Report Generation**: Download media plan reports as Excel files

### 📁 Draft Management (NEW!)
- **View All Drafts**: Organized by campaign → budget → format
- **Statistics Dashboard**: Total drafts, by status, by budget, by format
- **Edit & Delete**: Manage drafts with ease
- **Finalize Drafts**: Select and finalize multiple drafts
- **Download Reports**: Export finalized plans as Excel

### 🎨 UI Design
- **Spotify Colors**: Green (#1DB954) and Black (#191414)
- **Black Borders**: All dropdowns and inputs have 2px black borders
- **Progress Bar**: Visual step indicator
- **Responsive Design**: Works on all screen sizes
- **Smooth Navigation**: Next/Previous buttons with validation

## 🚀 Quick Start

### Option 1: One-Click Startup (Easiest!)
```bash
# Just double-click this file:
START_APPLICATION.bat
```
This starts both backend and frontend automatically!

### Option 2: Manual Startup

**Terminal 1 (Backend):**
```bash
cd "C:\Users\user\Desktop\backend folder - Copy\spotify-report-studio-backend"
run.bat
```

**Terminal 2 (Frontend):**
```bash
cd "C:\Users\user\Desktop\MediaPlan - Frontend"
streamlit run media_plan_form_streamlit.py
```

### URLs
- **Frontend**: http://localhost:8501
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📖 Full Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup and troubleshooting
- **[COMPLETED_SETUP.md](COMPLETED_SETUP.md)** - Architecture and changes summary

## Prerequisites

- Python 3.8 or higher
- Backend API running on `http://localhost:8000`

## Installation

Both frontend and backend dependencies are already configured.

**Frontend:**
```bash
cd "C:\Users\user\Desktop\MediaPlan - Frontend"
pip install -r requirements.txt
```

**Backend:**
```bash
cd "C:\Users\user\Desktop\backend folder - Copy\spotify-report-studio-backend"
pip install -r requirements.txt
```

## Configuration

If your backend API is running on a different URL, you can modify the `API_BASE_URL` constant at the top of `media_plan_form_streamlit.py`:

```python
API_BASE_URL = "http://localhost:8000"  # Change this to your backend URL
```

## Usage

1. **Objective Tab**: Enter campaign name and select campaign objective
2. **Targeting Tab**: Configure geographic, demographic, and interest targeting
3. **Format Tab**: Select asset formats, placements, and content filters
4. **Delivery Tab**: Set frequency caps for daily, weekly, and monthly impressions
5. **Budget Tab**: Define budget type, amount, and campaign schedule
6. **Bidding Tab**: Get bid estimates and set your bid cap
7. Click **Generate Insights** to get campaign forecasts
8. Click **Generate Report** to download the media plan report

## 📡 API Endpoints

### Media Plan Form
- `GET /mediaplan/sensitive-topics` - Get sensitive topics
- `POST /mediaplan/estimate-bid` - Get bid estimates
- `POST /mediaplan/insights` - Generate campaign insights
- `POST /mediaplan/report` - Generate and download report

### Search (Dynamic)
- `GET /mediaplan/search/artists?q={query}` - Search artists
- `GET /mediaplan/search/interests?q={query}` - Search interests
- `GET /mediaplan/search/geo?q={query}` - Search geographic targets
- `GET /mediaplan/search/playlists?q={query}` - Search playlists
- `GET /mediaplan/search/podcast-topics?q={query}` - Search podcast topics

### Drafts Management (NEW!)
- `GET /mediaplan/drafts/list` - List all drafts
- `GET /mediaplan/drafts/stats` - Get draft statistics
- `POST /mediaplan/drafts/create` - Create new draft
- `GET /mediaplan/drafts/get/{id}` - Get specific draft
- `PUT /mediaplan/drafts/update/{id}` - Update draft
- `DELETE /mediaplan/drafts/delete/{id}` - Delete draft
- `POST /mediaplan/drafts/finalize` - Finalize selected drafts
- `GET /mediaplan/drafts/finalized` - Get finalized plans
- `GET /mediaplan/drafts/download_report` - Download Excel report

All API calls go through the centralized `api_service.py` module.

## 🏗️ Architecture

```
Frontend (Streamlit)          Backend (FastAPI)
├── api_service.py      ─────▶ app/main.py
├── media_plan_form.py  ─────▶ routers/mediaplan.py
└── pages/              ─────▶ routers/media_plan_drafts.py
    └── mediaplandrafts.py     services/
                               models/
```

**Centralized API Service**: All API calls go through `api_service.py` (Python equivalent of TypeScript `api.ts`)

## ✅ What's New

- ✅ **Centralized API Service** - Single source of truth for all API calls
- ✅ **Draft Management Page** - Complete CRUD interface for drafts
- ✅ **Black Borders on Dropdowns** - All dropdowns and inputs styled with 2px black borders
- ✅ **Statistics Dashboard** - View draft counts by status, budget, and format
- ✅ **One-Click Startup** - `START_APPLICATION.bat` for easy launching
- ✅ **Complete Documentation** - SETUP_GUIDE.md and COMPLETED_SETUP.md

## 📂 Project Structure

```
MediaPlan - Frontend/
├── api_service.py                  # ✨ Centralized API service
├── media_plan_form_streamlit.py    # Main form (6 tabs)
├── pages/
│   └── mediaplandrafts.py          # Drafts management
├── START_APPLICATION.bat           # One-click startup
├── SETUP_GUIDE.md                  # Complete guide
├── COMPLETED_SETUP.md              # Architecture summary
├── README.md                       # This file
└── requirements.txt                # Dependencies
```

## Notes

- All form data is stored in Streamlit's session state
- Search results are cached to improve performance
- The application requires an active backend API connection
- Drafts are stored in: `backend folder - Copy/spotify-report-studio-backend/media_plan_drafts.json`

## 🎉 Status

**✅ PRODUCTION READY**

All components are fully integrated, styled, and ready to use!

---

**Created with ❤️ for Spotify Media Planning**
