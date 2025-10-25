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

from app.models import VerificationResponse, FieldCheck, BeverageType

logger = logging.getLogger(__name__)

# Government warning text patterns (basic check)
GOVT_WARNING_KEYWORDS = [
    "government warning",
    "surgeon general",
    "pregnant",
    "birth defects",
    "operating machinery"
]

# Official TTB required warning text (27 CFR 16.21)
REQUIRED_WARNING_TEXT = """GOVERNMENT WARNING: (1) According to the Surgeon General, women should not drink alcoholic beverages during pregnancy because of the risk of birth defects. (2) Consumption of alcoholic beverages impairs your ability to drive a car or operate machinery, and may cause health problems."""


def extract_government_warning(text: str) -> Optional[str]:
    """
    Extract the government warning section from OCR text
    
    Args:
        text: Full OCR extracted text
        
    Returns:
        Extracted warning text or None
    """
    # Look for text starting with "GOVERNMENT WARNING"
    pattern = r'GOVERNMENT WARNING:.*?(?:health problems|$)'
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    
    if match:
        warning_text = match.group(0)
        # Clean up extra whitespace but preserve structure
        warning_text = re.sub(r'\s+', ' ', warning_text).strip()
        return warning_text
    
    return None


def validate_warning_compliance(extracted_text: str) -> tuple[bool, list[str]]:
    """
    Detailed compliance check for government warning per 27 CFR 16.21
    
    Checks:
    - "GOVERNMENT WARNING" in all caps
    - "Surgeon General" with proper capitalization
    - Both statements (1) and (2) present
    - Overall text similarity to required warning
    
    Args:
        extracted_text: Full OCR text from label
        
    Returns:
        Tuple of (is_compliant, list_of_violations)
    """
    violations = []
    
    # Extract warning section
    warning_text = extract_government_warning(extracted_text)
    
    if not warning_text:
        violations.append("Government warning statement not found")
        return False, violations
    
    # Check 1: "GOVERNMENT WARNING" must be in all caps
    if "GOVERNMENT WARNING:" not in warning_text:
        if "government warning:" in warning_text.lower():
            violations.append("'GOVERNMENT WARNING' must be in all capital letters")
    
    # Check 2: "Surgeon General" capitalization (not "surgeon general" or "Surgeon general")
    if "surgeon general" in warning_text.lower():
        # Check if it's properly capitalized
        if "Surgeon General" not in warning_text:
            violations.append("'Surgeon General' must have capital S and capital G")
    
    # Check 3: Both statements (1) and (2) must be present
    has_statement_1 = "(1)" in warning_text or "1)" in warning_text
    has_statement_2 = "(2)" in warning_text or "2)" in warning_text
    
    if not has_statement_1:
        violations.append("Statement (1) about pregnancy and birth defects is missing")
    if not has_statement_2:
        violations.append("Statement (2) about driving/machinery is missing")
    
    # Check 4: Key phrases must be present
    required_phrases = [
        ("women should not drink", "women and pregnancy warning"),
        ("birth defects", "birth defects warning"),
        ("drive a car or operate machinery", "driving/machinery warning"),
        ("health problems", "health problems warning")
    ]
    
    warning_lower = warning_text.lower()
    for phrase, description in required_phrases:
        if phrase not in warning_lower:
            violations.append(f"Missing required phrase: '{description}'")
    
    # Check 5: Overall similarity to required text (fuzzy match for OCR tolerance)
    # Normalize both texts for comparison
    normalized_required = normalize_text(REQUIRED_WARNING_TEXT)
    normalized_found = normalize_text(warning_text)
    
    similarity = ratio(normalized_required, normalized_found)
    
    # Require high similarity (0.90) since this is regulatory text
    if similarity < 0.90:
        violations.append(f"Warning text differs from required regulatory text (similarity: {similarity:.2%})")
    
    is_compliant = len(violations) == 0
    
    return is_compliant, violations


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


def check_sulfite_declaration(text: str) -> bool:
    """
    Check for sulfite declaration (required for wine)
    
    Args:
        text: OCR extracted text
        
    Returns:
        True if sulfite declaration found
    """
    sulfite_patterns = [
        "contains sulfites",
        "contains sulphites",
        "sulfite",
        "sulphite"
    ]
    
    text_lower = text.lower()
    return any(pattern in text_lower for pattern in sulfite_patterns)


def check_vintage_year(text: str) -> Optional[int]:
    """
    Extract vintage year from wine label
    
    Args:
        text: OCR extracted text
        
    Returns:
        Vintage year or None
    """
    # Look for 4-digit years between 1900-2099
    pattern = r'\b(19\d{2}|20\d{2})\b'
    matches = re.findall(pattern, text)
    
    if matches:
        # Return first year found
        return int(matches[0])
    
    return None


def check_ingredients_list(text: str) -> bool:
    """
    Check for ingredients list (common on beer labels)
    
    Args:
        text: OCR extracted text
        
    Returns:
        True if ingredients list appears to be present
    """
    ingredient_keywords = [
        "ingredients",
        "contains",
        "water",
        "barley",
        "hops",
        "yeast",
        "malt"
    ]
    
    text_lower = text.lower()
    # Consider ingredients present if we find at least 2 keywords
    found_count = sum(1 for keyword in ingredient_keywords if keyword in text_lower)
    return found_count >= 2


def verify_label_data(
    extracted_text: str,
    brand_name: str,
    product_class: str,
    alcohol_content: float,
    net_contents: Optional[str] = None,
    beverage_type: BeverageType = BeverageType.SPIRITS
) -> VerificationResponse:
    """
    Verify label data against form inputs with beverage-type specific rules
    
    Args:
        extracted_text: OCR extracted text from label
        brand_name: Expected brand name
        product_class: Expected product class/type
        alcohol_content: Expected alcohol content (ABV %)
        net_contents: Expected net contents/volume (optional)
        beverage_type: Type of beverage (spirits, wine, beer)
        
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
    
    # Check 5: Government Warning - Detailed Compliance Check (27 CFR 16.21)
    warning_compliant, violations = validate_warning_compliance(extracted_text)
    
    if warning_compliant:
        warning_message = "✓ Government warning complies with 27 CFR 16.21 requirements"
        warning_found_value = "Compliant"
    else:
        # List all violations
        violation_details = "; ".join(violations)
        warning_message = f"✗ Warning non-compliant: {violation_details}"
        warning_found_value = f"Non-compliant ({len(violations)} violations)"
    
    checks.append(FieldCheck(
        field_name="Government Warning (Detailed)",
        expected_value="27 CFR 16.21 compliant warning",
        found_value=warning_found_value,
        matched=warning_compliant,
        message=warning_message,
        violations=violations if not warning_compliant else None
    ))
    # Government warning is mandatory - fail verification if non-compliant
    all_matched = all_matched and warning_compliant
    
    # Beverage-type specific checks
    if beverage_type == BeverageType.WINE:
        # Check for sulfite declaration (required for wine)
        sulfite_found = check_sulfite_declaration(extracted_text)
        checks.append(FieldCheck(
            field_name="Sulfite Declaration",
            expected_value="Contains Sulfites",
            found_value="Present" if sulfite_found else "Not found",
            matched=sulfite_found,
            message="✓ Sulfite declaration found on label" if sulfite_found
                    else "✗ Sulfite declaration not found (required for wine)"
        ))
        all_matched = all_matched and sulfite_found
        
        # Check for vintage year (optional but common)
        vintage_year = check_vintage_year(extracted_text)
        checks.append(FieldCheck(
            field_name="Vintage Year",
            expected_value="Vintage year (if applicable)",
            found_value=str(vintage_year) if vintage_year else "Not found",
            matched=vintage_year is not None,
            message=f"✓ Vintage year {vintage_year} found on label" if vintage_year
                    else "ℹ️ No vintage year found (optional for some wines)"
        ))
        # Don't fail overall match if vintage year missing (optional)
        
    elif beverage_type == BeverageType.BEER:
        # Check for ingredients list (often present on craft beer)
        ingredients_found = check_ingredients_list(extracted_text)
        checks.append(FieldCheck(
            field_name="Ingredients",
            expected_value="Ingredients list",
            found_value="Present" if ingredients_found else "Not found",
            matched=ingredients_found,
            message="✓ Ingredients list found on label" if ingredients_found
                    else "ℹ️ Ingredients list not detected (optional but common)"
        ))
        # Don't fail overall match if ingredients missing (not always required)
    
    # Generate overall message
    if all_matched:
        message = f"✅ The {beverage_type.value} label matches the form data. All required information is consistent."
    else:
        failed_checks = [check.field_name for check in checks if not check.matched and check.field_name != "Government Warning"]
        message = f"❌ The {beverage_type.value} label does not match the form. Issues found in: {', '.join(failed_checks)}"
    
    return VerificationResponse(
        success=True,
        overall_match=all_matched,
        message=message,
        extracted_text=extracted_text,
        checks=checks
    )
