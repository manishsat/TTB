"""
Test the detailed government warning compliance validation
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.verification import extract_government_warning, validate_warning_compliance
import pytesseract
from PIL import Image

def test_label(label_path, expected_result):
    """Test a label image for warning compliance"""
    print(f"\n{'='*80}")
    print(f"Testing: {os.path.basename(label_path)}")
    print(f"Expected: {expected_result}")
    print('='*80)
    
    # Extract text using OCR
    image = Image.open(label_path)
    extracted_text = pytesseract.image_to_string(image)
    
    print(f"\nExtracted text:\n{extracted_text[:500]}...")
    
    # Extract warning section
    warning_section = extract_government_warning(extracted_text)
    print(f"\nWarning section:\n{warning_section}")
    
    # Validate compliance
    is_compliant, violations = validate_warning_compliance(warning_section)
    
    print(f"\n{'✅ COMPLIANT' if is_compliant else '❌ NON-COMPLIANT'}")
    
    if violations:
        print(f"\nViolations found ({len(violations)}):")
        for i, violation in enumerate(violations, 1):
            print(f"  {i}. {violation}")
    else:
        print("\nNo violations - warning meets all requirements!")
    
    # Check if result matches expectation
    result_matches = (is_compliant and expected_result == "PASS") or (not is_compliant and expected_result == "FAIL")
    print(f"\n{'✅ Test PASSED' if result_matches else '❌ Test FAILED'} - Result matches expectation: {result_matches}")
    
    return result_matches


if __name__ == '__main__':
    print("="*80)
    print("DETAILED GOVERNMENT WARNING COMPLIANCE TESTING")
    print("="*80)
    
    test_cases = [
        ('test_labels/compliance_tests/compliant_warning.png', 'PASS'),
        ('test_labels/compliance_tests/noncompliant_lowercase_sg.png', 'FAIL'),
        ('test_labels/compliance_tests/noncompliant_missing_statement2.png', 'FAIL'),
    ]
    
    results = []
    for label_path, expected in test_cases:
        try:
            result = test_label(label_path, expected)
            results.append(result)
        except Exception as e:
            print(f"\n❌ Error testing {label_path}: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    passed = sum(results)
    total = len(results)
    print(f"Tests passed: {passed}/{total}")
    
    if all(results):
        print("\n✅ All compliance tests PASSED!")
    else:
        print("\n❌ Some tests failed")
        for i, (label_path, _) in enumerate(test_cases):
            status = "✅ PASS" if results[i] else "❌ FAIL"
            print(f"  {status} - {os.path.basename(label_path)}")
