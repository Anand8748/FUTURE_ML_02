# Deploy to Streamlit Community Cloud - Step by Step Guide

This guide will walk you through deploying your Spotify Churn Prediction System to Streamlit Community Cloud.

## 📋 Prerequisites

Before you start, make sure you have:
- ✅ A GitHub account (free)
- ✅ Your code pushed to a GitHub repository
- ✅ All required files ready

---

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your GitHub Repository

1. **Create a GitHub repository** (if you don't have one):
   - Go to [github.com](https://github.com)
   - Click the "+" icon → "New repository"
   - Name it: `spotify-churn-prediction` (or any name you prefer)
   - Make it **Public** (required for free Streamlit Cloud)
   - Click "Create repository"

2. **Push your code to GitHub:**

   If you haven't initialized git yet:
   ```bash
   # Navigate to your project folder
   cd "customer churn prediction system"
   
   # Initialize git (if not already done)
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial commit - Spotify Churn Prediction System"
   
   # Add your GitHub repository as remote
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   
   # Push to GitHub
   git branch -M main
   git push -u origin main
   ```

   If you already have git initialized:
   ```bash
   git add .
   git commit -m "Ready for Streamlit Cloud deployment"
   git push origin main
   ```

### Step 2: Train Your Models (Important!)

Before deploying, make sure your models are trained:

```bash
# Run data preprocessing
python data_preprocessing.py

# Train the models
python model_training.py
```

This will create:
- `preprocessor.pkl`
- `best_churn_model.pkl`
- Other model files

**Make sure these files are committed to GitHub!**

### Step 3: Verify Required Files

Ensure these files are in your GitHub repository:

**Required Files:**
- ✅ `app.py` - Main application
- ✅ `requirements.txt` - Dependencies
- ✅ `Spotify_data.xlsx` - Dataset
- ✅ `preprocessor.pkl` - Preprocessor (after training)
- ✅ `best_churn_model.pkl` - Trained model (after training)

**Optional Files:**
- `spotify_image.png` - Logo
- `237248_medium.mp4` - Video file
- `data_preprocessing.py` - Preprocessing script
- `model_training.py` - Training script

### Step 4: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud:**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Click "Sign in" or "Get started"

2. **Sign in with GitHub:**
   - Click "Continue with GitHub"
   - Authorize Streamlit Cloud to access your GitHub account
   - You'll be redirected to the Streamlit Cloud dashboard

3. **Deploy Your App:**
   - Click the **"New app"** button
   - You'll see a form with these fields:

   **Repository:**
   - Select your GitHub repository from the dropdown
   - Or paste the repository URL: `https://github.com/YOUR_USERNAME/YOUR_REPO_NAME`

   **Branch:**
   - Select `main` (or `master` if that's your default branch)

   **Main file path:**
   - Enter: `app.py`
   - This is the main Streamlit application file

   **App URL (optional):**
   - You can customize this or leave it auto-generated
   - Example: `spotify-churn-prediction` will create:
     `https://spotify-churn-prediction.streamlit.app`

4. **Click "Deploy":**
   - Streamlit Cloud will start building your app
   - This usually takes 1-2 minutes
   - You'll see a progress indicator

5. **Wait for Deployment:**
   - Watch the build logs in real-time
   - If successful, you'll see "Your app is live!"
   - If there are errors, check the logs below

### Step 5: Access Your Live App

Once deployed, your app will be available at:
```
https://YOUR_APP_NAME.streamlit.app
```

You can:
- Share this URL with others
- Access it from any device
- Update it by pushing new code to GitHub

---

## 🔧 Troubleshooting Common Issues

### Issue 1: "Module not found" Error

**Solution:**
- Check that all dependencies are in `requirements.txt`
- Make sure versions are specified:
  ```
  streamlit>=1.28.0
  pandas>=1.5.0
  numpy>=1.24.3
  scikit-learn>=1.3.2
  xgboost>=2.0.3
  plotly>=5.18.0
  openpyxl>=3.1.2
  ```

### Issue 2: "File not found" Error (preprocessor.pkl or model.pkl)

**Solution:**
- Make sure you've trained the models locally
- Commit the `.pkl` files to GitHub:
  ```bash
  git add preprocessor.pkl best_churn_model.pkl
  git commit -m "Add trained models"
  git push origin main
  ```
- Redeploy on Streamlit Cloud

### Issue 3: "Dataset not found" Error

**Solution:**
- Ensure `Spotify_data.xlsx` is in your repository
- Check the file size (Streamlit Cloud has limits)
- Commit and push the file:
  ```bash
  git add Spotify_data.xlsx
  git commit -m "Add dataset"
  git push origin main
  ```

### Issue 4: Build Fails

**Solution:**
- Check the build logs in Streamlit Cloud
- Common causes:
  - Missing dependencies in `requirements.txt`
  - Syntax errors in `app.py`
  - Missing required files
- Fix the issue and push again

### Issue 5: App Runs but Shows Errors

**Solution:**
- Check the app logs in Streamlit Cloud dashboard
- Common issues:
  - Model files not found (need to train and commit)
  - Dataset path incorrect
  - Missing optional files (video, images)

---

## 🔄 Updating Your App

To update your deployed app:

1. **Make changes locally**
2. **Test locally:**
   ```bash
   streamlit run app.py
   ```
3. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Update app"
   git push origin main
   ```
4. **Streamlit Cloud will automatically redeploy!**
   - Go to your app dashboard
   - Click "Reboot app" if needed
   - Changes usually deploy within 1-2 minutes

---

## 📝 Streamlit Cloud Configuration

### Advanced Settings (Optional)

You can create a `.streamlit/config.toml` file for configuration:

```toml
[server]
headless = true
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

### Secrets Management

For sensitive data, use Streamlit Secrets:

1. In Streamlit Cloud dashboard, go to "Settings"
2. Click "Secrets"
3. Add your secrets in TOML format:
   ```toml
   [secrets]
   api_key = "your-api-key"
   ```
4. Access in your app:
   ```python
   import streamlit as st
   api_key = st.secrets["secrets"]["api_key"]
   ```

---

## ✅ Deployment Checklist

Before deploying, ensure:

- [ ] Code is pushed to GitHub
- [ ] `requirements.txt` is up to date
- [ ] Models are trained (`preprocessor.pkl`, `best_churn_model.pkl`)
- [ ] Dataset file is in repository
- [ ] App runs locally without errors
- [ ] All required files are committed
- [ ] Repository is public (for free tier)

---

## 🎉 Success!

Once deployed, you'll have:
- ✅ A live web application
- ✅ Shareable URL
- ✅ Automatic updates from GitHub
- ✅ Free hosting (with limitations)
- ✅ HTTPS included

---

## 📞 Need Help?

- **Streamlit Cloud Docs:** https://docs.streamlit.io/streamlit-community-cloud
- **Streamlit Community:** https://discuss.streamlit.io
- **GitHub Issues:** Check your repository for deployment logs

---

## 🚀 Quick Command Reference

```bash
# Initialize git (if needed)
git init

# Add all files
git add .

# Commit
git commit -m "Deploy to Streamlit Cloud"

# Push to GitHub
git push origin main

# Then deploy on share.streamlit.io!
```

**Your app will be live in minutes! 🎉**

