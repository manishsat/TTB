import { useState, useEffect } from 'react';
import type { FormEvent, ChangeEvent } from 'react';
import { verifyLabel } from '../services/api';
import type { VerificationResponse } from '../types';

interface Props {
  onVerificationComplete: (response: VerificationResponse, imageUrl: string) => void;
  onVerificationStart: () => void;
  isLoading: boolean;
}

const LabelVerificationForm: React.FC<Props> = ({
  onVerificationComplete,
  onVerificationStart,
  isLoading,
}) => {
  const [brandName, setBrandName] = useState('');
  const [productClass, setProductClass] = useState('');
  const [alcoholContent, setAlcoholContent] = useState<string>('');
  const [netContents, setNetContents] = useState('');
  const [beverageType, setBeverageType] = useState('spirits');
  const [labelImage, setLabelImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [error, setError] = useState<string>('');

  const handleImageChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (!file.type.startsWith('image/')) {
        setError('Please select a valid image file (JPEG, PNG, etc.)');
        return;
      }
      if (file.size > 10 * 1024 * 1024) { // 10MB limit
        setError('Image file size must be less than 10MB');
        return;
      }
      
      // Revoke old preview URL to free memory
      if (imagePreview) {
        URL.revokeObjectURL(imagePreview);
      }
      
      setLabelImage(file);
      setError('');
      
      // Create new preview using object URL (more efficient and reliable)
      const objectUrl = URL.createObjectURL(file);
      setImagePreview(objectUrl);
    }
  };

  // Cleanup object URL when component unmounts
  useEffect(() => {
    return () => {
      if (imagePreview) {
        URL.revokeObjectURL(imagePreview);
      }
    };
  }, [imagePreview]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');

    // Validation
    if (!brandName.trim()) {
      setError('Brand name is required');
      return;
    }
    if (!productClass.trim()) {
      setError('Product class/type is required');
      return;
    }
    if (!alcoholContent || parseFloat(alcoholContent) <= 0) {
      setError('Valid alcohol content is required');
      return;
    }
    if (!labelImage) {
      setError('Please upload a label image');
      return;
    }

    try {
      onVerificationStart();
      const response = await verifyLabel(
        brandName,
        productClass,
        parseFloat(alcoholContent),
        netContents,
        labelImage,
        beverageType
      );
      onVerificationComplete(response, imagePreview!);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'An error occurred during verification');
      onVerificationComplete({
        success: false,
        overall_match: false,
        message: 'Verification failed',
        extracted_text: '',
        checks: [],
      }, imagePreview || '');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Brand Name */}
      <div>
        <label htmlFor="brandName" className="block text-sm font-medium text-gray-700 mb-1">
          Brand Name <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="brandName"
          value={brandName}
          onChange={(e) => setBrandName(e.target.value)}
          placeholder="e.g., Old Tom Distillery"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          disabled={isLoading}
        />
      </div>

      {/* Beverage Type */}
      <div>
        <label htmlFor="beverageType" className="block text-sm font-medium text-gray-700 mb-1">
          Beverage Type <span className="text-red-500">*</span>
        </label>
        <select
          id="beverageType"
          value={beverageType}
          onChange={(e) => setBeverageType(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          disabled={isLoading}
        >
          <option value="spirits">Distilled Spirits (Whiskey, Vodka, Rum, etc.)</option>
          <option value="wine">Wine</option>
          <option value="beer">Beer</option>
        </select>
        <p className="text-xs text-gray-500 mt-1">
          {beverageType === 'wine' && '(Wine labels require sulfite declaration)'}
          {beverageType === 'beer' && '(Beer labels may include ingredients list)'}
          {beverageType === 'spirits' && '(Standard spirit label verification)'}
        </p>
      </div>

      {/* Product Class/Type */}
      <div>
        <label htmlFor="productClass" className="block text-sm font-medium text-gray-700 mb-1">
          Product Class/Type <span className="text-red-500">*</span>
        </label>
        <input
          type="text"
          id="productClass"
          value={productClass}
          onChange={(e) => setProductClass(e.target.value)}
          placeholder="e.g., Kentucky Straight Bourbon Whiskey"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          disabled={isLoading}
        />
      </div>

      {/* Alcohol Content */}
      <div>
        <label htmlFor="alcoholContent" className="block text-sm font-medium text-gray-700 mb-1">
          Alcohol Content (% ABV) <span className="text-red-500">*</span>
        </label>
        <input
          type="number"
          id="alcoholContent"
          value={alcoholContent}
          onChange={(e) => setAlcoholContent(e.target.value)}
          placeholder="e.g., 45"
          step="0.1"
          min="0"
          max="100"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          disabled={isLoading}
        />
      </div>

      {/* Net Contents */}
      <div>
        <label htmlFor="netContents" className="block text-sm font-medium text-gray-700 mb-1">
          Net Contents (Optional)
        </label>
        <input
          type="text"
          id="netContents"
          value={netContents}
          onChange={(e) => setNetContents(e.target.value)}
          placeholder="e.g., 750 mL or 12 fl oz"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          disabled={isLoading}
        />
      </div>

      {/* Image Upload */}
      <div>
        <label htmlFor="labelImage" className="block text-sm font-medium text-gray-700 mb-1">
          Label Image <span className="text-red-500">*</span>
        </label>
        <input
          type="file"
          id="labelImage"
          accept="image/*"
          onChange={handleImageChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
          disabled={isLoading}
        />
        {imagePreview && (
          <div className="mt-3">
            <img
              src={imagePreview}
              alt="Label preview"
              className="max-w-full h-auto rounded-md border border-gray-300"
            />
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md">
          {error}
        </div>
      )}

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
      >
        {isLoading ? 'Verifying...' : 'Verify Label'}
      </button>

      <p className="text-xs text-gray-500 mt-2">
        <span className="text-red-500">*</span> Required fields
      </p>
    </form>
  );
};

export default LabelVerificationForm;
