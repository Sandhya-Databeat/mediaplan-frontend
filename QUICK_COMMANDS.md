# 🚀 Quick Commands Reference

## Initialize and Push to GitHub (First Time Only)

```bash
# Navigate to project folder
cd "C:\Users\user\Desktop\MediaPlan - Frontend"

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit"

# Add remote (REPLACE yourusername!)
git remote add origin https://github.com/yourusername/mediaplan-frontend.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## Update Deployed App (After Making Changes)

```bash
# Navigate to project
cd "C:\Users\user\Desktop\MediaPlan - Frontend"

# Check what changed
git status

# Add all changes
git add .

# Commit with message
git commit -m "Description of what you changed"

# Push to GitHub (triggers auto-deploy on Streamlit)
git push origin main
```

---

## Quick Git Commands

```bash
# See what changed
git status

# See changes in detail
git diff

# Add specific file
git add filename.py

# Add all files
git add .

# Commit
git commit -m "Your message here"

# Push
git push origin main

# Pull latest changes
git pull origin main

# See commit history
git log --oneline

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard local changes
git checkout -- filename.py
```

---

## Test Locally Before Pushing

```bash
# Run backend locally
cd "C:\Users\user\Desktop\backend folder - Copy\spotify-report-studio-backend"
python -m uvicorn app.main:app --reload --port 8000

# Run frontend locally (in new terminal)
cd "C:\Users\user\Desktop\MediaPlan - Frontend"
streamlit run media_plan_form_streamlit.py
```

---

## Check Deployed Apps

```bash
# Test backend health
curl https://your-backend-url.onrender.com/health

# Open frontend
# Just visit: https://your-app.streamlit.app
```

---

## Emergency: Start Over

If you mess up Git and want to start fresh:

```bash
# Delete .git folder
cd "C:\Users\user\Desktop\MediaPlan - Frontend"
rmdir /s .git

# Start over
git init
git add .
git commit -m "Fresh start"
git remote add origin https://github.com/yourusername/mediaplan-frontend.git
git branch -M main
git push -u origin main --force
```

---

## Install Git (If Not Installed)

Download from: https://git-scm.com/downloads

Configure after install:
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

---

## Troubleshooting

### "Permission denied"
- You may need to authenticate with GitHub
- Use personal access token instead of password
- Or use SSH keys

### "Not a git repository"
- You're not in the right folder
- Run `git init` first

### "Remote already exists"
```bash
git remote rm origin
git remote add origin https://github.com/yourusername/repo.git
```

### "Failed to push"
```bash
# Force push (WARNING: overwrites remote)
git push origin main --force
```
