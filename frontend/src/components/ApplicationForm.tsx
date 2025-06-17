import { useFormik } from 'formik';
import * as Yup from 'yup';
import { FormProps, LOCApplicationData, ProvinceOption, EmploymentStatusOption, PaymentHistoryOption } from '../types';

// Validation schema using Yup
const ApplicationSchema = Yup.object().shape({
  applicant_id: Yup.string()
    .required('Required')
    .max(50, 'Must be 50 characters or less'),
  annual_income: Yup.number()
    .required('Required')
    .min(20000, 'Must be at least $20,000')
    .max(200000, 'Must be at most $200,000'),
  self_reported_debt: Yup.number()
    .required('Required')
    .min(0, 'Must be at least $0')
    .max(10000, 'Must be at most $10,000'),
  self_reported_expenses: Yup.number()
    .required('Required')
    .min(0, 'Must be at least $0')
    .max(10000, 'Must be at most $10,000'),
  requested_amount: Yup.number()
    .required('Required')
    .min(1000, 'Must be at least $1,000')
    .max(50000, 'Must be at most $50,000'),
  age: Yup.number()
    .required('Required')
    .integer('Must be a whole number')
    .min(19, 'Must be at least 19 years old')
    .max(100, 'Must be at most 100 years old'),
  province: Yup.string()
    .required('Required')
    .oneOf(
      ['ON', 'BC', 'AB', 'QC', 'MB', 'SK', 'NS', 'NB', 'NL', 'PE', 'YT', 'NT', 'NU'],
      'Invalid province'
    ),
  employment_status: Yup.string()
    .required('Required')
    .oneOf(
      ['Full-time', 'Part-time', 'Unemployed'],
      'Invalid employment status'
    ) as Yup.StringSchema<'Full-time' | 'Part-time' | 'Unemployed'>,
  months_employed: Yup.number()
    .required('Required')
    .integer('Must be a whole number')
    .min(0, 'Must be at least 0')
    .max(600, 'Must be at most 600'),
  credit_score: Yup.number()
    .required('Required')
    .integer('Must be a whole number')
    .min(300, 'Must be at least 300')
    .max(900, 'Must be at most 900'),
  total_credit_limit: Yup.number()
    .required('Required')
    .min(0, 'Must be at least $0')
    .max(50000, 'Must be at most $50,000'),
  credit_utilization: Yup.number()
    .required('Required')
    .min(0, 'Must be at least 0%')
    .max(100, 'Must be at most 100%'),
  num_open_accounts: Yup.number()
    .required('Required')
    .integer('Must be a whole number')
    .min(0, 'Must be at least 0')
    .max(20, 'Must be at most 20'),
  num_credit_inquiries: Yup.number()
    .required('Required')
    .integer('Must be a whole number')
    .min(0, 'Must be at least 0')
    .max(10, 'Must be at most 10'),
  payment_history: Yup.string()
    .required('Required')
    .oneOf(
      ['On Time', 'Late <30', 'Late 30-60', 'Late >60'],
      'Invalid payment history'
    ) as Yup.StringSchema<'On Time' | 'Late <30' | 'Late 30-60' | 'Late >60'>,
  monthly_expenses: Yup.number()
    .required('Required')
    .min(0, 'Must be at least $0')
    .max(10000, 'Must be at most $10,000'),
});

// Initial form values
const initialValues: LOCApplicationData = {
  applicant_id: '',
  annual_income: 60000,
  self_reported_debt: 1000,
  self_reported_expenses: 2000,
  requested_amount: 10000,
  age: 35,
  province: 'ON',
  employment_status: 'Full-time',
  months_employed: 24,
  credit_score: 700,
  total_credit_limit: 15000,
  credit_utilization: 30,
  num_open_accounts: 3,
  num_credit_inquiries: 1,
  payment_history: 'On Time',
  monthly_expenses: 2500,
};

// Province options
const provinces: ProvinceOption[] = [
  { value: 'ON', label: 'Ontario' },
  { value: 'BC', label: 'British Columbia' },
  { value: 'AB', label: 'Alberta' },
  { value: 'QC', label: 'Quebec' },
  { value: 'MB', label: 'Manitoba' },
  { value: 'SK', label: 'Saskatchewan' },
  { value: 'NS', label: 'Nova Scotia' },
  { value: 'NB', label: 'New Brunswick' },
  { value: 'NL', label: 'Newfoundland and Labrador' },
  { value: 'PE', label: 'Prince Edward Island' },
  { value: 'YT', label: 'Yukon' },
  { value: 'NT', label: 'Northwest Territories' },
  { value: 'NU', label: 'Nunavut' },
];

// Employment status options
const employmentStatuses: EmploymentStatusOption[] = [
  { value: 'Full-time', label: 'Full-time' },
  { value: 'Part-time', label: 'Part-time' },
  { value: 'Unemployed', label: 'Unemployed' },
];

// Payment history options
const paymentHistories: PaymentHistoryOption[] = [
  { value: 'On Time', label: 'On Time' },
  { value: 'Late <30', label: 'Late <30 days' },
  { value: 'Late 30-60', label: 'Late 30-60 days' },
  { value: 'Late >60', label: 'Late >60 days' },
];

const ApplicationForm: React.FC<FormProps> = ({ onSubmit, loading, error }) => {
  const formik = useFormik({
    initialValues,
    validationSchema: ApplicationSchema,
    onSubmit: (values) => {
      onSubmit(values);
    },
  });

  return (
    <div>
      <h2 className="card-title">Line of Credit Application</h2>
      
      <form onSubmit={formik.handleSubmit}>
        {/* Personal Information Section */}
        <div className="mb-6">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Personal Information</h3>
          <div className="divider"></div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="applicant_id" className="form-label">Applicant ID</label>
              <input
                id="applicant_id"
                name="applicant_id"
                type="text"
                className="form-input"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.applicant_id}
              />
              {formik.touched.applicant_id && formik.errors.applicant_id ? (
                <div className="form-error">{formik.errors.applicant_id}</div>
              ) : null}
            </div>
            
            <div>
              <label htmlFor="age" className="form-label">Age</label>
              <input
                id="age"
                name="age"
                type="number"
                className="form-input"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.age}
              />
              {formik.touched.age && formik.errors.age ? (
                <div className="form-error">{formik.errors.age}</div>
              ) : null}
            </div>
            
            <div>
              <label htmlFor="province" className="form-label">Province</label>
              <select
                id="province"
                name="province"
                className="form-input"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.province}
              >
                {provinces.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
              {formik.touched.province && formik.errors.province ? (
                <div className="form-error">{formik.errors.province}</div>
              ) : null}
            </div>
            
            <div>
              <label htmlFor="employment_status" className="form-label">Employment Status</label>
              <select
                id="employment_status"
                name="employment_status"
                className="form-input"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.employment_status}
              >
                {employmentStatuses.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
              {formik.touched.employment_status && formik.errors.employment_status ? (
                <div className="form-error">{formik.errors.employment_status}</div>
              ) : null}
            </div>
            
            <div>
              <label htmlFor="months_employed" className="form-label">Months Employed</label>
              <input
                id="months_employed"
                name="months_employed"
                type="number"
                className="form-input"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.months_employed}
              />
              {formik.touched.months_employed && formik.errors.months_employed ? (
                <div className="form-error">{formik.errors.months_employed}</div>
              ) : null}
            </div>
            
            <div>
              <label htmlFor="annual_income" className="form-label">Annual Income (CAD)</label>
              <input
                id="annual_income"
                name="annual_income"
                type="number"
                className="form-input"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.annual_income}
              />
              {formik.touched.annual_income && formik.errors.annual_income ? (
                <div className="form-error">{formik.errors.annual_income}</div>
              ) : null}
            </div>
          </div>
        </div>
        
        {/* Financial Information Section */}
        <div className="mb-6">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Financial Information</h3>
          <div className="divider"></div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="self_reported_debt" className="form-label">Monthly Debt (CAD)</label>
              <input
                id="self_reported_debt"
                name="self_reported_debt"
                type="number"
                className="form-input"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.self_reported_debt}
              />
              {formik.touched.self_reported_debt && formik.errors.self_reported_debt ? (
                <div className="form-error">{formik.errors.self_reported_debt}</div>
              ) : null}
            </div>
            
            <div>
              <label htmlFor="self_reported_expenses" className="form-label">Self-Reported Expenses (CAD)</label>
              <input
                id="self_reported_expenses"
                name="self_reported_expenses"
                type="number"
                className="form-input"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.self_reported_expenses}
              />
              {formik.touched.self_reported_expenses && formik.errors.self_reported_expenses ? (
                <div className="form-error">{formik.errors.self_reported_expenses}</div>
              ) : null}
            </div>
            
            <div>
              <label htmlFor="monthly_expenses" className="form-label">Monthly Expenses (CAD)</label>
              <input
                id="monthly_expenses"
                name="monthly_expenses"
                type="number"
                className="form-input"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.monthly_expenses}
              />
              {formik.touched.monthly_expenses && formik.errors.monthly_expenses ? (
                <div className="form-error">{formik.errors.monthly_expenses}</div>
              ) : null}
            </div>
            
            <div>
              <label htmlFor="requested_amount" className="form-label">Requested Credit Amount (CAD)</label>
              <input
                id="requested_amount"
                name="requested_amount"
                type="number"
                className="form-input"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.requested_amount}
              />
              {formik.touched.requested_amount && formik.errors.requested_amount ? (
                <div className="form-error">{formik.errors.requested_amount}</div>
              ) : null}
            </div>
          </div>
        </div>
        
        {/* Credit Information Section */}
        <div className="mb-6">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Credit Information</h3>
          <div className="divider"></div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="credit_score" className="form-label">Credit Score</label>
              <input
                id="credit_score"
                name="credit_score"
                type="number"
                className="form-input"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.credit_score}
              />
              {formik.touched.credit_score && formik.errors.credit_score ? (
                <div className="form-error">{formik.errors.credit_score}</div>
              ) : null}
            </div>
            
            <div>
              <label htmlFor="total_credit_limit" className="form-label">Total Credit Limit (CAD)</label>
              <input
                id="total_credit_limit"
                name="total_credit_limit"
                type="number"
                className="form-input"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.total_credit_limit}
              />
              {formik.touched.total_credit_limit && formik.errors.total_credit_limit ? (
                <div className="form-error">{formik.errors.total_credit_limit}</div>
              ) : null}
            </div>
            
            <div>
              <label htmlFor="credit_utilization" className="form-label">Credit Utilization (%)</label>
              <input
                id="credit_utilization"
                name="credit_utilization"
                type="number"
                className="form-input"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.credit_utilization}
              />
              {formik.touched.credit_utilization && formik.errors.credit_utilization ? (
                <div className="form-error">{formik.errors.credit_utilization}</div>
              ) : null}
            </div>
            
            <div>
              <label htmlFor="num_open_accounts" className="form-label">Number of Open Accounts</label>
              <input
                id="num_open_accounts"
                name="num_open_accounts"
                type="number"
                className="form-input"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.num_open_accounts}
              />
              {formik.touched.num_open_accounts && formik.errors.num_open_accounts ? (
                <div className="form-error">{formik.errors.num_open_accounts}</div>
              ) : null}
            </div>
            
            <div>
              <label htmlFor="num_credit_inquiries" className="form-label">Number of Credit Inquiries</label>
              <input
                id="num_credit_inquiries"
                name="num_credit_inquiries"
                type="number"
                className="form-input"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.num_credit_inquiries}
              />
              {formik.touched.num_credit_inquiries && formik.errors.num_credit_inquiries ? (
                <div className="form-error">{formik.errors.num_credit_inquiries}</div>
              ) : null}
            </div>
            
            <div>
              <label htmlFor="payment_history" className="form-label">Payment History</label>
              <select
                id="payment_history"
                name="payment_history"
                className="form-input"
                onChange={formik.handleChange}
                onBlur={formik.handleBlur}
                value={formik.values.payment_history}
              >
                {paymentHistories.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
              {formik.touched.payment_history && formik.errors.payment_history ? (
                <div className="form-error">{formik.errors.payment_history}</div>
              ) : null}
            </div>
          </div>
        </div>
        
        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}
        
        {/* Submit Button */}
        <div className="flex justify-center">
          <button
            type="submit"
            className={`btn btn-primary ${loading ? 'opacity-70 cursor-not-allowed' : ''}`}
            disabled={loading || !formik.isValid}
          >
            {loading ? (
              <span className="flex items-center">
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </span>
            ) : (
              'Submit Application'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default ApplicationForm;
