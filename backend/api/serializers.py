"""
Serializers for the LOC Approval API.
"""

from rest_framework import serializers

class LOCApplicationSerializer(serializers.Serializer):
    """
    Serializer for LOC application data.
    Validates input data according to the specified ranges and formats.
    """
    
    # Applicant information
    applicant_id = serializers.CharField(max_length=50)
    annual_income = serializers.FloatField(min_value=20000, max_value=200000)
    self_reported_debt = serializers.FloatField(min_value=0, max_value=10000)
    self_reported_expenses = serializers.FloatField(min_value=0, max_value=10000)
    requested_amount = serializers.FloatField(min_value=1000, max_value=50000)
    age = serializers.IntegerField(min_value=19, max_value=100)
    province = serializers.CharField(max_length=2)
    employment_status = serializers.ChoiceField(
        choices=["Full-time", "Part-time", "Unemployed"]
    )
    months_employed = serializers.IntegerField(min_value=0, max_value=600)
    
    # Credit information
    credit_score = serializers.IntegerField(min_value=300, max_value=900)
    total_credit_limit = serializers.FloatField(min_value=0, max_value=50000)
    credit_utilization = serializers.FloatField(min_value=0, max_value=100)
    num_open_accounts = serializers.IntegerField(min_value=0, max_value=20)
    num_credit_inquiries = serializers.IntegerField(min_value=0, max_value=10)
    payment_history = serializers.ChoiceField(
        choices=["On Time", "Late <30", "Late 30-60", "Late >60"]
    )
    monthly_expenses = serializers.FloatField(min_value=0, max_value=10000)
    
    def validate_province(self, value):
        """Validate that province is a valid Canadian province code."""
        valid_provinces = [
            "ON", "BC", "AB", "QC", "MB", "SK", "NS", "NB", "NL", "PE", "YT", "NT", "NU"
        ]
        if value not in valid_provinces:
            raise serializers.ValidationError(
                f"Invalid province code. Must be one of: {', '.join(valid_provinces)}"
            )
        return value

class LOCDecisionSerializer(serializers.Serializer):
    """
    Serializer for LOC decision output.
    """
    
    approval_status = serializers.BooleanField()
    credit_limit = serializers.FloatField(min_value=0)
    interest_rate = serializers.FloatField(min_value=0)
    reason = serializers.CharField(required=False, allow_blank=True)
