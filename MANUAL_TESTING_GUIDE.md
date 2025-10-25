# TTB Label Verification - Testing Guide

This guide provides step-by-step instructions for testing various scenarios of the TTB Label Verification application.

## Prerequisites

- Access to the deployed application:
  - **Frontend URL:** https://ttb-lime.vercel.app
  - **Backend API URL:** https://ttb-production.up.railway.app
- Test label images located in `test_labels/` directory

## Test Scenarios

### Test Scenario 1: ✅ COMPLIANT - Standard Bourbon

**Purpose:** Verify that a compliant bourbon label passes all validation checks.

**Test Data:**
- **Brand Name:** `Eagle Peak`
- **Beverage Type:** `Distilled Spirits`
- **Product Class/Type:** `Bourbon Whiskey`
- **Alcohol Content (% ABV):** `45`
- **Net Contents (Optional):** `750`
- **Label Image:** `test_labels/compliance_tests/compliant_warning.png`

**Expected Result:** ✅ **COMPLIANT**
- All validation checks should pass
- Government warning detected and validated
- ABV meets minimum requirement (≥40%)
- Product type matches label content

---

### Test Scenario 2: ✅ COMPLIANT - Beer

**Purpose:** Verify that beer products with lower ABV are correctly validated.

**Test Data:**
- **Brand Name:** `Summit Brew`
- **Beverage Type:** `Beer`
- **Product Class/Type:** `India Pale Ale`
- **Alcohol Content (% ABV):** `6.5`
- **Net Contents (Optional):** `355`
- **Label Image:** `test_labels/compliance_tests/beer_compliant.png`

**Expected Result:** ✅ **COMPLIANT**
- Beer products have different ABV requirements than spirits
- Government warning should be present and validated
- Lower ABV (5-7%) is normal for beer

---

### Test Scenario 3: ✅ COMPLIANT - Wine

**Purpose:** Verify wine label compliance with sulfite declaration requirement.

**Test Data:**
- **Brand Name:** `Chateau Valley`
- **Beverage Type:** `Wine`
- **Product Class/Type:** `Cabernet Sauvignon`
- **Alcohol Content (% ABV):** `13.5`
- **Net Contents (Optional):** `750`
- **Label Image:** `test_labels/compliance_tests/wine_compliant.png`

**Expected Result:** ✅ **COMPLIANT**
- Wine labels require sulfite declaration (✓ "CONTAINS SULFITES" present)
- Government warning present
- ABV typical for wine (12-15%)
- Vintage year 2019 detected

---

### Test Scenario 4: ❌ NON-COMPLIANT - Incomplete Government Warning

**Purpose:** Verify that labels with incomplete government warnings are flagged.

**Test Data:**
- **Brand Name:** `Test Rum`
- **Beverage Type:** `Distilled Spirits`
- **Product Class/Type:** `Rum`
- **Alcohol Content (% ABV):** `35`
- **Net Contents (Optional):** `700`
- **Label Image:** `test_labels/compliance_tests/noncompliant_missing_statement2.png`

**Expected Result:** ❌ **NON-COMPLIANT**
- **Reason:** Government warning is incomplete (missing statement 2 about driving/machinery)
- Error message should indicate:
  - Statement (2) about driving/machinery is missing
  - Missing required phrases about health problems
  - Warning text differs from required regulatory text

---

### Test Scenario 5: ❌ NON-COMPLIANT - Form/Label Mismatch

**Purpose:** Verify that mismatches between form data and label content are detected.

**Test Data:**
- **Brand Name:** `Test Rum`
- **Beverage Type:** `Distilled Spirits`
- **Product Class/Type:** `Rum`
- **Alcohol Content (% ABV):** `40`  ← **Different from label (35%)**
- **Net Contents (Optional):** `700`
- **Label Image:** `test_labels/compliance_tests/noncompliant_missing_statement2.png`

**Expected Result:** ❌ **NON-COMPLIANT**
- **Reason:** Alcohol content on form (40%) doesn't match label (35%)
- Also has incomplete government warning
- This tests that the system catches when someone enters incorrect ABV on the form

---

### Test Scenario 6: ❌ NON-COMPLIANT - Incorrect Capitalization

**Purpose:** Verify that government warnings with incorrect formatting are caught.

**Test Data:**
- **Brand Name:** `Test Spirits`
- **Beverage Type:** `Distilled Spirits`
- **Product Class/Type:** `Vodka`
- **Alcohol Content (% ABV):** `40`
- **Net Contents (Optional):** `750`
- **Label Image:** `test_labels/compliance_tests/noncompliant_lowercase_sg.png`

**Expected Result:** ❌ **NON-COMPLIANT**
- **Reason:** "Surgeon General" not properly capitalized (should be capital S and capital G)
- TTB requires specific formatting for government warnings
- Error message: "'Surgeon General' must have capital S and capital G"

---

### Test Scenario 7: 🔄 EDGE CASE - Low Image Quality (Blurry)

**Purpose:** Test OCR performance with poor quality images.

**Test Data:**
- **Brand Name:** `Mountain View`
- **Beverage Type:** `Beer`
- **Product Class/Type:** `Beer`
- **Alcohol Content (% ABV):** `4.5`
- **Net Contents (Optional):** `355`
- **Label Image:** `test_labels/slightly_blurry_beer.png`

**Expected Result:** ❌ **NON-COMPLIANT** (likely)
- **Reason:** OCR fails to extract most text from blurry image
- Typical failures:
  - Product type not found
  - Alcohol content not found
  - Net contents not found
  - Government warning not found
- Only brand name may be detected (larger text)
- This tests the system's handling of poor image quality

---

### Test Scenario 8: 🔄 EDGE CASE - Low Contrast

**Purpose:** Test OCR performance with low contrast images.

**Test Data:**
- **Brand Name:** `Smooth Spirit`
- **Beverage Type:** `Distilled Spirits`
- **Product Class/Type:** `Vodka`
- **Alcohol Content (% ABV):** `40`
- **Net Contents (Optional):** `750`
- **Label Image:** `test_labels/low_contrast_vodka.png`

**Expected Result:** ❌ **NON-COMPLIANT** (partial failure)
- **Reason:** Low contrast makes some text difficult to extract
- Typical results:
  - ✓ Product type detected (Vodka)
  - ✓ Alcohol content detected (40%)
  - ✓ Net contents detected (750)
  - ❌ Government warning incomplete (missing phrases)
- Shows that OCR can handle low contrast for large/bold text but struggles with detailed warning text

---

### Test Scenario 9: 🔄 EDGE CASE - Tiny Image

**Purpose:** Test minimum image size requirements.

**Test Data:**
- **Brand Name:** `Mini Distillery`
- **Beverage Type:** `Distilled Spirits`
- **Product Class/Type:** `Bourbon`
- **Alcohol Content (% ABV):** `45`
- **Net Contents (Optional):** `750`
- **Label Image:** `test_labels/tiny_bourbon.png`

**Expected Result:** ⚠️ **IMAGE QUALITY CHECK FAILED**
- **Reason:** Image resolution too low (300x400 pixels)
- Error message: "Image resolution too low. Minimum 400x400 pixels required for accurate OCR."
- **System correctly rejects** the image before attempting OCR
- This validates that image quality pre-checks are working properly
- Prevents wasted OCR processing on images that will fail anyway

---

### Test Scenario 10: 🔄 EDGE CASE - Compressed Image

**Purpose:** Test handling of heavily compressed images.

**Test Data:**
- **Brand Name:** `Golden Hops`
- **Beverage Type:** `Beer`
- **Product Class/Type:** `India Pale Ale`
- **Alcohol Content (% ABV):** `6.5`
- **Net Contents (Optional):** `355`
- **Label Image:** `test_labels/compressed_ipa.jpg`

**Expected Result:** ❌ **NON-COMPLIANT** (partial failure)
- **Reason:** Compression artifacts affect detailed text extraction
- Typical results:
  - ✓ Product type detected (India Pale Ale)
  - ✓ Alcohol content detected (6.5%, within tolerance of 6.8% form input)
  - ✓ Net contents detected (355)
  - ❌ Government warning incomplete (both statements missing)
- Shows that compression particularly degrades small/detailed text quality
- Main label fields survive compression better than warning text

---

## Testing Checklist

Use this checklist to track your testing progress:

- [ ] **Test 1:** Compliant Bourbon - PASS expected
- [ ] **Test 2:** Compliant Beer - PASS expected
- [ ] **Test 3:** Compliant Wine - PASS expected
- [ ] **Test 4:** Incomplete Warning - FAIL expected
- [ ] **Test 5:** Low ABV Bourbon - FAIL expected
- [ ] **Test 6:** Incorrect Capitalization - FAIL expected
- [ ] **Test 7:** Blurry Image - FAIL expected
- [ ] **Test 8:** Low Contrast - Variable
- [ ] **Test 9:** Tiny Image - Variable
- [ ] **Test 10:** Compressed Image - Variable

## How to Test

1. **Open the Application:** Navigate to https://ttb-lime.vercel.app
2. **Fill in the Form:** Enter the test data exactly as specified above
3. **Upload Image:** Select the specified image from `test_labels/` directory
4. **Submit:** Click the "Verify Label" button
5. **Review Results:** Check if the actual result matches the expected result
6. **Document:** Note any discrepancies or unexpected behavior

## Understanding Results

### ✅ Compliant Result
- Green success message
- All validation checks passed
- Government warning detected and highlighted with green bounding box
- Brand name, product type, and other fields match

### ❌ Non-Compliant Result
- Red error message
- Lists specific compliance issues
- May include:
  - Missing or incomplete government warning
  - Product type mismatch
  - Invalid alcohol content
  - Missing required information
- Red bounding boxes highlight problem areas (if detected)

### 🟡 Warnings
- Yellow warning messages
- Non-critical issues detected
- Label may still be compliant but has minor concerns

## Additional Test Images

Your `test_labels/` directory contains additional organized test images:

```
test_labels/
├── compliance_tests/
│   ├── beer_compliant.png
│   ├── compliant_warning.png
│   ├── wine_compliant.png
│   ├── noncompliant_lowercase_sg.png
│   └── noncompliant_missing_statement2.png
├── failures/
├── ocr_tolerance_tests/
└── product_types/
```

Feel free to explore these directories for additional test cases.

## Backend API Testing (Optional)

For advanced testing, you can also test the backend API directly using curl:

```bash
# Test compliant bourbon
curl -X POST "https://ttb-production.up.railway.app/api/verify" \
  -F "file=@test_labels/compliance_tests/compliant_warning.png" \
  -F "brand_name=Eagle Peak" \
  -F "product_class=Bourbon Whiskey" \
  -F "alcohol_content=45" \
  -F "volume=750"

# Test low ABV bourbon (should fail)
curl -X POST "https://ttb-production.up.railway.app/api/verify" \
  -F "file=@test_labels/clear_bourbon.png" \
  -F "brand_name=Low Proof" \
  -F "product_class=Bourbon Whiskey" \
  -F "alcohol_content=35" \
  -F "volume=750"
```

## Health Check

Before testing, verify the backend is running:

```bash
curl https://ttb-production.up.railway.app/
```

Expected response:
```json
{
  "status": "ok",
  "message": "TTB Label Verification API is running",
  "version": "1.0.0"
}
```

## Troubleshooting

### Common Issues

1. **Image Upload Fails**
   - Check file size (max 10MB)
   - Verify file format (PNG, JPG, JPEG supported)
   - Ensure file path is correct

2. **OCR Not Working**
   - Backend Tesseract may need time to initialize
   - Check Railway logs for errors
   - Verify image quality is sufficient

3. **API Connection Error**
   - Check that Railway backend is running
   - Verify VITE_API_URL environment variable in Vercel
   - Check browser console for CORS errors

4. **Unexpected Results**
   - Review the validation logic in `backend/app/verification.py`
   - Check OCR extracted text in response
   - Verify form data was submitted correctly

## Success Criteria

A successful test run should demonstrate:

- ✅ At least 2 compliant labels pass validation
- ✅ At least 3 non-compliant labels fail with appropriate errors
- ✅ Government warning detection works on clear images
- ✅ ABV validation enforces minimum requirements
- ✅ Product type matching functions correctly
- ✅ Results display with proper visual feedback (colors, bounding boxes)

## Notes

- Test images are located in the `test_labels/` directory of the repository
- All test scenarios use real validation logic implemented in the application
- Edge cases (scenarios 7-10) may produce variable results depending on image quality
- The system uses Tesseract OCR which has varying accuracy based on image quality

---

**Happy Testing!** 🎉

If you encounter any issues or unexpected behavior, please document them with:
- Test scenario number
- Input data used
- Expected vs actual result
- Screenshots (if applicable)
- Any error messages displayed
