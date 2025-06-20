#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Model Training Script for LOC Approval System

This script trains three ML models for the LOC approval system:
1. Approval Status Model (Classification)
2. Credit Limit Model (Regression)
3. Interest Rate Model (Regression)

The models are trained on the merged dataset generated by data_generation.py.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    confusion_matrix, mean_absolute_error, r2_score
)
import joblib

# Set random seed for reproducibility
np.random.seed(42)

# Constants
TEST_SIZE = 0.2
RANDOM_STATE = 42
MODELS_DIR = '../backend/ml_models'

def load_data():
    """Load the merged dataset."""
    try:
        data_path = 'data/merged_data.csv'
        data = pd.read_csv(data_path)
        print(f"Loaded data with {data.shape[0]} rows and {data.shape[1]} columns.")
        return data
    except FileNotFoundError:
        print(f"Error: File {data_path} not found. Please run data_generation.py first.")
        exit(1)

def preprocess_data(data):
    """Preprocess the data for model training."""
    
    # Define features and targets
    X = data.drop(['applicant_id', 'approved', 'approved_amount', 'interest_rate'], axis=1)
    y_approval = data['approved']
    y_amount = data['approved_amount']
    y_interest = data['interest_rate']
    
    # Split data into training and testing sets
    X_train, X_test, y_approval_train, y_approval_test = train_test_split(
        X, y_approval, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    
    # Get indices of approved applications in training and testing sets
    approved_train_idx = y_approval_train == 1
    approved_test_idx = y_approval_test == 1
    
    # Create training and testing sets for amount and interest rate models
    # (only using approved applications)
    X_train_approved = X_train[approved_train_idx]
    X_test_approved = X_test[approved_test_idx]
    y_amount_train = y_amount[X_train.index[approved_train_idx]]
    y_amount_test = y_amount[X_test.index[approved_test_idx]]
    y_interest_train = y_interest[X_train.index[approved_train_idx]]
    y_interest_test = y_interest[X_test.index[approved_test_idx]]
    
    # Identify categorical and numerical columns
    categorical_cols = ['province', 'employment_status', 'payment_history']
    numerical_cols = [col for col in X.columns if col not in categorical_cols]
    
    # Create preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ]), numerical_cols),
            ('cat', Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore'))
            ]), categorical_cols)
        ]
    )
    
    return {
        'X_train': X_train,
        'X_test': X_test,
        'y_approval_train': y_approval_train,
        'y_approval_test': y_approval_test,
        'X_train_approved': X_train_approved,
        'X_test_approved': X_test_approved,
        'y_amount_train': y_amount_train,
        'y_amount_test': y_amount_test,
        'y_interest_train': y_interest_train,
        'y_interest_test': y_interest_test,
        'preprocessor': preprocessor,
        'feature_names': list(X.columns)
    }

def train_approval_model(data_dict):
    """Train the approval status classification model."""
    
    print("\n--- Training Approval Status Model ---")
    
    # Create pipeline with preprocessor and classifier
    approval_pipeline = Pipeline([
        ('preprocessor', data_dict['preprocessor']),
        ('classifier', RandomForestClassifier(
            n_estimators=200,  # Increased from 100
            max_depth=15,      # Increased from 10
            min_samples_split=3,  # Decreased from 5 for more granularity
            min_samples_leaf=2,   # Added parameter
            class_weight='balanced',  # Added to handle class imbalance
            random_state=RANDOM_STATE
        ))
    ])
    
    # Train the model
    approval_pipeline.fit(data_dict['X_train'], data_dict['y_approval_train'])
    
    # Make predictions on test set
    y_pred = approval_pipeline.predict(data_dict['X_test'])
    
    # Evaluate the model
    accuracy = accuracy_score(data_dict['y_approval_test'], y_pred)
    precision = precision_score(data_dict['y_approval_test'], y_pred)
    recall = recall_score(data_dict['y_approval_test'], y_pred)
    f1 = f1_score(data_dict['y_approval_test'], y_pred)
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    
    # Cross-validation
    cv_scores = cross_val_score(
        approval_pipeline, 
        pd.concat([data_dict['X_train'], data_dict['X_test']]), 
        pd.concat([data_dict['y_approval_train'], data_dict['y_approval_test']]), 
        cv=5, 
        scoring='accuracy'
    )
    print(f"Cross-validation accuracy: {cv_scores.mean():.4f} (±{cv_scores.std():.4f})")
    
    # Confusion matrix
    cm = confusion_matrix(data_dict['y_approval_test'], y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=['Denied', 'Approved'], 
                yticklabels=['Denied', 'Approved'])
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix - Approval Status')
    plt.tight_layout()
    plt.savefig('approval_confusion_matrix.png')
    
    # Feature importance
    if hasattr(approval_pipeline.named_steps['classifier'], 'feature_importances_'):
        # Get feature names after preprocessing
        preprocessor = approval_pipeline.named_steps['preprocessor']
        cat_cols = preprocessor.transformers_[1][2]  # Categorical columns
        cat_features = preprocessor.named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(cat_cols)
        feature_names = list(preprocessor.transformers_[0][2]) + list(cat_features)  # Numerical + categorical
        
        # Get feature importances
        importances = approval_pipeline.named_steps['classifier'].feature_importances_
        
        # Plot top 15 features
        indices = np.argsort(importances)[-15:]
        plt.figure(figsize=(10, 8))
        plt.barh(range(len(indices)), importances[indices])
        plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
        plt.xlabel('Feature Importance')
        plt.title('Top 15 Features - Approval Status Model')
        plt.tight_layout()
        plt.savefig('approval_feature_importance.png')
    
    return approval_pipeline

def train_credit_limit_model(data_dict):
    """Train the credit limit regression model."""
    
    print("\n--- Training Credit Limit Model ---")
    
    # Create pipeline with preprocessor and regressor
    credit_limit_pipeline = Pipeline([
        ('preprocessor', data_dict['preprocessor']),
        ('regressor', GradientBoostingRegressor(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            random_state=RANDOM_STATE
        ))
    ])
    
    # Train the model
    credit_limit_pipeline.fit(data_dict['X_train_approved'], data_dict['y_amount_train'])
    
    # Make predictions on test set
    y_pred = credit_limit_pipeline.predict(data_dict['X_test_approved'])
    
    # Evaluate the model
    mae = mean_absolute_error(data_dict['y_amount_test'], y_pred)
    r2 = r2_score(data_dict['y_amount_test'], y_pred)
    
    print(f"Mean Absolute Error: ${mae:.2f}")
    print(f"R² Score: {r2:.4f}")
    
    # Cross-validation
    cv_scores = cross_val_score(
        credit_limit_pipeline, 
        pd.concat([data_dict['X_train_approved'], data_dict['X_test_approved']]), 
        pd.concat([data_dict['y_amount_train'], data_dict['y_amount_test']]), 
        cv=5, 
        scoring='neg_mean_absolute_error'
    )
    print(f"Cross-validation MAE: ${-cv_scores.mean():.2f} (±{cv_scores.std():.2f})")
    
    # Plot actual vs predicted
    plt.figure(figsize=(10, 6))
    plt.scatter(data_dict['y_amount_test'], y_pred, alpha=0.5)
    plt.plot([0, 50000], [0, 50000], 'r--')
    plt.xlabel('Actual Credit Limit')
    plt.ylabel('Predicted Credit Limit')
    plt.title('Actual vs Predicted Credit Limit')
    plt.tight_layout()
    plt.savefig('credit_limit_predictions.png')
    
    return credit_limit_pipeline

def train_interest_rate_model(data_dict):
    """Train the interest rate regression model."""
    
    print("\n--- Training Interest Rate Model ---")
    
    # Create pipeline with preprocessor and regressor
    interest_rate_pipeline = Pipeline([
        ('preprocessor', data_dict['preprocessor']),
        ('regressor', GradientBoostingRegressor(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.05,
            random_state=RANDOM_STATE
        ))
    ])
    
    # Train the model
    interest_rate_pipeline.fit(data_dict['X_train_approved'], data_dict['y_interest_train'])
    
    # Make predictions on test set
    y_pred = interest_rate_pipeline.predict(data_dict['X_test_approved'])
    
    # Evaluate the model
    mae = mean_absolute_error(data_dict['y_interest_test'], y_pred)
    r2 = r2_score(data_dict['y_interest_test'], y_pred)
    
    print(f"Mean Absolute Error: {mae:.4f}%")
    print(f"R² Score: {r2:.4f}")
    
    # Cross-validation
    cv_scores = cross_val_score(
        interest_rate_pipeline, 
        pd.concat([data_dict['X_train_approved'], data_dict['X_test_approved']]), 
        pd.concat([data_dict['y_interest_train'], data_dict['y_interest_test']]), 
        cv=5, 
        scoring='neg_mean_absolute_error'
    )
    print(f"Cross-validation MAE: {-cv_scores.mean():.4f}% (±{cv_scores.std():.4f})")
    
    # Plot actual vs predicted
    plt.figure(figsize=(10, 6))
    plt.scatter(data_dict['y_interest_test'], y_pred, alpha=0.5)
    plt.plot([3, 15], [3, 15], 'r--')
    plt.xlabel('Actual Interest Rate (%)')
    plt.ylabel('Predicted Interest Rate (%)')
    plt.title('Actual vs Predicted Interest Rate')
    plt.tight_layout()
    plt.savefig('interest_rate_predictions.png')
    
    return interest_rate_pipeline

def save_models(approval_model, credit_limit_model, interest_rate_model):
    """Save the trained models to disk."""
    
    # Create models directory if it doesn't exist
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    # Save models
    joblib.dump(approval_model, os.path.join(MODELS_DIR, 'approval_model.joblib'))
    joblib.dump(credit_limit_model, os.path.join(MODELS_DIR, 'credit_limit_model.joblib'))
    joblib.dump(interest_rate_model, os.path.join(MODELS_DIR, 'interest_rate_model.joblib'))
    
    print(f"\nModels saved to {MODELS_DIR}")

def main():
    """Main function to train and save all models."""
    
    # Load data
    data = load_data()
    
    # Preprocess data
    data_dict = preprocess_data(data)
    
    # Train models
    approval_model = train_approval_model(data_dict)
    credit_limit_model = train_credit_limit_model(data_dict)
    interest_rate_model = train_interest_rate_model(data_dict)
    
    # Save models
    save_models(approval_model, credit_limit_model, interest_rate_model)
    
    print("\nModel training complete.")

if __name__ == "__main__":
    main()
