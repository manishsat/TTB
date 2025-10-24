import axios from 'axios';
import type { VerificationResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const verifyLabel = async (
  brandName: string,
  productClass: string,
  alcoholContent: number,
  netContents: string,
  labelImage: File
): Promise<VerificationResponse> => {
  const formData = new FormData();
  formData.append('brand_name', brandName);
  formData.append('product_class', productClass);
  formData.append('alcohol_content', alcoholContent.toString());
  
  if (netContents) {
    formData.append('net_contents', netContents);
  }
  
  formData.append('label_image', labelImage);

  const response = await axios.post<VerificationResponse>(
    `${API_BASE_URL}/api/verify`,
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  );

  return response.data;
};
