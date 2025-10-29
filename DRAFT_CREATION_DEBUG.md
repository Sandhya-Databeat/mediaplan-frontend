# Draft Creation Debug Information

## Issue Fixed: Silent Failure

### Root Cause
The `st.rerun()` call was clearing all messages before they could be displayed to the user.

### What Was Fixed

1. **Removed Premature Rerun** (`create_draft_modal.py`)
   - Removed `st.rerun()` on line 119 that was clearing error messages
   - Messages will now stay visible for debugging

2. **Enhanced Error Logging** (`api_service.py`)
   - Added console logging with status codes
   - Added status code display in UI
   - Better error message formatting

## Backend Endpoint Investigation

### Confirmed Backend Endpoint
- **File**: `C:\Users\user\Desktop\backend folder - Copy\spotify-report-studio-backend\app\main.py` (line 98)
- **Router Registration**: `prefix="/mediaplan/drafts"`
- **Route Definition**: `@router.post("/create")` in `media_plan_drafts.py` (line 44)
- **Full Endpoint**: `http://localhost:8000/mediaplan/drafts/create`

### Current Streamlit Configuration
- **Endpoint**: `/mediaplan/drafts/create` ✅ CORRECT
- **File**: `api_service.py` (line 327)

### React App Configuration (For Reference)
- **Endpoint**: `/drafts/create` ⚠️ MISMATCH
- **File**: `frontend folder\spotify-report-studio\src\services\api.ts` (line 292)
- **Note**: React may be using an older endpoint or proxy configuration

## What to Check Now

### 1. Verify Backend is Running
```bash
# Check if backend is running on port 8000
curl http://localhost:8000/health
```

### 2. Test the Draft Creation Endpoint Directly
```bash
# Test the endpoint (should return 422 validation error)
curl -X POST http://localhost:8000/mediaplan/drafts/create -H "Content-Type: application/json" -d '{}'
```

Expected response: 422 Unprocessable Entity (because we sent empty data)

### 3. Run Streamlit and Check Console Output

When you click "Create Draft", you should now see:
- ✅ "📤 Sending draft to API..."
- ✅ API endpoint URL
- ✅ "📥 Received response from API"
- ✅ Response type and content
- ✅ Either success message OR detailed error message

### 4. Check Console/Terminal for Debug Logs

The console running Streamlit will show:
```
API Error during creating draft:
  Status Code: 404 (or other)
  Error Message: (error details)
  Full Error: (full exception)
```

## Possible Issues and Solutions

### Issue 1: Backend Not Running
**Symptoms**: Connection refused error, status code None
**Solution**:
```bash
cd "C:\Users\user\Desktop\backend folder - Copy\spotify-report-studio-backend"
python -m uvicorn app.main:app --reload --port 8000
```

### Issue 2: Wrong Endpoint (404 Error)
**Symptoms**: Status code 404
**Solution**: Backend endpoint changed, update `api_service.py` line 327

### Issue 3: Validation Error (422 Error)
**Symptoms**: Status code 422, "validation error" message
**Solution**: Check the draft data structure being sent, may need adjustment

### Issue 4: CORS Error
**Symptoms**: CORS-related error in browser console
**Solution**: Backend CORS settings may need update

## Next Steps After Testing

1. Click "Create Draft" in Streamlit
2. Screenshot or copy all messages that appear
3. Check the Streamlit console/terminal for debug output
4. Share the output to identify the exact issue

The messages will now persist on screen instead of disappearing!
