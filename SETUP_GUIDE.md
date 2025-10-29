# 🎵 Spotify Media Plan - Complete Setup Guide

This guide will help you set up and run both the frontend (Streamlit) and backend (FastAPI) for the Spotify Media Plan application.

---

## 📁 Project Structure

```
Desktop/
├── MediaPlan - Frontend/              # Streamlit Frontend
│   ├── api_service.py                 # Centralized API service
│   ├── media_plan_form_streamlit.py   # Main form page
│   ├── pages/
│   │   └── mediaplandrafts.py         # Drafts management page
│   ├── requirements.txt
│   └── SETUP_GUIDE.md (this file)
│
└── backend folder - Copy/
    └── spotify-report-studio-backend/ # FastAPI Backend
        ├── app/
        │   ├── main.py                # Main API application
        │   ├── routers/               # API route handlers
        │   ├── models/                # Data models
        │   └── services/              # Business logic
        ├── requirements.txt
        └── run.bat                    # Startup script
```

---

## 🚀 Quick Start

### Step 1: Start the Backend (FastAPI)

Open a **new terminal/command prompt**:

```bash
cd "C:\Users\user\Desktop\backend folder - Copy\spotify-report-studio-backend"
run.bat
```

This will:
- Activate the virtual environment (if it exists)
- Install dependencies
- Start the FastAPI server on `http://localhost:8000`

**Expected Output:**
```
Starting FastAPI server...
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

✅ **Backend is ready!** You should see "Application startup complete."

---

### Step 2: Start the Frontend (Streamlit)

Open a **second terminal/command prompt**:

```bash
cd "C:\Users\user\Desktop\MediaPlan - Frontend"
streamlit run media_plan_form_streamlit.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

✅ **Frontend is ready!** Your browser should automatically open to `http://localhost:8501`

---

## 🎯 How to Use the Application

### Creating a Media Plan

1. **Fill out the form** by going through the 6 tabs:
   - 📋 Objective
   - 🎯 Targeting
   - 🎨 Format
   - 📊 Delivery
   - 💰 Budget
   - 💵 Bidding

2. **Click "Get Bid Estimate"** in the Bidding tab

3. **Click "Generate Insights"** to see campaign projections

4. **Click "Generate Draft"** to create a downloadable Excel report

### Managing Drafts

1. **Click the "📁 Media Plan Drafts" button** in the top-right corner

2. You'll see all your saved drafts organized by:
   - Campaign name
   - Budget level
   - Asset format (Audio, Video, Display)

3. **Select drafts** to finalize them

4. **Edit or delete** drafts as needed

---

## 🔧 API Endpoints

The backend provides these main endpoints:

### Media Plan Form
- `POST /mediaplan/insights` - Get campaign insights
- `POST /mediaplan/estimate-bid` - Get bid estimates
- `POST /mediaplan/report` - Generate media plan report
- `GET /mediaplan/sensitive-topics` - Get sensitive topics list

### Search
- `GET /mediaplan/search/artists?q={query}` - Search artists
- `GET /mediaplan/search/interests?q={query}` - Search interests
- `GET /mediaplan/search/geo?q={query}` - Search locations
- `GET /mediaplan/search/playlists?q={query}` - Search playlists
- `GET /mediaplan/search/podcast-topics?q={query}` - Search podcast topics

### Drafts Management
- `GET /mediaplan/drafts/list` - List all drafts
- `GET /mediaplan/drafts/stats` - Get draft statistics
- `POST /mediaplan/drafts/create` - Create new draft
- `GET /mediaplan/drafts/get/{id}` - Get specific draft
- `PUT /mediaplan/drafts/update/{id}` - Update draft
- `DELETE /mediaplan/drafts/delete/{id}` - Delete draft
- `POST /mediaplan/drafts/finalize` - Finalize selected drafts
- `GET /mediaplan/drafts/finalized` - Get finalized plans
- `GET /mediaplan/drafts/download_report` - Download Excel report

---

## 🎨 UI Features

### Styling
- **Spotify Colors**: Green (#1DB954), Black (#191414), White
- **Black Borders**: All dropdowns, inputs, and form elements have 2px black borders
- **Expanders**: Music Genres, Playlist Themes, and Podcast Topics use collapsible sections
- **Responsive Design**: Works on desktop and mobile browsers

### Navigation
- **Progress Bar**: Visual indicator showing which step you're on
- **Next/Previous Buttons**: Navigate between form sections
- **Media Plan Drafts Button**: Quick access to drafts management (top-right corner)
- **Back Button**: Return to form from drafts page (top-left corner)

---

## 📊 Data Storage

- **Drafts Storage**: `backend folder - Copy/spotify-report-studio-backend/media_plan_drafts.json`
- **Format**: JSON file with structure:
  ```json
  {
    "campaign_name": {
      "budget_name": {
        "AUDIO": [draft1, draft2, ...],
        "VIDEO": [draft1, draft2, ...],
        "DISPLAY": [draft1, draft2, ...]
      }
    }
  }
  ```

---

## 🔍 Troubleshooting

### Backend Issues

**Problem**: Backend won't start
```bash
# Solution: Install dependencies manually
cd "C:\Users\user\Desktop\backend folder - Copy\spotify-report-studio-backend"
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Problem**: "Address already in use" error
```bash
# Solution: Kill the process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

### Frontend Issues

**Problem**: "Error loading drafts: 404"
- ✅ **Solution**: Make sure the backend is running first!
- Check: `http://localhost:8000/health` should return `{"status":"ok"}`

**Problem**: "Connection refused" errors
- ✅ **Solution**: The backend must be running on port 8000
- Verify in backend terminal: Look for "Uvicorn running on http://0.0.0.0:8000"

**Problem**: Dropdown borders not showing
- ✅ **Solution**: The CSS has been updated. Try:
  1. Hard refresh: `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac)
  2. Restart Streamlit: `Ctrl + C` then `streamlit run media_plan_form_streamlit.py`

---

## 🔐 Configuration

### API Base URL

The frontend connects to `http://localhost:8000` by default.

To change this, create a secrets file:

```bash
# Create directory
mkdir "C:\Users\user\Desktop\MediaPlan - Frontend\.streamlit"

# Create file: .streamlit/secrets.toml
# Add this line:
API_BASE_URL = "http://your-api-url:8000"
```

---

## 📝 Development Notes

### File Organization

**Frontend (`MediaPlan - Frontend/`):**
- `api_service.py` - **Centralized API service** (mirrors TypeScript api.ts)
- `media_plan_form_streamlit.py` - Main form with 6-step wizard
- `pages/mediaplandrafts.py` - Drafts management interface

**Backend (`backend folder - Copy/spotify-report-studio-backend/`):**
- `app/main.py` - FastAPI app with CORS and router registration
- `app/routers/media_plan_drafts.py` - Draft CRUD operations
- `app/routers/mediaplan.py` - Media plan insights and bidding
- `app/services/` - Business logic layer
- `app/models/` - Pydantic models for request/response

### Key Changes Made
1. ✅ Created centralized `api_service.py` based on TypeScript `api.ts`
2. ✅ Updated `media_plan_form_streamlit.py` to use centralized API service
3. ✅ Updated `mediaplandrafts.py` to use centralized API service
4. ✅ Fixed backend router prefix: `/drafts` → `/mediaplan/drafts`
5. ✅ Added 2px black borders to all dropdowns and inputs
6. ✅ Ensured all API calls go through one service layer

---

## ✅ Verification Checklist

Before using the application, verify:

- [ ] Backend is running on `http://localhost:8000`
- [ ] Frontend is running on `http://localhost:8501`
- [ ] Health check works: Visit `http://localhost:8000/health`
- [ ] API docs available: Visit `http://localhost:8000/docs`
- [ ] Main form loads without errors
- [ ] "Media Plan Drafts" button navigates successfully
- [ ] Dropdowns have black borders
- [ ] All input fields have black borders

---

## 🎉 You're All Set!

Your Spotify Media Plan application is now ready to use. Enjoy creating media plans! 🚀

For questions or issues, check the troubleshooting section above.
