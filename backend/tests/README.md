# Automated Tests

This directory contains unit tests for the TTB Label Verification application.

## Test Coverage

### `test_verification.py` - Core Verification Logic Tests

**37 test cases** covering:

#### 1. Fuzzy Matching (7 tests)
- Exact string matching
- Case-insensitive matching
- OCR error tolerance (l→i, O→0)
- Whitespace handling
- Threshold-based similarity
- No-match scenarios

#### 2. Text Normalization (3 tests)
- Lowercase conversion
- Whitespace collapsing
- Trim leading/trailing spaces

#### 3. Percentage Extraction (7 tests)
- Basic percentage (`45%`)
- Percentage with space (`45 %`)
- ABV notation (`45% ABV`)
- Alc./Vol. notation (`45% Alc./Vol.`)
- Decimal percentages (`45.5%`)
- Alternative notations (`alc. 45`)
- No percentage found scenarios

#### 4. Volume Extraction (7 tests)
- mL volumes (`750 mL`, `750mL`)
- Liter volumes (`1 L`)
- Ounce volumes (`12 oz`, `16 fl oz`)
- Decimal volumes (`750.5 mL`)
- No volume found scenarios

#### 5. Brand Name Extraction (3 tests)
- First line extraction
- Skip empty lines
- Handle empty text

#### 6. Product Type Extraction (4 tests)
- Extract bourbon whiskey
- Extract vodka
- Longest match preference
- No product type found

#### 7. Full Label Verification (6 integration tests)
- Perfect match scenario
- Brand mismatch detection
- Alcohol content tolerance (±0.5%)
- Alcohol content out of tolerance
- Net contents exact match
- Net contents substring prevention (750 vs 1750)

## Running Tests

### Prerequisites
```bash
cd backend
pip install -r requirements.txt
```

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Specific Test File
```bash
python -m pytest tests/test_verification.py -v
```

### Run Specific Test Class
```bash
python -m pytest tests/test_verification.py::TestFuzzyMatching -v
```

### Run Specific Test
```bash
python -m pytest tests/test_verification.py::TestFuzzyMatching::test_ocr_error_tolerance_l_to_i -v
```

### Run with Coverage Report
```bash
pip install pytest-cov
python -m pytest tests/ --cov=app --cov-report=html
```

## Test Results

```
======================== 37 passed in 0.08s ========================
```

All tests passing ✅

## What These Tests Validate

1. **OCR Error Tolerance**: Confirms fuzzy matching handles common OCR mistakes
   - Character substitutions (l→i, O→0)
   - Extra/missing whitespace
   - Case variations

2. **Data Extraction**: Validates all extraction functions correctly parse:
   - Alcohol percentages in various formats
   - Volume measurements in different units
   - Brand names from label structure
   - Product types from text

3. **Verification Logic**: Ensures the main verification function:
   - Correctly identifies matches and mismatches
   - Applies appropriate tolerances (±0.5% for ABV)
   - Prevents false positives (750 vs 1750)
   - Extracts actual values when mismatches occur

4. **Edge Cases**: Tests handle:
   - Empty or malformed input
   - Missing data
   - Decimal values
   - Multiple notations for same information

## Adding New Tests

When adding new features, add corresponding tests:

```python
def test_new_feature(self):
    """Test description"""
    result = function_to_test(input_data)
    assert result == expected_output
```

Follow existing patterns for organization and naming.
