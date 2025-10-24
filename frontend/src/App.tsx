import { useState } from 'react';
import LabelVerificationForm from './components/LabelVerificationForm';
import VerificationResults from './components/VerificationResults';
import type { VerificationResponse } from './types';

function App() {
  const [results, setResults] = useState<VerificationResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [formKey, setFormKey] = useState(0); // Key to force form reset
  const [labelImageUrl, setLabelImageUrl] = useState<string | null>(null);

  const handleVerificationComplete = (response: VerificationResponse, imageUrl: string) => {
    setResults(response);
    setLabelImageUrl(imageUrl);
    setIsLoading(false);
  };

  const handleVerificationStart = () => {
    setIsLoading(true);
    setResults(null);
  };

  const handleReset = () => {
    setResults(null);
    setLabelImageUrl(null);
    setFormKey(prev => prev + 1); // Increment key to reset form
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            TTB Label Verification System
          </h1>
          <p className="text-gray-600">
            Alcohol and Tobacco Tax and Trade Bureau (TTB) Label Approval Simulator
          </p>
        </header>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Form Section */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              Label Application Form
            </h2>
            <LabelVerificationForm
              key={formKey}
              onVerificationComplete={handleVerificationComplete}
              onVerificationStart={handleVerificationStart}
              isLoading={isLoading}
            />
          </div>

          {/* Results Section */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-800 mb-4">
              Verification Results
            </h2>
            {isLoading ? (
              <div className="flex flex-col items-center justify-center py-12">
                <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-indigo-600"></div>
                <p className="mt-4 text-gray-600">Processing label image...</p>
              </div>
            ) : results ? (
              <VerificationResults results={results} onReset={handleReset} imageUrl={labelImageUrl || undefined} />
            ) : (
              <div className="flex items-center justify-center py-12 text-gray-400">
                <p>Submit the form to see verification results</p>
              </div>
            )}
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-8 text-center text-gray-600 text-sm">
          <p>
            This is a simplified simulation for educational purposes. 
            Actual TTB label approval involves more comprehensive review.
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;

