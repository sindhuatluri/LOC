import { useState } from 'react';
import ApplicationForm from './components/ApplicationForm';
import ResultDisplay from './components/ResultDisplay';
import { LOCApplicationData, LOCDecisionResult } from './types';

function App() {
  const [result, setResult] = useState<LOCDecisionResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (formData: LOCApplicationData) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/api/predict/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'An error occurred while processing your application');
      }
      
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
      console.error('Error submitting application:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-center text-gray-900 mb-8">
          Line of Credit Approval System
        </h1>
        
        <div className="card">
          {!result ? (
            <ApplicationForm 
              onSubmit={handleSubmit} 
              loading={loading} 
              error={error} 
            />
          ) : (
            <ResultDisplay 
              result={result} 
              onReset={handleReset} 
            />
          )}
        </div>
        
        <div className="mt-8 text-center text-gray-500 text-sm">
          © {new Date().getFullYear()} Line of Credit Approval System
        </div>
      </div>
    </div>
  );
}

export default App;
