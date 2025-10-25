#!/usr/bin/env python3
"""Check which old test labels have government warnings and if they're compliant."""

import pytesseract
from PIL import Image
import os
import re

old_labels = [
    'test_labels/clear_bourbon.png',
    'test_labels/low_contrast_vodka.png',
    'test_labels/slightly_blurry_beer.png',
    'test_labels/test_ocr.png',
    'test_labels/tiny_bourbon.png',
    'test_labels/failures/missing_warning.png',
    'test_labels/failures/multiple_errors.png',
    'test_labels/failures/wrong_alcohol_content.png',
    'test_labels/failures/wrong_brand.png',
    'test_labels/failures/wrong_product_type.png',
    'test_labels/failures/wrong_volume.png',
    'test_labels/ocr_tolerance_tests/error_tolerance_test.png',
    'test_labels/product_types/beer_label.png',
    'test_labels/product_types/wine_label.png',
]

print('=' * 80)
print('CHECKING OLD TEST LABELS FOR GOVERNMENT WARNING COMPLIANCE')
print('=' * 80)

labels_with_warnings = []

for label in old_labels:
    if os.path.exists(label):
        img = Image.open(label)
        text = pytesseract.image_to_string(img)
        
        # Check if has government warning
        has_warning = 'GOVERNMENT WARNING' in text.upper()
        
        if has_warning:
            # Extract warning text
            pattern = r'GOVERNMENT WARNING:.*?(?:health problems|$)'
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            
            warning_text = match.group(0) if match else "Could not extract"
            
            # Check for compliance issues
            issues = []
            if 'surgeon general' in text.lower() and 'Surgeon General' not in text:
                issues.append('lowercase "surgeon general"')
            if '(1)' not in text:
                issues.append('missing statement (1)')
            if '(2)' not in text:
                issues.append('missing statement (2)')
            
            labels_with_warnings.append({
                'path': label,
                'issues': issues,
                'warning_snippet': warning_text[:100] + '...' if len(warning_text) > 100 else warning_text
            })
            
            status = '❌ NON-COMPLIANT' if issues else '✅ COMPLIANT'
            print(f'\n{status}: {label}')
            if issues:
                for issue in issues:
                    print(f'  - {issue}')
        else:
            print(f'\n⚪ NO WARNING: {label}')

print('\n' + '=' * 80)
print(f'SUMMARY: {len(labels_with_warnings)} labels with warnings found')
print('=' * 80)

if labels_with_warnings:
    non_compliant = [l for l in labels_with_warnings if l['issues']]
    print(f'\n❌ NON-COMPLIANT: {len(non_compliant)} labels')
    for label in non_compliant:
        print(f'   - {label["path"]}')
    
    compliant = [l for l in labels_with_warnings if not l['issues']]
    print(f'\n✅ COMPLIANT: {len(compliant)} labels')
    for label in compliant:
        print(f'   - {label["path"]}')
