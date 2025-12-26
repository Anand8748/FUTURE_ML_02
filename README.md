# 🎵 Spotify Churn Prediction System

A comprehensive end-to-end machine learning project for predicting customer churn in Spotify. This system includes data preprocessing, model training with multiple algorithms, evaluation metrics, and a beautiful interactive web application.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Models](#models)
- [Web Application](#web-application)
- [Results](#results)
- [Technologies Used](#technologies-used)

## ✨ Features

- **Data Preprocessing**: Automated data cleaning, feature engineering, and churn target creation
- **Multiple ML Models**: Logistic Regression, Random Forest, and XGBoost
- **Comprehensive Evaluation**: Accuracy, Precision, Recall, F1-Score, ROC-AUC metrics
- **Visualizations**: Confusion matrices, ROC curves, feature importance charts
- **Interactive Web App**: Modern Streamlit application with beautiful UI
- **Churn Prediction**: Real-time customer churn risk assessment
- **Analytics Dashboard**: Customer behavior insights and visualizations

## 📁 Project Structure

```
customer churn prediction system/
│
├── Spotify_data.xlsx                    # Original dataset
├── data_preprocessing.py                # Data preprocessing pipeline
├── model_training.py                    # Model training and evaluation
├── app.py                               # Streamlit web application
├── requirements.txt                     # Python dependencies
├── README.md                            # Project documentation
│
├── Generated Files (after running):
├── X_train.csv                          # Training features
├── X_test.csv                           # Test features
├── y_train.csv                          # Training labels
├── y_test.csv                           # Test labels
├── preprocessor.pkl                     # Saved preprocessor
├── best_churn_model.pkl                 # Best trained model
├── churn_model_*.pkl                    # Individual model files
├── model_results_summary.csv             # Model performance summary
├── model_comparison.png                  # Model comparison visualization
├── roc_curves.png                       # ROC curves plot
└── feature_importance.png                # Feature importance chart
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone or download this repository**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure the dataset is in the project directory**:
   - `Spotify_data.xlsx` should be in the root directory

## 📊 Usage

### Step 1: Data Preprocessing

Run the data preprocessing script to clean and prepare the data:

```bash
python data_preprocessing.py
```

This will:
- Load the Spotify dataset
- Create churn target variable based on business rules
- Handle missing values
- Encode categorical features
- Split data into train/test sets
- Save processed data and preprocessor

### Step 2: Model Training

Train multiple ML models and evaluate their performance:

```bash
python model_training.py
```

This will:
- Train Logistic Regression, Random Forest, and XGBoost models
- Evaluate each model with multiple metrics
- Generate visualizations (confusion matrices, ROC curves, feature importance)
- Save the best model and all trained models
- Create a performance summary CSV

### Step 3: Launch Web Application

Start the Streamlit web application:

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## 📈 Dataset

The dataset contains 520 Spotify users with 20 features including:

- **Demographics**: Age, Gender
- **Usage**: Spotify usage period, listening device, subscription plan
- **Preferences**: Music genre, listening frequency, time slot, mood
- **Engagement**: Music recommendation rating, discovery methods
- **Podcasts**: Listening frequency, genre preferences, format preferences

### Churn Target Creation

The churn target variable is created based on business logic:
- Free plan users not willing to take premium
- Low recommendation ratings (≤ 2)
- Infrequent music listening
- Not satisfied with podcast variety
- Very short usage period

## 🤖 Models

Three machine learning models are trained and compared:

1. **Logistic Regression**: Baseline linear model
2. **Random Forest**: Ensemble tree-based model
3. **XGBoost**: Gradient boosting model

### Evaluation Metrics

- **Accuracy**: Overall prediction correctness
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1-Score**: Harmonic mean of precision and recall
- **ROC-AUC**: Area under the ROC curve

## 🌐 Web Application

The Streamlit web app includes four main pages:

### 🏠 Home
- Project overview and quick start guide
- Dataset statistics

### 🔮 Predict Churn
- Interactive form to input customer details
- Real-time churn probability prediction
- Risk classification (High/Moderate/Low)
- Personalized recommendations

### 📈 Analytics Dashboard
- Key customer metrics
- Subscription plan distribution
- Age group analysis
- Premium willingness trends
- Music genre preferences
- Listening device distribution
- Interactive Plotly visualizations

### 📊 Model Performance
- Model comparison metrics
- Performance visualizations
- Feature importance charts
- ROC curves

## 📊 Results

After training, you'll get:
- Model performance comparison table
- Confusion matrices for each model
- ROC curves visualization
- Feature importance rankings
- Best model selection based on F1-score

## 🛠️ Technologies Used

- **Python**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Scikit-learn**: Machine learning algorithms and utilities
- **XGBoost**: Gradient boosting framework
- **Streamlit**: Web application framework
- **Plotly**: Interactive visualizations
- **Matplotlib/Seaborn**: Static visualizations

## 📝 Key Features of the System

### Data Preprocessing
- Automatic missing value handling
- Label encoding for categorical variables
- Feature scaling with StandardScaler
- Stratified train-test split

### Model Training
- Multiple algorithm comparison
- Hyperparameter tuning ready
- Comprehensive evaluation metrics
- Model persistence (pickle)

### Web Application
- Modern, responsive UI design
- Real-time predictions
- Interactive dashboards
- Beautiful visualizations
- User-friendly interface

## 🎯 Business Impact

This churn prediction system helps:
- **Identify at-risk customers** before they churn
- **Prioritize retention efforts** based on churn probability
- **Understand churn drivers** through feature importance
- **Make data-driven decisions** to reduce customer churn
- **Improve customer retention** and revenue

## 🔮 Future Enhancements

- [ ] Hyperparameter tuning with GridSearchCV
- [ ] Model deployment to cloud (AWS, Azure, GCP)
- [ ] Real-time data pipeline integration
- [ ] Email/SMS alerts for high-risk customers
- [ ] A/B testing framework for retention strategies
- [ ] Advanced feature engineering
- [ ] Deep learning models (Neural Networks)

## 📄 License

This project is created for educational and internship purposes.

## 👥 Author

Built as part of the Machine Learning Task 2 - Churn Prediction System project.

## 🙏 Acknowledgments

- Spotify User Behavior Dataset from Kaggle
- Scikit-learn and XGBoost communities
- Streamlit team for the amazing framework

---

**Note**: Make sure to run the preprocessing and training scripts before using the web application. The app requires the trained model and preprocessor files to function properly.

