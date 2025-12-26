# 🚀 Quick Start Guide

## Installation (One-time Setup)

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Complete Pipeline

### Option 1: Run Everything at Once (Recommended)
```bash
python run_pipeline.py
```

This will:
- ✅ Preprocess the data
- ✅ Train all models
- ✅ Generate visualizations
- ✅ Save the best model

### Option 2: Run Step by Step

**Step 1: Data Preprocessing**
```bash
python data_preprocessing.py
```

**Step 2: Model Training**
```bash
python model_training.py
```

## Launching the Web Application

After running the pipeline, start the Streamlit app:

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## Using the Web App

### 🔮 Predict Churn Page
1. Fill in customer details using the form
2. Click "Predict Churn Risk"
3. View the churn probability and risk classification
4. See personalized recommendations

### 📈 Analytics Dashboard
- Explore customer demographics
- View subscription plan distributions
- Analyze music preferences
- Check engagement metrics

### 📊 Model Performance
- Compare model metrics
- View ROC curves
- See feature importance rankings

## Expected Results

After training, you should see:
- **Best Model**: XGBoost (typically achieves >95% accuracy)
- **Generated Files**:
  - `best_churn_model.pkl` - Best trained model
  - `preprocessor.pkl` - Data preprocessor
  - `model_comparison.png` - Model comparison charts
  - `roc_curves.png` - ROC curve visualization
  - `feature_importance.png` - Feature importance chart
  - `model_results_summary.csv` - Performance metrics

## Troubleshooting

### Issue: "Model not found" error in web app
**Solution**: Run `python model_training.py` first

### Issue: "Dataset not found" error
**Solution**: Ensure `Spotify_data.xlsx` is in the project root directory

### Issue: Import errors
**Solution**: Install all dependencies: `pip install -r requirements.txt`

### Issue: Port 8501 already in use
**Solution**: Streamlit will automatically use the next available port, or specify:
```bash
streamlit run app.py --server.port 8502
```

## Project Structure

```
├── Spotify_data.xlsx          # Original dataset
├── data_preprocessing.py      # Data preprocessing
├── model_training.py          # Model training
├── app.py                     # Web application
├── run_pipeline.py            # Quick start script
├── requirements.txt           # Dependencies
└── README.md                  # Full documentation
```

## Next Steps

1. ✅ Run the complete pipeline
2. ✅ Launch the web app
3. ✅ Test predictions with sample data
4. ✅ Explore the analytics dashboard
5. ✅ Review model performance metrics

---

**Need Help?** Check the full [README.md](README.md) for detailed documentation.

