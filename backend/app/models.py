"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class BoundingBox(BaseModel):
    """Bounding box coordinates for highlighting"""
    left: int = Field(..., description="Left coordinate (x)")
    top: int = Field(..., description="Top coordinate (y)")
    width: int = Field(..., description="Width of bounding box")
    height: int = Field(..., description="Height of bounding box")
    conf: int = Field(..., description="OCR confidence (0-100)")


class FieldCheck(BaseModel):
    """Individual field verification result"""
    field_name: str = Field(..., description="Name of the field being checked")
    expected_value: str = Field(..., description="Expected value from form")
    found_value: Optional[str] = Field(None, description="Value found in image")
    matched: bool = Field(..., description="Whether the field matched")
    message: str = Field(..., description="Detailed message about the check")
    bounding_boxes: Optional[List[BoundingBox]] = Field(None, description="Bounding boxes where text was found")


class VerificationResponse(BaseModel):
    """Complete verification response"""
    success: bool = Field(..., description="Whether the request was processed successfully")
    overall_match: bool = Field(..., description="Whether all required fields matched")
    message: str = Field(..., description="Overall result message")
    extracted_text: str = Field(..., description="Raw text extracted from image")
    checks: List[FieldCheck] = Field(..., description="Individual field verification results")
    word_boxes: Optional[Dict[str, Any]] = Field(None, description="All word-level bounding boxes for highlighting")
