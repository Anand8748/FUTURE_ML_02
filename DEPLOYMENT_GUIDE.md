# Deployment Guide - Spotify Churn Prediction System

This guide covers multiple ways to deploy your Streamlit application online.

## 🚀 Quick Deployment Options

### Option 1: Streamlit Cloud (Recommended - Easiest)

**Streamlit Cloud is the easiest way to deploy your app for free!**

#### Steps:

1. **Prepare your repository:**
   - Push your code to GitHub
   - Ensure all files are committed:
     - `app.py`
     - `requirements.txt`
     - `Spotify_data.xlsx` (or ensure it's in the repo)
     - `preprocessor.pkl` and `best_churn_model.pkl` (after training)

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Your app will be live at:**
   - `https://your-username-spotify-churn.streamlit.app`

#### Requirements:
- GitHub account
- All dependencies in `requirements.txt`
- Model files must be in the repository

---

### Option 2: Heroku

#### Prerequisites:
- Heroku account (free tier available)
- Heroku CLI installed
- Git repository

#### Steps:

1. **Install Heroku CLI:**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create necessary files:**

   **Create `Procfile`:**
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

   **Create `setup.sh`:**
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [general]\n\
   email = \"your-email@domain.com\"\n\
   " > ~/.streamlit/credentials.toml
   echo "\
   [server]\n\
   headless = true\n\
   enableCORS=false\n\
   port = $PORT\n\
   " > ~/.streamlit/config.toml
   ```

3. **Update `requirements.txt`** (ensure it includes):
   ```
   streamlit
   pandas
   numpy
   scikit-learn
   xgboost
   plotly
   openpyxl
   pickle5
   ```

4. **Deploy:**
   ```bash
   # Login to Heroku
   heroku login
   
   # Create app
   heroku create your-app-name
   
   # Deploy
   git push heroku main
   ```

---

### Option 3: Docker + Any Cloud Provider

#### Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run streamlit
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Create `.dockerignore`:
```
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv
pip-log.txt
pip-delete-this-directory.txt
.git
.gitignore
.DS_Store
*.md
```

#### Build and Run:
```bash
# Build image
docker build -t spotify-churn-app .

# Run container
docker run -p 8501:8501 spotify-churn-app
```

#### Deploy to:
- **AWS ECS/Fargate**
- **Google Cloud Run**
- **Azure Container Instances**
- **DigitalOcean App Platform**

---

### Option 4: PythonAnywhere

1. **Sign up at:** [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload files via Files tab**

3. **Install dependencies in Bash console:**
   ```bash
   pip3.9 install --user streamlit pandas numpy scikit-learn xgboost plotly openpyxl
   ```

4. **Run in Bash:**
   ```bash
   streamlit run app.py --server.port=8501
   ```

---

## 📋 Pre-Deployment Checklist

### 1. **Ensure all files are ready:**
- [ ] `app.py` - Main application
- [ ] `requirements.txt` - All dependencies
- [ ] `Spotify_data.xlsx` - Dataset
- [ ] `preprocessor.pkl` - Preprocessor (after running `data_preprocessing.py`)
- [ ] `best_churn_model.pkl` - Trained model (after running `model_training.py`)
- [ ] `spotify_image.png` or `spotify_image.png` - Logo (optional)
- [ ] `237248_medium.mp4` - Video file (optional)

### 2. **Test locally:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run preprocessing
python data_preprocessing.py

# Train model
python model_training.py

# Test app
streamlit run app.py
```

### 3. **Update `requirements.txt`** (ensure all packages are listed):
```
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.23.0
scikit-learn>=1.2.0
xgboost>=1.7.0
plotly>=5.14.0
openpyxl>=3.0.0
pickle5>=0.0.11
```

### 4. **Environment Variables (if needed):**
Create `.env` file or set in deployment platform:
```
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

---

## 🔧 Troubleshooting

### Common Issues:

1. **Model files not found:**
   - Ensure `preprocessor.pkl` and `best_churn_model.pkl` are in the repository
   - Run training scripts before deployment

2. **Port issues:**
   - Use `$PORT` environment variable (Heroku)
   - Or set to `8501` (default Streamlit port)

3. **Missing dependencies:**
   - Check `requirements.txt` includes all packages
   - Some platforms need `gunicorn` or `waitress` for production

4. **File size limits:**
   - Some platforms have file size limits
   - Consider using cloud storage for large files (S3, Google Cloud Storage)

---

## 🌐 Recommended: Streamlit Cloud

**Why Streamlit Cloud?**
- ✅ Free tier available
- ✅ Automatic deployments from GitHub
- ✅ Easy to set up (5 minutes)
- ✅ HTTPS included
- ✅ Custom domain support
- ✅ No credit card required

**Steps:**
1. Push code to GitHub
2. Go to share.streamlit.io
3. Connect repository
4. Deploy!

Your app will be live at: `https://your-repo-name.streamlit.app`

---

## 📱 Mobile App (Future Enhancement)

To convert to a mobile app, consider:
- **Streamlit Mobile** (if available)
- **Flutter/React Native** wrapper
- **Progressive Web App (PWA)** conversion

---

## 🔐 Security Considerations

Before deploying:
- [ ] Remove any hardcoded API keys
- [ ] Use environment variables for secrets
- [ ] Enable authentication if needed
- [ ] Review file permissions
- [ ] Add rate limiting for production

---

## 📞 Need Help?

- Streamlit Docs: https://docs.streamlit.io
- Streamlit Community: https://discuss.streamlit.io
- Deployment Issues: Check platform-specific documentation

---

**Good luck with your deployment! 🚀**

