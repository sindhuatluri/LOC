#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Data Generation Script for LOC Approval System

This script generates synthetic data for training the ML models in the LOC approval system.
It creates three datasets:
1. Applicant Input Dataset
2. Third-Party Credit Dataset
3. Merged Dataset with calculated fields and target variables

The data follows the distributions specified in the requirements.
"""

import os
import numpy as np
import pandas as pd

# Set random seed for reproducibility
np.random.seed(42)

# Constants
NUM_SAMPLES = 5000
PROVINCES = ["ON", "BC", "AB", "QC", "MB", "SK", "NS", "NB", "NL", "PE", "YT", "NT", "NU"]
EMPLOYMENT_STATUS = ["Full-time", "Part-time", "Unemployed"]
PAYMENT_HISTORY = ["On Time", "Late <30", "Late 30-60", "Late >60"]

# Weights for categorical variables to create realistic distributions
# Define initial weights
PROVINCE_WEIGHTS_INITIAL = [0.4, 0.15, 0.12, 0.25, 0.02, 0.02, 0.01, 0.01, 0.01, 0.005, 0.001, 0.001, 0.001]
# Normalize weights to ensure they sum to 1
PROVINCE_WEIGHTS = [w / sum(PROVINCE_WEIGHTS_INITIAL) for w in PROVINCE_WEIGHTS_INITIAL]
EMPLOYMENT_WEIGHTS = [0.7, 0.2, 0.1]
PAYMENT_WEIGHTS = [0.8, 0.1, 0.07, 0.03]

def generate_applicant_data():
    """Generate the applicant input dataset."""
    
    # Generate unique applicant IDs
    applicant_ids = [f"APP{i:05d}" for i in range(1, NUM_SAMPLES + 1)]
    
    # Generate features based on specified distributions
    annual_income = np.random.lognormal(mean=11, sigma=0.5, size=NUM_SAMPLES)  # Log-normal, mean ~$60K
    annual_income = np.clip(annual_income, 20000, 200000)  # Clip to range
    
    self_reported_debt = np.random.gamma(shape=2, scale=500, size=NUM_SAMPLES)
    self_reported_debt = np.clip(self_reported_debt, 0, 10000)
    
    self_reported_expenses = np.random.gamma(shape=3, scale=300, size=NUM_SAMPLES)
    self_reported_expenses = np.clip(self_reported_expenses, 0, 10000)
    
    requested_amount = np.random.uniform(1000, 50000, size=NUM_SAMPLES)
    
    age = np.random.normal(loc=40, scale=12, size=NUM_SAMPLES).astype(int)
    age = np.clip(age, 19, 100)
    
    province = np.random.choice(PROVINCES, size=NUM_SAMPLES, p=PROVINCE_WEIGHTS)
    
    employment_status = np.random.choice(EMPLOYMENT_STATUS, size=NUM_SAMPLES, p=EMPLOYMENT_WEIGHTS)
    
    # Months employed depends on employment status
    months_employed = np.zeros(NUM_SAMPLES)
    for i, status in enumerate(employment_status):
        if status == "Unemployed":
            months_employed[i] = 0
        elif status == "Part-time":
            months_employed[i] = np.random.gamma(shape=2, scale=10, size=1)[0]
        else:  # Full-time
            months_employed[i] = np.random.gamma(shape=5, scale=12, size=1)[0]
    
    months_employed = np.clip(months_employed, 0, 600).astype(int)
    
    # Create DataFrame
    applicant_data = pd.DataFrame({
        'applicant_id': applicant_ids,
        'annual_income': annual_income,
        'self_reported_debt': self_reported_debt,
        'self_reported_expenses': self_reported_expenses,
        'requested_amount': requested_amount,
        'age': age,
        'province': province,
        'employment_status': employment_status,
        'months_employed': months_employed
    })
    
    return applicant_data

def generate_credit_data(applicant_ids):
    """Generate the third-party credit dataset."""
    
    # Credit score: normal distribution, mean 680, std 100
    credit_score = np.random.normal(loc=680, scale=100, size=NUM_SAMPLES).astype(int)
    credit_score = np.clip(credit_score, 300, 900)
    
    # Total credit limit: depends on credit score
    total_credit_limit = credit_score * np.random.uniform(30, 70, size=NUM_SAMPLES)
    total_credit_limit = np.clip(total_credit_limit, 0, 50000)
    
    # Credit utilization: beta distribution for realistic utilization rates
    credit_utilization = np.random.beta(a=2, b=5, size=NUM_SAMPLES) * 100
    
    # Number of open accounts: poisson distribution
    num_open_accounts = np.random.poisson(lam=3, size=NUM_SAMPLES)
    num_open_accounts = np.clip(num_open_accounts, 0, 20)
    
    # Number of credit inquiries: poisson distribution
    num_credit_inquiries = np.random.poisson(lam=1, size=NUM_SAMPLES)
    num_credit_inquiries = np.clip(num_credit_inquiries, 0, 10)
    
    # Payment history: weighted choice
    payment_history = np.random.choice(PAYMENT_HISTORY, size=NUM_SAMPLES, p=PAYMENT_WEIGHTS)
    
    # Create DataFrame
    credit_data = pd.DataFrame({
        'applicant_id': applicant_ids,
        'credit_score': credit_score,
        'total_credit_limit': total_credit_limit,
        'credit_utilization': credit_utilization,
        'num_open_accounts': num_open_accounts,
        'num_credit_inquiries': num_credit_inquiries,
        'payment_history': payment_history
    })
    
    return credit_data

def merge_and_generate_targets(applicant_data, credit_data):
    """Merge datasets and generate target variables."""
    
    # Merge datasets on applicant_id
    merged_data = pd.merge(applicant_data, credit_data, on='applicant_id')
    
    # Calculate monthly expenses (simulated spending on credit)
    merged_data['monthly_expenses'] = merged_data['self_reported_expenses'] * np.random.uniform(0.7, 1.3, size=NUM_SAMPLES)
    merged_data['monthly_expenses'] = np.clip(merged_data['monthly_expenses'], 0, 10000)
    
    # Calculate estimated debt
    merged_data['estimated_debt'] = merged_data['total_credit_limit'] * merged_data['credit_utilization'] * 0.03 / 100
    
    # Calculate debt-to-income ratio (DTI)
    monthly_income = merged_data['annual_income'] / 12
    monthly_debt = merged_data['self_reported_debt'] + merged_data['estimated_debt']
    merged_data['dti_ratio'] = (monthly_debt / monthly_income) * 100
    
    # Apply approval rules
    conditions = [
        # Approve if credit score >= 660, DTI <= 40%, payment history "On Time"
        (merged_data['credit_score'] >= 660) & 
        (merged_data['dti_ratio'] <= 40) & 
        (merged_data['payment_history'] == "On Time"),
        
        # Approve if credit score >= 700, DTI <= 45%, any payment history except "Late >60"
        (merged_data['credit_score'] >= 700) & 
        (merged_data['dti_ratio'] <= 45) & 
        (merged_data['payment_history'] != "Late >60"),
        
        # Approve if credit score >= 750, DTI <= 50%
        (merged_data['credit_score'] >= 750) & 
        (merged_data['dti_ratio'] <= 50)
    ]
    
    # Default to denied
    merged_data['approved'] = 0
    
    # Apply each approval condition
    for condition in conditions:
        merged_data.loc[condition & (merged_data['approved'] == 0), 'approved'] = 1
    
    # Add some noise (2-5% of decisions flipped - reduced from 5-10%)
    noise_indices = np.random.choice(
        merged_data.index, 
        size=int(NUM_SAMPLES * np.random.uniform(0.02, 0.05)), 
        replace=False
    )
    merged_data.loc[noise_indices, 'approved'] = 1 - merged_data.loc[noise_indices, 'approved']
    
    # Calculate approved amount (credit limit) for approved applications
    # Base on income, credit score, and requested amount
    merged_data['approved_amount'] = 0
    approved_mask = merged_data['approved'] == 1
    
    # Formula: min(requested amount, (annual income * factor + credit score bonus))
    income_factor = 0.3  # 30% of annual income
    credit_bonus = 50  # $50 per credit score point above 650
    
    merged_data.loc[approved_mask, 'approved_amount'] = np.minimum(
        merged_data.loc[approved_mask, 'requested_amount'],
        (merged_data.loc[approved_mask, 'annual_income'] * income_factor / 12) + 
        np.maximum(0, (merged_data.loc[approved_mask, 'credit_score'] - 650)) * credit_bonus
    )
    
    # Calculate interest rate for approved applications
    # Base rate + adjustments for credit score, DTI, and payment history
    merged_data['interest_rate'] = 0
    
    # Base rate: 8%
    base_rate = 8.0
    
    # Credit score adjustment: -0.01% per point above 650, up to -2.5%
    credit_adjustment = np.minimum(2.5, np.maximum(0, merged_data.loc[approved_mask, 'credit_score'] - 650) * 0.01)
    
    # DTI adjustment: +0.05% per percentage point above 20%, up to +2.5%
    dti_adjustment = np.minimum(2.5, np.maximum(0, merged_data.loc[approved_mask, 'dti_ratio'] - 20) * 0.05)
    
    # Payment history adjustment
    payment_adjustment = pd.Series(0, index=merged_data.loc[approved_mask].index)
    payment_adjustment.loc[merged_data.loc[approved_mask, 'payment_history'] == "Late <30"] = 1.0
    payment_adjustment.loc[merged_data.loc[approved_mask, 'payment_history'] == "Late 30-60"] = 2.0
    payment_adjustment.loc[merged_data.loc[approved_mask, 'payment_history'] == "Late >60"] = 3.0
    
    # Calculate final interest rate
    merged_data.loc[approved_mask, 'interest_rate'] = base_rate - credit_adjustment + dti_adjustment + payment_adjustment
    
    # Ensure interest rate is within bounds (3.0-15.0%)
    merged_data.loc[approved_mask, 'interest_rate'] = np.clip(
        merged_data.loc[approved_mask, 'interest_rate'], 
        3.0, 
        15.0
    )
    
    # Add some random noise to interest rates (±0.5%)
    merged_data.loc[approved_mask, 'interest_rate'] += np.random.uniform(-0.5, 0.5, size=sum(approved_mask))
    merged_data.loc[approved_mask, 'interest_rate'] = np.round(merged_data.loc[approved_mask, 'interest_rate'], 2)
    
    # Add missing data (1-2%)
    # Select random cells to set as NaN
    for column in ['annual_income', 'self_reported_debt', 'credit_score', 'total_credit_limit']:
        missing_indices = np.random.choice(
            merged_data.index, 
            size=int(NUM_SAMPLES * np.random.uniform(0.01, 0.02)), 
            replace=False
        )
        merged_data.loc[missing_indices, column] = np.nan
    
    return merged_data

def main():
    """Main function to generate and save all datasets."""
    
    print("Generating applicant input dataset...")
    applicant_data = generate_applicant_data()
    
    print("Generating third-party credit dataset...")
    credit_data = generate_credit_data(applicant_data['applicant_id'])
    
    print("Merging datasets and generating targets...")
    merged_data = merge_and_generate_targets(applicant_data, credit_data)
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save datasets to CSV
    print("Saving datasets to CSV files...")
    applicant_data.to_csv('data/applicant_data.csv', index=False)
    credit_data.to_csv('data/credit_data.csv', index=False)
    merged_data.to_csv('data/merged_data.csv', index=False)
    
    print(f"Data generation complete. Generated {NUM_SAMPLES} samples.")
    print(f"Approval rate: {merged_data['approved'].mean() * 100:.2f}%")
    
    # Print some statistics
    print("\nDataset Statistics:")
    print(f"Average credit score: {merged_data['credit_score'].mean():.2f}")
    print(f"Average annual income: ${merged_data['annual_income'].mean():.2f}")
    print(f"Average approved credit limit: ${merged_data.loc[merged_data['approved'] == 1, 'approved_amount'].mean():.2f}")
    print(f"Average interest rate: {merged_data.loc[merged_data['approved'] == 1, 'interest_rate'].mean():.2f}%")

if __name__ == "__main__":
    main()
