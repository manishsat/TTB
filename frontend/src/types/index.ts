export interface FieldCheck {
  field_name: string;
  expected_value: string;
  found_value: string | null;
  matched: boolean;
  message: string;
}

export interface VerificationResponse {
  success: boolean;
  overall_match: boolean;
  message: string;
  extracted_text: string;
  checks: FieldCheck[];
}

export interface FormData {
  brandName: string;
  productClass: string;
  alcoholContent: number;
  netContents: string;
  labelImage: File | null;
}
