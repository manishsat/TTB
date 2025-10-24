"""
TTB Label Verification API
Main FastAPI application entry point
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import logging

from app.ocr import extract_text_from_image, validate_image_quality, extract_text_with_boxes
from app.verification import verify_label_data
from app.models import VerificationResponse, BeverageType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="TTB Label Verification API",
    description="AI-powered alcohol label verification system",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "TTB Label Verification API is running",
        "version": "1.0.0"
    }


@app.post("/api/verify", response_model=VerificationResponse)
async def verify_label(
    brand_name: str = Form(...),
    product_class: str = Form(...),
    alcohol_content: float = Form(...),
    net_contents: Optional[str] = Form(None),
    beverage_type: str = Form("spirits"),
    label_image: UploadFile = File(...)
):
    """
    Verify alcohol label against form data with beverage-type specific rules
    
    Args:
        brand_name: Brand name from form
        product_class: Product class/type from form
        alcohol_content: Alcohol by volume (ABV) percentage
        net_contents: Net contents/volume (optional)
        beverage_type: Type of beverage (spirits, wine, beer)
        label_image: Uploaded label image file
    
    Returns:
        VerificationResponse with match results and details
    """
    try:
        logger.info(f"Processing verification request for {beverage_type} - brand: {brand_name}")
        
        # Validate file type
        if not label_image.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="Uploaded file must be an image (JPEG, PNG, etc.)"
            )
        
        # Read image file
        image_bytes = await label_image.read()
        
        # Validate image quality before OCR
        logger.info("Validating image quality...")
        is_valid, validation_message = validate_image_quality(image_bytes)
        
        if not is_valid:
            logger.warning(f"Image quality validation failed: {validation_message}")
            return VerificationResponse(
                success=False,
                overall_match=False,
                message=f"⚠️ Image quality check failed: {validation_message}",
                extracted_text="",
                checks=[]
            )
        
        # Extract text from image using OCR with bounding boxes
        logger.info("Extracting text from label image...")
        extracted_text, word_boxes = extract_text_with_boxes(image_bytes)
        
        if not extracted_text or len(extracted_text.strip()) < 10:
            logger.warning("Could not extract sufficient text from image")
            return VerificationResponse(
                success=False,
                overall_match=False,
                message="⚠️ Could not read text from the label image. Please try a clearer image.",
                extracted_text=extracted_text,
                checks=[],
                word_boxes={}
            )
        
        logger.info(f"Extracted text length: {len(extracted_text)} characters")
        logger.info(f"OCR EXTRACTED TEXT:\n{extracted_text}\n")
        
        # Convert beverage_type string to enum
        try:
            bev_type = BeverageType(beverage_type.lower())
        except ValueError:
            bev_type = BeverageType.SPIRITS  # Default to spirits
        
        # Verify extracted data against form inputs with beverage-specific rules
        verification_result = verify_label_data(
            extracted_text=extracted_text,
            brand_name=brand_name,
            product_class=product_class,
            alcohol_content=alcohol_content,
            net_contents=net_contents,
            beverage_type=bev_type
        )
        
        # Add word boxes to response for frontend highlighting
        verification_result.word_boxes = word_boxes
        
        logger.info(f"Verification complete. Match: {verification_result.overall_match}")
        
        return verification_result
        
    except Exception as e:
        logger.error(f"Error processing verification: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing verification: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
