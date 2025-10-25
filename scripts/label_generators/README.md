# Label Generator Scripts

This directory contains utility scripts for generating test label images for the TTB Label Verification system.

## Scripts

- `create_realistic_labels.py` - Generate realistic-looking test labels
- `create_failure_test_images.py` - Generate labels with intentional errors for testing
- `create_compliance_test_labels.py` - Generate labels for government warning compliance testing
- `create_beverage_type_compliance_labels.py` - Generate compliant labels for different beverage types (beer, wine)
- `create_product_type_test_labels.py` - Generate labels for testing different product types
- `create_ocr_error_test.py` - Generate labels to test OCR error tolerance
- `regenerate_old_labels.py` - Regenerate old labels with updated compliant warnings
- `check_old_warnings.py` - Verify government warning compliance in existing labels
- `test_compliance.py` - Test compliance validation functions

## Usage

All scripts should be run from the project root directory:

```bash
cd /path/to/TTB
python3 scripts/label_generators/create_realistic_labels.py
```

## Requirements

These scripts require:
- Python 3.8+
- Pillow (PIL)
- pytesseract (for verification scripts)
