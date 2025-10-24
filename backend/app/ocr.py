"""
OCR (Optical Character Recognition) module
Handles text extraction from label images using Tesseract
"""
import pytesseract
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)

# Image quality thresholds
MIN_WIDTH = 400
MIN_HEIGHT = 400
MIN_FILE_SIZE = 5000  # 5KB
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def validate_image_quality(image_bytes: bytes) -> tuple[bool, str]:
    """
    Validate image quality before OCR processing
    
    Args:
        image_bytes: Image file as bytes
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # Check file size
        file_size = len(image_bytes)
        if file_size < MIN_FILE_SIZE:
            return False, f"Image file too small ({file_size} bytes). Minimum {MIN_FILE_SIZE} bytes required for quality OCR."
        
        if file_size > MAX_FILE_SIZE:
            return False, f"Image file too large ({file_size / 1024 / 1024:.1f}MB). Maximum {MAX_FILE_SIZE / 1024 / 1024}MB allowed."
        
        # Open and check image dimensions
        image = Image.open(io.BytesIO(image_bytes))
        width, height = image.size
        
        if width < MIN_WIDTH or height < MIN_HEIGHT:
            return False, f"Image resolution too low ({width}x{height}). Minimum {MIN_WIDTH}x{MIN_HEIGHT} pixels required for accurate OCR."
        
        # Check if image is too small in aspect ratio (likely a thumbnail or icon)
        if width < 200 or height < 200:
            return False, "Image appears to be a thumbnail. Please upload a full-size label image."
        
        # Check color mode
        if image.mode not in ('RGB', 'RGBA', 'L', 'P'):
            return False, f"Unsupported image color mode '{image.mode}'. Please use RGB, RGBA, or grayscale images."
        
        logger.info(f"Image quality validation passed: {width}x{height}, {file_size} bytes, mode: {image.mode}")
        return True, "OK"
        
    except Exception as e:
        logger.error(f"Error validating image quality: {str(e)}")
        return False, f"Invalid image file: {str(e)}"


def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extract text from image using Tesseract OCR
    
    Args:
        image_bytes: Image file as bytes
        
    Returns:
        Extracted text from the image
    """
    try:
        # Open image from bytes
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary (handles different image formats)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Perform OCR
        # PSM 3 = Fully automatic page segmentation (better for labels with large headings)
        # OEM 3 = Default OCR Engine Mode (uses both legacy and LSTM engines)
        custom_config = r'--oem 3 --psm 3'
        text = pytesseract.image_to_string(image, config=custom_config)
        
        logger.info(f"OCR extracted {len(text)} characters")
        
        return text.strip()
        
    except Exception as e:
        logger.error(f"Error extracting text from image: {str(e)}")
        raise Exception(f"OCR processing failed: {str(e)}")
