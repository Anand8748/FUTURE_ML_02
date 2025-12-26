"""
Model Training Script for Spotify Churn Prediction
Trains multiple ML models and evaluates their performance.
"""

import pandas as pd
import numpy as np
import pickle
import warnings
warnings.filterwarnings('ignore')

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    roc_curve, precision_recall_curve
)
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns

class ChurnModelTrainer:
    """Class to train and evaluate churn prediction models"""
    
    def __init__(self):
        self.models = {}
        self.results = {}
        
    def train_logistic_regression(self, X_train, y_train, X_test, y_test):
        """Train Logistic Regression model"""
        print("\n" + "="*50)
        print("Training Logistic Regression...")
        print("="*50)
        
        model = LogisticRegression(random_state=42, max_iter=1000)
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Metrics
        metrics = self.calculate_metrics(y_test, y_pred, y_pred_proba)
        
        self.models['Logistic Regression'] = model
        self.results['Logistic Regression'] = {
            'model': model,
            'metrics': metrics,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba
        }
        
        self.print_metrics('Logistic Regression', metrics)
        return model, metrics
    
    def train_random_forest(self, X_train, y_train, X_test, y_test):
        """Train Random Forest model"""
        print("\n" + "="*50)
        print("Training Random Forest...")
        print("="*50)
        
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Metrics
        metrics = self.calculate_metrics(y_test, y_pred, y_pred_proba)
        
        self.models['Random Forest'] = model
        self.results['Random Forest'] = {
            'model': model,
            'metrics': metrics,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba,
            'feature_importance': model.feature_importances_
        }
        
        self.print_metrics('Random Forest', metrics)
        return model, metrics
    
    def train_xgboost(self, X_train, y_train, X_test, y_test):
        """Train XGBoost model"""
        print("\n" + "="*50)
        print("Training XGBoost...")
        print("="*50)
        
        model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            eval_metric='logloss'
        )
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Metrics
        metrics = self.calculate_metrics(y_test, y_pred, y_pred_proba)
        
        self.models['XGBoost'] = model
        self.results['XGBoost'] = {
            'model': model,
            'metrics': metrics,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba,
            'feature_importance': model.feature_importances_
        }
        
        self.print_metrics('XGBoost', metrics)
        return model, metrics
    
    def calculate_metrics(self, y_true, y_pred, y_pred_proba):
        """Calculate evaluation metrics"""
        metrics = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),
            'f1_score': f1_score(y_true, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(y_true, y_pred_proba) if len(np.unique(y_true)) > 1 else 0.0,
            'confusion_matrix': confusion_matrix(y_true, y_pred)
        }
        return metrics
    
    def print_metrics(self, model_name, metrics):
        """Print model metrics"""
        print(f"\n{model_name} Performance:")
        print(f"  Accuracy:  {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall:    {metrics['recall']:.4f}")
        print(f"  F1-Score:  {metrics['f1_score']:.4f}")
        print(f"  ROC-AUC:   {metrics['roc_auc']:.4f}")
        print(f"\nConfusion Matrix:")
        print(metrics['confusion_matrix'])
    
    def get_best_model(self):
        """Get the best model based on F1-score"""
        best_model_name = None
        best_f1 = 0
        
        for model_name, result in self.results.items():
            f1 = result['metrics']['f1_score']
            if f1 > best_f1:
                best_f1 = f1
                best_model_name = model_name
        
        return best_model_name, self.results[best_model_name]
    
    def save_models(self, filepath_prefix='churn_model'):
        """Save all trained models"""
        for model_name, result in self.results.items():
            filename = f"{filepath_prefix}_{model_name.lower().replace(' ', '_')}.pkl"
            with open(filename, 'wb') as f:
                pickle.dump(result['model'], f)
            print(f"Saved: {filename}")
    
    def save_best_model(self, filepath='best_churn_model.pkl'):
        """Save the best model"""
        best_name, best_result = self.get_best_model()
        with open(filepath, 'wb') as f:
            pickle.dump(best_result['model'], f)
        print(f"\n[SUCCESS] Best model ({best_name}) saved to {filepath}")
        return best_name

def create_visualizations(trainer, X_test, y_test, feature_names):
    """Create visualization plots for model evaluation"""
    print("\nCreating visualizations...")
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (15, 10)
    
    # 1. Model Comparison
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    model_names = list(trainer.results.keys())
    metrics_to_plot = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']
    
    for idx, metric in enumerate(metrics_to_plot):
        ax = axes[idx // 3, idx % 3]
        values = [trainer.results[name]['metrics'][metric] for name in model_names]
        bars = ax.bar(model_names, values, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        ax.set_title(f'{metric.replace("_", " ").title()}', fontsize=12, fontweight='bold')
        ax.set_ylabel('Score', fontsize=10)
        ax.set_ylim(0, 1)
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.3f}', ha='center', va='bottom', fontsize=9)
        
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Confusion Matrix for best model
    best_name, best_result = trainer.get_best_model()
    ax = axes[1, 2]
    cm = best_result['metrics']['confusion_matrix']
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                xticklabels=['No Churn', 'Churn'],
                yticklabels=['No Churn', 'Churn'])
    ax.set_title(f'Confusion Matrix - {best_name}', fontsize=12, fontweight='bold')
    ax.set_ylabel('Actual', fontsize=10)
    ax.set_xlabel('Predicted', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved: model_comparison.png")
    plt.close()
    
    # 2. ROC Curves
    plt.figure(figsize=(10, 8))
    for model_name, result in trainer.results.items():
        fpr, tpr, _ = roc_curve(y_test, result['y_pred_proba'])
        auc = result['metrics']['roc_auc']
        plt.plot(fpr, tpr, label=f'{model_name} (AUC = {auc:.3f})', linewidth=2)
    
    plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('ROC Curves Comparison', fontsize=14, fontweight='bold')
    plt.legend(loc='lower right', fontsize=10)
    plt.grid(alpha=0.3)
    plt.savefig('roc_curves.png', dpi=300, bbox_inches='tight')
    print("Saved: roc_curves.png")
    plt.close()
    
    # 3. Feature Importance (for tree-based models)
    tree_models = ['Random Forest', 'XGBoost']
    if any(name in trainer.results for name in tree_models):
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))
        
        for idx, model_name in enumerate(tree_models):
            if model_name in trainer.results:
                ax = axes[idx]
                importance = trainer.results[model_name]['feature_importance']
                feature_imp_df = pd.DataFrame({
                    'feature': feature_names,
                    'importance': importance
                }).sort_values('importance', ascending=False).head(15)
                
                sns.barplot(data=feature_imp_df, y='feature', x='importance', ax=ax, palette='viridis')
                ax.set_title(f'{model_name} - Top 15 Features', fontsize=12, fontweight='bold')
                ax.set_xlabel('Importance', fontsize=10)
                ax.set_ylabel('Feature', fontsize=10)
                ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
        print("Saved: feature_importance.png")
        plt.close()

def main():
    """Main training pipeline"""
    print("="*60)
    print("SPOTIFY CHURN PREDICTION - MODEL TRAINING")
    print("="*60)
    
    # Load preprocessed data
    print("\nLoading preprocessed data...")
    X_train = pd.read_csv('X_train.csv')
    X_test = pd.read_csv('X_test.csv')
    y_train = pd.read_csv('y_train.csv').values.ravel()
    y_test = pd.read_csv('y_test.csv').values.ravel()
    
    feature_names = X_train.columns.tolist()
    
    print(f"Training set: {X_train.shape}")
    print(f"Test set: {X_test.shape}")
    
    # Initialize trainer
    trainer = ChurnModelTrainer()
    
    # Train models
    trainer.train_logistic_regression(X_train, y_train, X_test, y_test)
    trainer.train_random_forest(X_train, y_train, X_test, y_test)
    trainer.train_xgboost(X_train, y_train, X_test, y_test)
    
    # Get best model
    best_name, best_result = trainer.get_best_model()
    print("\n" + "="*60)
    print(f"BEST MODEL: {best_name}")
    print("="*60)
    trainer.print_metrics(best_name, best_result['metrics'])
    
    # Save models
    trainer.save_models()
    trainer.save_best_model()
    
    # Create visualizations
    create_visualizations(trainer, X_test, y_test, feature_names)
    
    # Save results summary
    results_summary = pd.DataFrame({
        model_name: result['metrics']
        for model_name, result in trainer.results.items()
    }).T
    results_summary = results_summary[['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']]
    results_summary.to_csv('model_results_summary.csv')
    print("\nSaved: model_results_summary.csv")
    
    print("\n[SUCCESS] Model training completed!")
    
    return trainer

if __name__ == '__main__':
    trainer = main()

