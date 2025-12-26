"""
Quick Start Script - Run the complete pipeline
This script runs data preprocessing and model training in sequence.
"""

import subprocess
import sys
import os

def run_script(script_name):
    """Run a Python script and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running {script_name}...")
    print('='*60)
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False,
            text=True
        )
        print(f"\n[SUCCESS] {script_name} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] {script_name} failed with error:")
        print(e)
        return False
    except FileNotFoundError:
        print(f"\n[ERROR] {script_name} not found!")
        return False

def main():
    """Main pipeline execution"""
    print("="*60)
    print("SPOTIFY CHURN PREDICTION - COMPLETE PIPELINE")
    print("="*60)
    
    # Check if dataset exists
    if not os.path.exists('Spotify_data.xlsx'):
        print("\n[ERROR] Spotify_data.xlsx not found!")
        print("Please ensure the dataset is in the current directory.")
        return
    
    # Step 1: Data Preprocessing
    if not run_script('data_preprocessing.py'):
        print("\n[ERROR] Pipeline stopped at data preprocessing.")
        return
    
    # Step 2: Model Training
    if not run_script('model_training.py'):
        print("\n[ERROR] Pipeline stopped at model training.")
        return
    
    # Success message
    print("\n" + "="*60)
    print("[SUCCESS] Complete pipeline executed successfully!")
    print("="*60)
    print("\nNext steps:")
    print("1. Launch the web app: streamlit run app.py")
    print("2. Open your browser to http://localhost:8501")
    print("3. Explore the churn prediction system!")
    print("="*60)

if __name__ == '__main__':
    main()

