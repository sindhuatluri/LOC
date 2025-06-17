#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for the LOC Approval API.
This script sends a test application to the API and prints the response.
"""

import requests
import json
import sys

# Test application data
test_application = {
    "applicant_id": "2",
    "annual_income": 200000,
    "self_reported_debt": 1000,
    "self_reported_expenses": 2000,
    "requested_amount": 10000,
    "age": 35,
    "province": "ON",
    "employment_status": "Full-time",
    "months_employed": 24,
    "credit_score": 700,
    "total_credit_limit": 15000,
    "credit_utilization": 30,
    "num_open_accounts": 3,
    "num_credit_inquiries": 1,
    "payment_history": "On Time",
    "monthly_expenses": 2500
}

def test_api(url="http://localhost:8000/api/predict/"):
    """Send a test application to the API and print the response."""
    
    print("Sending test application to API...")
    print(f"URL: {url}")
    print(f"Application data: {json.dumps(test_application, indent=2)}")
    
    try:
        response = requests.post(url, json=test_application)
        
        print("\nResponse:")
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Approval status: {result['approval_status']}")
            if result['approval_status']:
                print(f"Credit limit: ${result['credit_limit']}")
                print(f"Interest rate: {result['interest_rate']}%")
            else:
                print(f"Reason: {result['reason']}")
        else:
            print(f"Error: {response.text}")
        
        return response.status_code == 200 and response.json()['approval_status']
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Check if the API URL is provided as a command-line argument
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/api/predict/"
    
    # Run the test
    success = test_api(url)
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)
