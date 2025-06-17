import { ResultDisplayProps } from '../types';

const ResultDisplay: React.FC<ResultDisplayProps> = ({ result, onReset }) => {
  const { approval_status, credit_limit, interest_rate, reason } = result;
  
  // Format currency
  const formatCurrency = (amount: number): string => {
    return new Intl.NumberFormat('en-CA', {
      style: 'currency',
      currency: 'CAD',
      minimumFractionDigits: 2,
    }).format(amount);
  };
  
  return (
    <div>
      <h2 className="card-title">Application Result</h2>
      
      <div className="flex justify-center mb-6">
        {approval_status ? (
          <span className="inline-flex items-center px-4 py-2 rounded-full text-lg font-semibold bg-green-100 text-green-800">
            <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path>
            </svg>
            APPROVED
          </span>
        ) : (
          <span className="inline-flex items-center px-4 py-2 rounded-full text-lg font-semibold bg-red-100 text-red-800">
            <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd"></path>
            </svg>
            DENIED
          </span>
        )}
      </div>
      
      {approval_status ? (
        <div className="bg-gray-50 rounded-lg p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <p className="text-sm text-gray-500 mb-1">Credit Limit</p>
              <p className="text-2xl font-bold text-primary">{formatCurrency(credit_limit)}</p>
            </div>
            
            <div>
              <p className="text-sm text-gray-500 mb-1">Interest Rate</p>
              <p className="text-2xl font-bold text-primary">{interest_rate.toFixed(2)}%</p>
            </div>
          </div>
          
          <div className="divider"></div>
          
          <p className="text-gray-700 mb-4">
            Congratulations! Your Line of Credit application has been approved. 
            You can access your funds within 1-2 business days.
          </p>
          
          <div className="mt-4">
            <h4 className="text-sm font-medium text-gray-700 mb-2">Important Information:</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              <li className="flex items-start">
                <span className="text-primary mr-2">•</span>
                <span>Your credit limit and interest rate are based on your application details and credit history.</span>
              </li>
              <li className="flex items-start">
                <span className="text-primary mr-2">•</span>
                <span>The interest rate is variable and may change based on market conditions.</span>
              </li>
              <li className="flex items-start">
                <span className="text-primary mr-2">•</span>
                <span>Minimum monthly payment is 3% of the outstanding balance.</span>
              </li>
            </ul>
          </div>
        </div>
      ) : (
        <div className="bg-gray-50 rounded-lg p-6 mb-6">
          <h3 className="text-xl font-semibold text-red-600 mb-4">Application Denied</h3>
          
          <p className="text-gray-700 mb-4">
            We're sorry, but we are unable to approve your Line of Credit application at this time.
          </p>
          
          {reason && (
            <p className="text-gray-700 mb-4">
              <strong>Reason:</strong> {reason}
            </p>
          )}
          
          <div className="divider"></div>
          
          <h4 className="text-sm font-medium text-gray-700 mb-2">What you can do next:</h4>
          <ul className="text-sm text-gray-600 space-y-1">
            <li className="flex items-start">
              <span className="text-primary mr-2">•</span>
              <span>Review your credit report for any errors</span>
            </li>
            <li className="flex items-start">
              <span className="text-primary mr-2">•</span>
              <span>Work on improving your credit score</span>
            </li>
            <li className="flex items-start">
              <span className="text-primary mr-2">•</span>
              <span>Reduce your existing debt</span>
            </li>
            <li className="flex items-start">
              <span className="text-primary mr-2">•</span>
              <span>You may reapply after 90 days</span>
            </li>
          </ul>
        </div>
      )}
      
      <div className="flex justify-center">
        <button
          onClick={onReset}
          className="btn btn-primary"
        >
          Start New Application
        </button>
      </div>
    </div>
  );
};

export default ResultDisplay;
