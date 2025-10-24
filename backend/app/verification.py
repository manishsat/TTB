"""
Label verification logic
Compares extracted OCR text with form data

MATCHING ASSUMPTIONS & RULES:
============================

1. BRAND NAME MATCHING:
   - Uses fuzzy matching with 0.75 similarity threshold
   - Case-insensitive comparison
   - Allows minor OCR errors (e.g., "Eagle Peak" matches "Eagie Peak")
   - Normalized whitespace (extra spaces ignored)

2. PRODUCT CLASS/TYPE MATCHING:
   - Uses fuzzy matching with 0.75 similarity threshold
   - Case-insensitive comparison
   - Matches "very close/identical" product types
   - Example: "Bourbon Whiskey" matches "bourbon whiskey" or "Bourbon  Whiskey"

3. ALCOHOL CONTENT MATCHING:
   - Extracts numeric percentage from OCR text
   - Allows ±0.5% tolerance for OCR reading errors
   - Recognizes multiple formats:
     * "45%", "45 %", "45% ABV", "45% Alc./Vol."
     * "alc. 45", "alcohol 45"
   - Must match the form input within tolerance

4. NET CONTENTS MATCHING:
   - Extracts volume numbers from text (mL, L, oz, fl oz)
   - Exact number comparison (no tolerance)
   - Example: "750 mL" on label must match "750" in form
   - Prevents substring matching (1750 won't match 750)

5. GOVERNMENT WARNING:
   - Checks for mandatory warning statement
   - Looks for keywords: "government warning", "surgeon general", 
     "pregnant", "birth defects", "operating machinery"
   - Uses fuzzy matching with 0.85 threshold
   - Currently shows warning if missing but doesn't fail verification
     (In production, this would be mandatory and fail the approval)

6. TEXT NORMALIZATION:
   - All text comparisons are case-insensitive
   - Extra whitespace is normalized (collapsed to single spaces)
   - Leading/trailing spaces removed
   - Uses Levenshtein distance for fuzzy matching to handle OCR errors

OCR CONFIGURATION:
==================
- Using Tesseract OCR with PSM 3 (fully automatic page segmentation)
- PSM 3 captures all text including large headers/titles
- OEM 3 (default engine mode using both legacy and LSTM)
"""
import re
import logging
from typing import Optional
from Levenshtein import ratio

from app.models import VerificationResponse, FieldCheck

logger = logging.getLogger(__name__)

# Government warning text patterns
GOVT_WARNING_KEYWORDS = [
    "government warning",
    "surgeon general",
    "pregnant",
    "birth defects",
    "operating machinery"
]


def extract_volume(text: str) -> Optional[str]:
    """
    Extract volume/net contents from text
    
    Args:
        text: Text containing volume information
        
    Returns:
        Extracted volume string or None
    """
    # Look for patterns like "750 mL", "750mL", "12 oz", "1 liter", etc.
    patterns = [
        r'(\d+(?:\.\d+)?)\s*(?:ml|mL|ML|milliliters?)',
        r'(\d+(?:\.\d+)?)\s*(?:l|L|liters?)',
        r'(\d+(?:\.\d+)?)\s*(?:oz|ounces?)',
        r'(\d+(?:\.\d+)?)\s*(?:fl\.?\s*oz)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            return matches[0]  # Return first match
    
    return None


def normalize_text(text: str) -> str:
    """Normalize text for comparison (lowercase, remove extra spaces)"""
    return re.sub(r'\s+', ' ', text.lower().strip())


def fuzzy_match(text: str, pattern: str, threshold: float = 0.8) -> bool:
    """
    Check if pattern exists in text using fuzzy matching
    
    Args:
        text: Text to search in
        pattern: Pattern to search for
        threshold: Similarity threshold (0.0 to 1.0)
        
    Returns:
        True if pattern found with similarity >= threshold
    """
    text_norm = normalize_text(text)
    pattern_norm = normalize_text(pattern)
    
    # Exact substring match
    if pattern_norm in text_norm:
        return True
    
    # Fuzzy match using Levenshtein distance
    # Check if pattern appears as a substring with fuzzy matching
    words = text_norm.split()
    pattern_words = pattern_norm.split()
    
    # Try to find consecutive words that match the pattern
    for i in range(len(words) - len(pattern_words) + 1):
        window = ' '.join(words[i:i + len(pattern_words)])
        similarity = ratio(window, pattern_norm)
        if similarity >= threshold:
            return True
    
    return False


def extract_percentage(text: str) -> Optional[float]:
    """
    Extract alcohol percentage from text
    
    Args:
        text: Text containing percentage
        
    Returns:
        Extracted percentage value or None
    """
    # Look for patterns like "45%", "45 %", "45% ABV", "45.5%", etc.
    patterns = [
        r'(\d+\.?\d*)\s*%',
        r'(\d+\.?\d*)\s*percent',
        r'alc\.?\s*(\d+\.?\d*)',
        r'alcohol\s*(\d+\.?\d*)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            try:
                return float(matches[0])
            except ValueError:
                continue
    
    return None


def verify_label_data(
    extracted_text: str,
    brand_name: str,
    product_class: str,
    alcohol_content: float,
    net_contents: Optional[str] = None
) -> VerificationResponse:
    """
    Verify label data against form inputs
    
    Args:
        extracted_text: OCR extracted text from label
        brand_name: Expected brand name
        product_class: Expected product class/type
        alcohol_content: Expected alcohol content (ABV %)
        net_contents: Expected net contents/volume (optional)
        
    Returns:
        VerificationResponse with detailed verification results
    """
    checks = []
    all_matched = True
    
    # Check 1: Brand Name
    brand_matched = fuzzy_match(extracted_text, brand_name, threshold=0.75)
    checks.append(FieldCheck(
        field_name="Brand Name",
        expected_value=brand_name,
        found_value=brand_name if brand_matched else "Not found or mismatch",
        matched=brand_matched,
        message=f"✓ Brand name '{brand_name}' found on label" if brand_matched 
                else f"✗ Brand name '{brand_name}' not found on label"
    ))
    all_matched = all_matched and brand_matched
    
    # Check 2: Product Class/Type
    product_matched = fuzzy_match(extracted_text, product_class, threshold=0.75)
    checks.append(FieldCheck(
        field_name="Product Class/Type",
        expected_value=product_class,
        found_value=product_class if product_matched else "Not found or mismatch",
        matched=product_matched,
        message=f"✓ Product class '{product_class}' found on label" if product_matched
                else f"✗ Product class '{product_class}' not found on label"
    ))
    all_matched = all_matched and product_matched
    
    # Check 3: Alcohol Content
    extracted_abv = extract_percentage(extracted_text)
    abv_matched = False
    abv_message = ""
    
    if extracted_abv is not None:
        # Allow small tolerance for OCR errors (±0.5%)
        if abs(extracted_abv - alcohol_content) <= 0.5:
            abv_matched = True
            abv_message = f"✓ Alcohol content {extracted_abv}% matches form ({alcohol_content}%)"
        else:
            abv_message = f"✗ Alcohol content on label ({extracted_abv}%) differs from form ({alcohol_content}%)"
    else:
        abv_message = f"✗ Could not find alcohol content on label (expected {alcohol_content}%)"
    
    checks.append(FieldCheck(
        field_name="Alcohol Content",
        expected_value=f"{alcohol_content}%",
        found_value=f"{extracted_abv}%" if extracted_abv else "Not found",
        matched=abv_matched,
        message=abv_message
    ))
    all_matched = all_matched and abv_matched
    
    # Check 4: Net Contents (optional)
    if net_contents:
        # Extract the volume number from the form input
        form_volume_match = re.search(r'(\d+(?:\.\d+)?)', net_contents)
        if not form_volume_match:
            # If we can't parse the form input, skip this check
            logger.warning(f"Could not parse net contents from form: {net_contents}")
        else:
            form_volume = form_volume_match.group(1)
            
            # Extract volume from OCR text
            extracted_volume = extract_volume(extracted_text)
            
            if extracted_volume and form_volume == extracted_volume:
                net_matched = True
                net_message = f"✓ Net contents '{net_contents}' found on label"
            elif extracted_volume:
                net_matched = False
                net_message = f"✗ Net contents on label ({extracted_volume} mL) differs from form ({net_contents})"
            else:
                net_matched = False
                net_message = f"✗ Net contents '{net_contents}' not found on label"
            
            checks.append(FieldCheck(
                field_name="Net Contents",
                expected_value=net_contents,
                found_value=f"{extracted_volume} mL" if extracted_volume else "Not found",
                matched=net_matched,
                message=net_message
            ))
            all_matched = all_matched and net_matched
    
    # Check 5: Government Warning (bonus check)
    warning_found = any(fuzzy_match(extracted_text, keyword, threshold=0.85) 
                       for keyword in GOVT_WARNING_KEYWORDS)
    
    checks.append(FieldCheck(
        field_name="Government Warning",
        expected_value="Required warning text",
        found_value="Present" if warning_found else "Not found",
        matched=warning_found,
        message="✓ Government warning statement found on label" if warning_found
                else "⚠️ Government warning statement not detected (required by law)"
    ))
    # Warning is important but won't fail the overall match for now
    # In production, this would be mandatory
    
    # Generate overall message
    if all_matched:
        message = "✅ The label matches the form data. All required information is consistent."
    else:
        failed_checks = [check.field_name for check in checks if not check.matched and check.field_name != "Government Warning"]
        message = f"❌ The label does not match the form. Issues found in: {', '.join(failed_checks)}"
    
    return VerificationResponse(
        success=True,
        overall_match=all_matched,
        message=message,
        extracted_text=extracted_text,
        checks=checks
    )
