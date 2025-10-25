export interface BoundingBox {
  left: number;
  top: number;
  width: number;
  height: number;
  conf: number;
}

export interface FieldCheck {
  field_name: string;
  expected_value: string;
  found_value: string | null;
  matched: boolean;
  message: string;
  bounding_boxes?: BoundingBox[];
  violations?: string[];
}

export interface VerificationResponse {
  success: boolean;
  overall_match: boolean;
  message: string;
  extracted_text: string;
  checks: FieldCheck[];
  word_boxes?: Record<string, BoundingBox | BoundingBox[]>;
}

export interface FormData {
  brandName: string;
  productClass: string;
  alcoholContent: number;
  netContents: string;
  labelImage: File | null;
}
