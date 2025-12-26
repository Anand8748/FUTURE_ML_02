# Quick Deploy to Streamlit Cloud - 5 Minutes

## 🚀 Fastest Way to Deploy

### 1. Push to GitHub (2 minutes)

```bash
# If first time
git init
git add .
git commit -m "Ready for deployment"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main

# If already on GitHub
git add .
git commit -m "Update for deployment"
git push origin main
```

### 2. Train Models (1 minute)

```bash
python data_preprocessing.py
python model_training.py
```

### 3. Commit Model Files (30 seconds)

```bash
git add preprocessor.pkl best_churn_model.pkl
git commit -m "Add trained models"
git push origin main
```

### 4. Deploy on Streamlit Cloud (1 minute)

1. Go to: https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Main file: `app.py`
6. Click "Deploy"

### 5. Done! ✅

Your app is live at: `https://YOUR-APP-NAME.streamlit.app`

---

## ⚠️ Important Notes

- Repository must be **Public** (for free tier)
- Make sure `preprocessor.pkl` and `best_churn_model.pkl` are committed
- All files in `requirements.txt` must be listed
- Test locally first: `streamlit run app.py`

---

## 🔧 If Something Goes Wrong

Check the deployment logs in Streamlit Cloud dashboard for error messages.

