"""
Views for the LOC Approval API.
"""

import os
import time
import logging
import numpy as np
import pandas as pd
import joblib
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import LOCApplicationSerializer, LOCDecisionSerializer

# Configure logging
logger = logging.getLogger(__name__)

# Load ML models
try:
    APPROVAL_MODEL = joblib.load(os.path.join(settings.ML_MODELS_DIR, 'approval_model.joblib'))
    CREDIT_LIMIT_MODEL = joblib.load(os.path.join(settings.ML_MODELS_DIR, 'credit_limit_model.joblib'))
    INTEREST_RATE_MODEL = joblib.load(os.path.join(settings.ML_MODELS_DIR, 'interest_rate_model.joblib'))
    MODELS_LOADED = True
    logger.info("ML models loaded successfully")
except Exception as e:
    logger.error(f"Error loading ML models: {str(e)}")
    MODELS_LOADED = False

class PredictView(APIView):
    """
    API view for predicting LOC approval, credit limit, and interest rate.
    """
    
    def post(self, request):
        """
        Process a POST request with LOC application data and return a decision.
        """
        # Record start time for performance monitoring
        start_time = time.time()
        
        # Validate input data
        serializer = LOCApplicationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid input data", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if models are loaded
        if not MODELS_LOADED:
            return Response(
                {"error": "ML models not loaded. Please check server logs."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        try:
            # Extract validated data
            data = serializer.validated_data
            
            # Calculate estimated debt
            estimated_debt = data['total_credit_limit'] * data['credit_utilization'] * 0.03 / 100
            
            # Prepare feature set for prediction
            features = {
                'annual_income': data['annual_income'],
                'self_reported_debt': data['self_reported_debt'],
                'self_reported_expenses': data['self_reported_expenses'],
                'requested_amount': data['requested_amount'],
                'age': data['age'],
                'province': data['province'],
                'employment_status': data['employment_status'],
                'months_employed': data['months_employed'],
                'credit_score': data['credit_score'],
                'total_credit_limit': data['total_credit_limit'],
                'credit_utilization': data['credit_utilization'],
                'num_open_accounts': data['num_open_accounts'],
                'num_credit_inquiries': data['num_credit_inquiries'],
                'payment_history': data['payment_history'],
                'monthly_expenses': data['monthly_expenses'],
                'estimated_debt': estimated_debt,
                'dti_ratio': ((data['self_reported_debt'] + estimated_debt) / (data['annual_income'] / 12)) * 100
            }
            
            # Convert to DataFrame for prediction
            features_df = pd.DataFrame([features])
            
            # Make predictions
            approval_status = APPROVAL_MODEL.predict(features_df)[0]
            
            # Initialize response data
            response_data = {
                'approval_status': bool(approval_status),
                'credit_limit': 0.0,
                'interest_rate': 0.0,
                'reason': ''
            }
            
            # If approved, predict credit limit and interest rate
            if approval_status:
                credit_limit = CREDIT_LIMIT_MODEL.predict(features_df)[0]
                interest_rate = INTEREST_RATE_MODEL.predict(features_df)[0]
                
                # Round and format results
                credit_limit = round(float(credit_limit), 2)
                interest_rate = round(float(interest_rate), 2)
                
                response_data['credit_limit'] = credit_limit
                response_data['interest_rate'] = interest_rate
            else:
                # Provide reason for denial
                if features['credit_score'] < 660:
                    response_data['reason'] = "Denied due to low credit score"
                elif features['dti_ratio'] > 50:
                    response_data['reason'] = "Denied due to high debt-to-income ratio"
                elif features['payment_history'] == "Late >60":
                    response_data['reason'] = "Denied due to payment history"
                else:
                    response_data['reason'] = "Denied based on multiple factors"
            
            # Validate output data
            output_serializer = LOCDecisionSerializer(data=response_data)
            if not output_serializer.is_valid():
                logger.error(f"Output validation error: {output_serializer.errors}")
                return Response(
                    {"error": "Error in prediction output", "details": output_serializer.errors},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Calculate processing time
            processing_time = time.time() - start_time
            logger.info(f"Prediction completed in {processing_time:.2f} seconds")
            
            # Return response
            return Response(output_serializer.validated_data)
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return Response(
                {"error": "Error processing prediction", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
