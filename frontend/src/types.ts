// Application data interface
export interface LOCApplicationData {
  applicant_id: string;
  annual_income: number;
  self_reported_debt: number;
  self_reported_expenses: number;
  requested_amount: number;
  age: number;
  province: string;
  employment_status: 'Full-time' | 'Part-time' | 'Unemployed';
  months_employed: number;
  credit_score: number;
  total_credit_limit: number;
  credit_utilization: number;
  num_open_accounts: number;
  num_credit_inquiries: number;
  payment_history: 'On Time' | 'Late <30' | 'Late 30-60' | 'Late >60';
  monthly_expenses: number;
}

// Decision result interface
export interface LOCDecisionResult {
  approval_status: boolean;
  credit_limit: number;
  interest_rate: number;
  reason?: string;
}

// Province option interface
export interface ProvinceOption {
  value: string;
  label: string;
}

// Employment status option interface
export interface EmploymentStatusOption {
  value: 'Full-time' | 'Part-time' | 'Unemployed';
  label: string;
}

// Payment history option interface
export interface PaymentHistoryOption {
  value: 'On Time' | 'Late <30' | 'Late 30-60' | 'Late >60';
  label: string;
}

// Form props interface
export interface FormProps {
  onSubmit: (data: LOCApplicationData) => void;
  loading: boolean;
  error: string | null;
}

// Result display props interface
export interface ResultDisplayProps {
  result: LOCDecisionResult;
  onReset: () => void;
}
