"""
Data Preprocessing Script for Spotify Churn Prediction
This script loads, cleans, and prepares the Spotify dataset for machine learning.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import pickle
import warnings
warnings.filterwarnings('ignore')

class SpotifyDataPreprocessor:
    """Class to handle data preprocessing for Spotify churn prediction"""
    
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_names = None
        
    def load_data(self, file_path='Spotify_data.xlsx'):
        """Load the Spotify dataset"""
        print("Loading data...")
        df = pd.read_excel(file_path)
        print(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    
    def create_churn_target(self, df):
        """
        Create churn target variable based on business logic:
        - Users with free plan who are not willing to take premium
        - Low recommendation ratings (<= 2)
        - Infrequent music listening
        - Not satisfied with podcast variety
        """
        print("\nCreating churn target variable...")
        
        # Initialize churn as 0 (no churn)
        churn = np.zeros(len(df))
        
        # Rule 1: Free plan users not willing to take premium
        free_not_willing = (
            (df['spotify_subscription_plan'].str.lower().str.contains('free', na=False)) &
            (df['premium_sub_willingness'].str.lower().str.contains('no', na=False))
        )
        churn[free_not_willing] = 1
        
        # Rule 2: Low recommendation ratings (<= 2 on scale 1-5)
        low_rating = df['music_recc_rating'] <= 2
        churn[low_rating] = 1
        
        # Rule 3: Infrequent music listening
        infrequent_listening = df['music_lis_frequency'].str.lower().str.contains(
            'rarely|never|occasionally', na=False, regex=True
        )
        churn[infrequent_listening] = 1
        
        # Rule 4: Not satisfied with podcast variety
        not_satisfied_podcast = df['pod_variety_satisfaction'].str.lower().str.contains(
            'not satisfied|dissatisfied|no', na=False, regex=True
        )
        churn[not_satisfied_podcast] = 1
        
        # Rule 5: Very short usage period (new users who might churn)
        short_usage = df['spotify_usage_period'].str.lower().str.contains(
            'less than|0-6|1-3', na=False, regex=True
        )
        churn[short_usage] = 1
        
        # Convert to binary (if any rule matches, churn = 1)
        df['churn'] = (churn > 0).astype(int)
        
        print(f"Churn distribution:")
        print(df['churn'].value_counts())
        print(f"\nChurn rate: {df['churn'].mean()*100:.2f}%")
        
        return df
    
    def handle_missing_values(self, df):
        """Handle missing values in the dataset"""
        print("\nHandling missing values...")
        
        # Fill missing values with appropriate defaults
        df['preffered_premium_plan'] = df['preffered_premium_plan'].fillna('Not Applicable')
        df['fav_pod_genre'] = df['fav_pod_genre'].fillna('None')
        df['preffered_pod_format'] = df['preffered_pod_format'].fillna('No Preference')
        df['pod_host_preference'] = df['pod_host_preference'].fillna('No Preference')
        df['preffered_pod_duration'] = df['preffered_pod_duration'].fillna('No Preference')
        
        print("Missing values handled")
        return df
    
    def encode_categorical_features(self, df, categorical_cols):
        """Encode categorical features using Label Encoding"""
        print("\nEncoding categorical features...")
        
        df_encoded = df.copy()
        
        for col in categorical_cols:
            if col in df_encoded.columns:
                le = LabelEncoder()
                # Handle NaN values
                df_encoded[col] = df_encoded[col].astype(str)
                df_encoded[col] = le.fit_transform(df_encoded[col])
                self.label_encoders[col] = le
                print(f"  Encoded: {col} ({len(le.classes_)} categories)")
        
        return df_encoded
    
    def prepare_features(self, df):
        """Prepare features for modeling"""
        print("\nPreparing features...")
        
        # Select features (exclude churn target)
        feature_cols = [col for col in df.columns if col != 'churn']
        
        # Identify categorical columns
        categorical_cols = df[feature_cols].select_dtypes(include=['object']).columns.tolist()
        
        # Encode categorical features
        df_encoded = self.encode_categorical_features(df, categorical_cols)
        
        # Select final features
        X = df_encoded[feature_cols]
        y = df_encoded['churn']
        
        self.feature_names = X.columns.tolist()
        
        print(f"Final feature count: {len(self.feature_names)}")
        
        return X, y
    
    def split_data(self, X, y, test_size=0.2, random_state=42):
        """Split data into train and test sets"""
        print(f"\nSplitting data (test_size={test_size})...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        print(f"Train set: {X_train.shape[0]} samples")
        print(f"Test set: {X_test.shape[0]} samples")
        return X_train, X_test, y_train, y_test
    
    def scale_features(self, X_train, X_test):
        """Scale features using StandardScaler"""
        print("\nScaling features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Convert back to DataFrame
        X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
        X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)
        
        return X_train_scaled, X_test_scaled
    
    def save_preprocessor(self, filepath='preprocessor.pkl'):
        """Save preprocessor objects"""
        preprocessor_data = {
            'label_encoders': self.label_encoders,
            'scaler': self.scaler,
            'feature_names': self.feature_names
        }
        with open(filepath, 'wb') as f:
            pickle.dump(preprocessor_data, f)
        print(f"\nPreprocessor saved to {filepath}")
    
    def load_preprocessor(self, filepath='preprocessor.pkl'):
        """Load preprocessor objects"""
        with open(filepath, 'rb') as f:
            preprocessor_data = pickle.load(f)
        self.label_encoders = preprocessor_data['label_encoders']
        self.scaler = preprocessor_data['scaler']
        self.feature_names = preprocessor_data['feature_names']
        print(f"Preprocessor loaded from {filepath}")

def main():
    """Main preprocessing pipeline"""
    preprocessor = SpotifyDataPreprocessor()
    
    # Load data
    df = preprocessor.load_data('Spotify_data.xlsx')
    
    # Create churn target
    df = preprocessor.create_churn_target(df)
    
    # Handle missing values
    df = preprocessor.handle_missing_values(df)
    
    # Prepare features
    X, y = preprocessor.prepare_features(df)
    
    # Split data
    X_train, X_test, y_train, y_test = preprocessor.split_data(X, y)
    
    # Scale features
    X_train_scaled, X_test_scaled = preprocessor.scale_features(X_train, X_test)
    
    # Save processed data
    X_train_scaled.to_csv('X_train.csv', index=False)
    X_test_scaled.to_csv('X_test.csv', index=False)
    y_train.to_csv('y_train.csv', index=False)
    y_test.to_csv('y_test.csv', index=False)
    
    # Save preprocessor
    preprocessor.save_preprocessor('preprocessor.pkl')
    
    print("\n[SUCCESS] Data preprocessing completed!")
    print(f"Processed data saved: X_train.csv, X_test.csv, y_train.csv, y_test.csv")
    
    return X_train_scaled, X_test_scaled, y_train, y_test, preprocessor

if __name__ == '__main__':
    main()

