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


def fuzzy_match(text: str, pattern: str, threshold: float = 0.8) -> tuple[bool, Optional[str]]:
    """
    Check if pattern exists in text using fuzzy matching
    
    Args:
        text: Text to search in
        pattern: Pattern to search for
        threshold: Similarity threshold (0.0 to 1.0)
        
    Returns:
        Tuple of (matched: bool, found_text: Optional[str])
        If matched, found_text contains the actual text that matched
    """
    text_norm = normalize_text(text)
    pattern_norm = normalize_text(pattern)
    
    # Exact substring match
    if pattern_norm in text_norm:
        # Find the actual text that matched
        idx = text_norm.index(pattern_norm)
        # Return the original case version
        return True, text[idx:idx + len(pattern)]
    
    # Fuzzy match using Levenshtein distance
    # Check if pattern appears as a substring with fuzzy matching
    words = text_norm.split()
    pattern_words = pattern_norm.split()
    
    # Try to find consecutive words that match the pattern
    best_match = None
    best_similarity = 0.0
    
    for i in range(len(words) - len(pattern_words) + 1):
        window = ' '.join(words[i:i + len(pattern_words)])
        similarity = ratio(window, pattern_norm)
        if similarity >= threshold and similarity > best_similarity:
            best_similarity = similarity
            # Find the original text for this window
            original_words = text.split()
            best_match = ' '.join(original_words[i:i + len(pattern_words)])
    
    if best_match:
        return True, best_match
    
    return False, None


def extract_brand_name(text: str) -> Optional[str]:
    """
    Extract the brand name from label text (typically first line or large text)
    
    Args:
        text: OCR extracted text
        
    Returns:
        Likely brand name or None
    """
    lines = text.strip().split('\n')
    if lines:
        # First non-empty line is usually the brand
        for line in lines:
            line = line.strip()
            if line and len(line) > 1:  # Skip single characters
                return line
    return None


def extract_product_type(text: str) -> Optional[str]:
    """
    Extract product type from label text
    
    Args:
        text: OCR extracted text
        
    Returns:
        Likely product type or None
    """
    # Common alcohol product types
    product_types = [
        'bourbon whiskey', 'bourbon', 'whiskey', 'whisky',
        'vodka', 'rum', 'gin', 'tequila', 'brandy',
        'scotch', 'rye', 'cognac', 'beer', 'wine',
        'kentucky straight bourbon whiskey'
    ]
    
    text_lower = text.lower()
    
    # Find the longest matching product type
    found_types = []
    for ptype in product_types:
        if ptype in text_lower:
            found_types.append(ptype)
    
    if found_types:
        # Return longest match (more specific)
        return max(found_types, key=len).title()
    
    return None


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
    brand_matched, found_brand = fuzzy_match(extracted_text, brand_name, threshold=0.75)
    
    # If no match found, try to extract what brand IS on the label
    if not found_brand:
        found_brand = extract_brand_name(extracted_text)
    
    checks.append(FieldCheck(
        field_name="Brand Name",
        expected_value=brand_name,
        found_value=found_brand if found_brand else "Not found",
        matched=brand_matched,
        message=f"✓ Brand name '{brand_name}' found on label" if brand_matched 
                else f"✗ Brand name '{brand_name}' not found on label"
    ))
    all_matched = all_matched and brand_matched
    
    # Check 2: Product Class/Type
    product_matched, found_product = fuzzy_match(extracted_text, product_class, threshold=0.75)
    
    # If no match found, try to extract what product type IS on the label
    if not found_product:
        found_product = extract_product_type(extracted_text)
    
    checks.append(FieldCheck(
        field_name="Product Class/Type",
        expected_value=product_class,
        found_value=found_product if found_product else "Not found",
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
    warning_found, found_warning = any(
        (match := fuzzy_match(extracted_text, keyword, threshold=0.85))[0]
        for keyword in GOVT_WARNING_KEYWORDS
    ) or (False, None), None
    
    # Simpler approach - just check if any keyword matches
    warning_matched = False
    for keyword in GOVT_WARNING_KEYWORDS:
        matched, _ = fuzzy_match(extracted_text, keyword, threshold=0.85)
        if matched:
            warning_matched = True
            break
    
    checks.append(FieldCheck(
        field_name="Government Warning",
        expected_value="Required warning text",
        found_value="Present" if warning_matched else "Not found",
        matched=warning_matched,
        message="✓ Government warning statement found on label" if warning_matched
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
