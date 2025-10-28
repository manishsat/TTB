"""
OCR (Optical Character Recognition) module
Handles text extraction from label images using Tesseract
"""
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
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
    Extract text from image using Tesseract OCR with enhanced preprocessing
    Tries multiple strategies to handle decorative fonts and various label designs
    
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
        
        all_text_lines = set()  # Use set to avoid duplicates
        width, height = image.size
        
        # Strategy 1: Standard OCR with PSM 3 (fully automatic)
        custom_config = r'--oem 3 --psm 3'
        text1 = pytesseract.image_to_string(image, config=custom_config)
        all_text_lines.update(line.strip() for line in text1.split('\n') if line.strip())
        
        # Strategy 2: Try PSM 4 (single column of text) - good for vertically stacked text
        text2 = pytesseract.image_to_string(image, config=r'--oem 3 --psm 4')
        all_text_lines.update(line.strip() for line in text2.split('\n') if line.strip())
        
        # Strategy 3: Enhanced contrast (helps with low-contrast decorative text)
        enhancer = ImageEnhance.Contrast(image)
        enhanced = enhancer.enhance(2.5)
        text3 = pytesseract.image_to_string(enhanced, config=custom_config)
        all_text_lines.update(line.strip() for line in text3.split('\n') if line.strip())
        
        # Strategy 4: Sharpening (helps with slightly blurry decorative fonts)
        sharpened = image.filter(ImageFilter.SHARPEN)
        text4 = pytesseract.image_to_string(sharpened, config=custom_config)
        all_text_lines.update(line.strip() for line in text4.split('\n') if line.strip())
        
        # Strategy 5: Scale up 1.5x (helps with small text or low resolution)
        scaled = image.resize((int(width * 1.5), int(height * 1.5)), Image.Resampling.LANCZOS)
        text5 = pytesseract.image_to_string(scaled, config=custom_config)
        all_text_lines.update(line.strip() for line in text5.split('\n') if line.strip())
        
        # Strategy 6: CRITICAL - Crop top 40% and use PSM 6 (uniform block)
        # This catches large decorative brand names that PSM 3 misses
        top_area = image.crop((int(width * 0.05), int(height * 0.1), int(width * 0.95), int(height * 0.4)))
        text6 = pytesseract.image_to_string(top_area, config=r'--oem 3 --psm 6')
        top_lines = [line.strip() for line in text6.split('\n') if line.strip() and len(line.strip()) > 2]
        if top_lines:
            logger.info(f"Top area OCR (PSM 6) found: {top_lines}")
            all_text_lines.update(top_lines)
        
        # Strategy 7: Try PSM 11 on top area (sparse text with OSD)
        # Sometimes works better with decorative fonts spread out
        text7a = pytesseract.image_to_string(top_area, config=r'--oem 3 --psm 11')
        psm11_lines = [line.strip() for line in text7a.split('\n') if line.strip() and len(line.strip()) > 2]
        if psm11_lines:
            logger.info(f"Top area OCR (PSM 11) found: {psm11_lines}")
            all_text_lines.update(psm11_lines)
        
        # Strategy 8: Binary threshold on top area (high contrast for decorative text)
        gray_top = top_area.convert('L')
        binary_top = gray_top.point(lambda x: 0 if x < 180 else 255, '1')
        text8 = pytesseract.image_to_string(binary_top, config=r'--oem 3 --psm 6')
        binary_lines = [line.strip() for line in text8.split('\n') if line.strip() and len(line.strip()) > 2]
        if binary_lines:
            logger.info(f"Binary threshold OCR found: {binary_lines}")
            all_text_lines.update(binary_lines)
        
        # Strategy 9: Inverted contrast on top area (alternative for decorative text)
        inverted_top = ImageOps.invert(gray_top)
        contrast_inv = ImageEnhance.Contrast(inverted_top).enhance(3.0)
        text9 = pytesseract.image_to_string(contrast_inv, config=r'--oem 3 --psm 6')
        inv_lines = [line.strip() for line in text9.split('\n') if line.strip() and len(line.strip()) > 2]
        if inv_lines:
            logger.info(f"Inverted top area OCR found: {inv_lines}")
            all_text_lines.update(inv_lines)
        
        # Build combined text preserving logical order
        # Standard OCR (text1) gives us the baseline order
        base_lines = [line.strip() for line in text1.split('\n') if line.strip()]
        
        # Add any new lines found by other strategies at the top
        # (assumes brand name is at top and most likely to be missed)
        new_lines = all_text_lines - set(base_lines)
        
        if new_lines:
            logger.info(f"Enhanced OCR found {len(new_lines)} additional lines: {list(new_lines)[:5]}")
            # Sort new lines to put longer ones first (likely to be brand names)
            sorted_new = sorted(new_lines, key=len, reverse=True)
            combined = '\n'.join(sorted_new) + '\n' + '\n'.join(base_lines)
        else:
            combined = '\n'.join(base_lines)
        
        logger.info(f"OCR extracted {len(combined)} characters using 9 preprocessing strategies")
        logger.info(f"Total unique lines found: {len(all_text_lines)}")
        
        return combined.strip()
        
    except Exception as e:
        logger.error(f"Error extracting text from image: {str(e)}")
        raise Exception(f"OCR processing failed: {str(e)}")


def extract_text_with_boxes(image_bytes: bytes) -> tuple[str, dict]:
    """
    Extract text from image with bounding box coordinates for highlighting
    Uses enhanced multi-strategy OCR for better text extraction
    
    Args:
        image_bytes: Image file as bytes
        
    Returns:
        Tuple of (extracted_text, word_boxes_dict)
        word_boxes_dict: {word: {'left': x, 'top': y, 'width': w, 'height': h, 'conf': confidence}}
    """
    try:
        # Use the enhanced multi-strategy OCR for text extraction
        enhanced_text = extract_text_from_image(image_bytes)
        
        # Still need to get bounding boxes from standard OCR
        # (bounding boxes require image_to_data which is only available with standard OCR)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Get detailed word-level data with bounding boxes using standard OCR
        custom_config = r'--oem 3 --psm 3'
        data = pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)
        
        # Build word boxes dictionary
        word_boxes = {}
        n_boxes = len(data['text'])
        
        for i in range(n_boxes):
            word_text = data['text'][i].strip()
            conf = int(data['conf'][i])
            
            # Only include words with good confidence (> 30) and non-empty text
            if word_text and conf > 30:
                # Store bounding box info for each word
                box_info = {
                    'left': data['left'][i],
                    'top': data['top'][i],
                    'width': data['width'][i],
                    'height': data['height'][i],
                    'conf': conf
                }
                
                word_lower = word_text.lower()
                if word_lower in word_boxes:
                    # Word already exists, store multiple occurrences
                    if isinstance(word_boxes[word_lower], list):
                        word_boxes[word_lower].append(box_info)
                    else:
                        # Convert to list
                        word_boxes[word_lower] = [word_boxes[word_lower], box_info]
                else:
                    word_boxes[word_lower] = box_info
        
        logger.info(f"Enhanced OCR extracted {len(enhanced_text)} characters with {len(word_boxes)} bounding boxes")
        
        # Return enhanced text with bounding boxes from standard OCR
        return enhanced_text.strip(), word_boxes
        
    except Exception as e:
        logger.error(f"Error extracting text with boxes: {str(e)}")
        raise Exception(f"OCR processing failed: {str(e)}")
