import React from 'react';
import type { VerificationResponse } from '../types';
import ImageWithHighlights from './ImageWithHighlights';

interface Props {
  results: VerificationResponse;
  onReset: () => void;
  imageUrl?: string;
}

const VerificationResults: React.FC<Props> = ({ results, onReset, imageUrl }) => {
  return (
    <div className="space-y-4">
      {/* Overall Result */}
      <div
        className={`p-4 rounded-md border-2 ${
          results.overall_match
            ? 'bg-green-50 border-green-300'
            : 'bg-red-50 border-red-300'
        }`}
      >
        <div className="flex items-start">
          <div className="flex-shrink-0">
            {results.overall_match ? (
              <svg
                className="h-6 w-6 text-green-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            ) : (
              <svg
                className="h-6 w-6 text-red-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            )}
          </div>
          <div className="ml-3">
            <h3
              className={`text-lg font-medium ${
                results.overall_match ? 'text-green-800' : 'text-red-800'
              }`}
            >
              {results.overall_match ? 'Verification Passed' : 'Verification Failed'}
            </h3>
            <p
              className={`mt-1 text-sm ${
                results.overall_match ? 'text-green-700' : 'text-red-700'
              }`}
            >
              {results.message}
            </p>
          </div>
        </div>
      </div>

      {/* Individual Checks */}
      <div className="space-y-3">
        <h4 className="font-semibold text-gray-700">Field Verification Details:</h4>
        {results.checks.map((check, index) => (
          <div
            key={index}
            className={`p-3 rounded-md border ${
              check.matched
                ? 'bg-green-50 border-green-200'
                : 'bg-yellow-50 border-yellow-200'
            }`}
          >
            <div className="flex items-start">
              <div className="flex-shrink-0 mt-0.5">
                {check.matched ? (
                  <svg
                    className="h-5 w-5 text-green-500"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                      clipRule="evenodd"
                    />
                  </svg>
                ) : (
                  <svg
                    className="h-5 w-5 text-yellow-500"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                  >
                    <path
                      fillRule="evenodd"
                      d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                      clipRule="evenodd"
                    />
                  </svg>
                )}
              </div>
              <div className="ml-3 flex-1">
                <p className="text-sm font-medium text-gray-900">
                  {check.field_name}
                </p>
                <p className="mt-1 text-sm text-gray-600">{check.message}</p>
                {!check.matched && (
                  <div className="mt-2 text-xs text-gray-500">
                    <p>Expected: {check.expected_value}</p>
                    <p>Found: {check.found_value || 'Not detected'}</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Extracted Text (Collapsible) */}
      <details className="mt-4">
        <summary className="cursor-pointer text-sm font-medium text-gray-700 hover:text-gray-900">
          View Extracted Text from Label
        </summary>
        <div className="mt-2 p-3 bg-gray-50 rounded-md border border-gray-200">
          <pre className="text-xs text-gray-600 whitespace-pre-wrap break-words">
            {results.extracted_text || 'No text extracted'}
          </pre>
        </div>
      </details>

      {/* Image with Bounding Boxes */}
      {imageUrl && results.word_boxes && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-3">
            Label Image with Highlighted Text
          </h3>
          <ImageWithHighlights imageUrl={imageUrl} verificationResult={results} />
        </div>
      )}

      {/* Reset Button */}
      <button
        onClick={onReset}
        className="w-full mt-4 bg-gray-600 text-white py-2 px-4 rounded-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors"
      >
        Verify Another Label
      </button>
    </div>
  );
};

export default VerificationResults;
