# Line of Credit (LOC) Approval System

An automated Line of Credit approval application that uses machine learning to predict approval decisions, credit limits, and interest rates.

## Project Overview

This project implements a proof-of-concept system for automating Line of Credit approvals in Canada. The system:

- Takes applicant information through a web interface
- Processes the data using machine learning models
- Returns an approval decision, credit limit, and interest rate within 2 minutes

## Technology Stack

- **Backend**: Django with Django REST Framework
- **Frontend**: React with TypeScript, Vite, and Tailwind CSS
- **Machine Learning**: Python with scikit-learn

## Project Structure

```
loc-approval-system/
├── backend/                 # Django backend
│   ├── loc_project/         # Django project
│   ├── api/                 # Django app for API
│   ├── ml_models/           # Saved ML models
│   └── requirements.txt     # Python dependencies
├── frontend/                # React frontend with TypeScript
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── types.ts
│   ├── index.html
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── tsconfig.json
│   └── package.json         # JS dependencies
└── ml/                      # ML model training
    ├── data_generation.py   # Generate synthetic data
    ├── model_training.py    # Train and save models
    ├── data/                # Generated datasets
    └── requirements.txt     # Python dependencies for ML
```

## Setup and Installation

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm 6+

### ML Component Setup

1. Create a Python virtual environment:
   ```
   cd ml
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Generate synthetic data:
   ```
   python data_generation.py
   ```

3. Train the ML models:
   ```
   python model_training.py
   ```

### Backend Setup

1. Create a Python virtual environment:
   ```
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```
   python manage.py migrate
   ```

3. Start the Django server:
   ```
   python manage.py runserver
   ```

### Frontend Setup

1. Install dependencies:
   ```
   cd frontend
   npm install
   ```

2. Start the development server:
   ```
   npm run dev
   ```

## Usage

1. Open your browser and navigate to `http://localhost:5173`
2. Fill out the application form with sample data
3. Submit the form to receive an approval decision

## API Endpoints

- `POST /api/predict/`: Submit application data and receive a decision

## Data Points

The application collects the following data points:

- **Personal Information**:
  - Applicant ID
  - Age
  - Province
  - Employment Status
  - Months Employed
  - Annual Income

- **Financial Information**:
  - Monthly Debt
  - Self-Reported Expenses
  - Monthly Expenses
  - Requested Credit Amount

- **Credit Information**:
  - Credit Score
  - Total Credit Limit
  - Credit Utilization
  - Number of Open Accounts
  - Number of Credit Inquiries
  - Payment History

## ML Model Details

The system uses three separate models:

1. **Approval Status Model**: Classification model to predict approval/denial
2. **Credit Limit Model**: Regression model to predict credit limit (for approved applications)
3. **Interest Rate Model**: Regression model to predict interest rate (for approved applications)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
