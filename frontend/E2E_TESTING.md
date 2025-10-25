# E2E (End-to-End) Testing

Automated browser tests for the TTB Label Verification application using Playwright.

## Overview

These tests automate the manual testing scenarios from `MANUAL_TESTING_GUIDE.md`. They run against the **deployed application** on Vercel (https://ttb-lime.vercel.app) and verify that the entire application workflow functions correctly.

## What's Tested

✅ **Test Scenario 1:** Compliant Standard Bourbon  
✅ **Test Scenario 2:** Compliant Beer  
✅ **Test Scenario 3:** Compliant Wine  
✅ **Test Scenario 4:** Non-Compliant - Incomplete Warning  
✅ **Test Scenario 5:** Non-Compliant - Form/Label Mismatch  
✅ **Test Scenario 6:** Non-Compliant - Incorrect Capitalization  
✅ **Test Scenario 9:** Edge Case - Tiny Image  
✅ **UI Tests:** Form validation, image preview, reset functionality  

## Prerequisites

- Node.js 18+ installed
- Frontend dependencies installed (`npm install`)
- Test label images in `../test_labels/` directory

## Running Tests

### Run all tests (headless)
```bash
cd frontend
npm run test:e2e
```

### Run tests with UI mode (recommended for development)
```bash
npm run test:e2e:ui
```

### Run tests in headed mode (see browser)
```bash
npm run test:e2e:headed
```

### View test report (after running tests)
```bash
npm run test:e2e:report
```

## Test Structure

```
frontend/
├── e2e/
│   └── label-verification.spec.ts    # All E2E test scenarios
├── playwright.config.ts               # Playwright configuration
└── package.json                       # Test scripts
```

## Configuration

The tests are configured to:
- Run against the deployed Vercel app: `https://ttb-lime.vercel.app`
- Use Chromium browser
- Take screenshots on failure
- Collect traces on retry
- Generate HTML reports

To test against localhost instead, update `baseURL` in `playwright.config.ts`:
```typescript
baseURL: 'http://localhost:5173',
```

## Test Scenarios

### 1. Compliant Labels (Should Pass)
- **Bourbon:** Eagle Peak, 45% ABV, 750mL
- **Beer:** Summit Brew, 6.5% ABV, 355mL
- **Wine:** Chateau Valley, 13.5% ABV, 750mL

### 2. Non-Compliant Labels (Should Fail)
- **Incomplete Warning:** Missing statement (2) about driving/machinery
- **Form Mismatch:** Form data doesn't match label content
- **Capitalization Error:** "Surgeon General" not properly capitalized

### 3. Edge Cases
- **Tiny Image:** Resolution too low (< 400x400), should reject before OCR

### 4. UI Tests
- Form validation for required fields
- Image preview after upload
- Clear/reset button functionality

## Debugging Failed Tests

### 1. View HTML Report
```bash
npm run test:e2e:report
```

### 2. Run in UI Mode
```bash
npm run test:e2e:ui
```
- Step through tests
- See live browser
- Inspect selectors
- Time travel through test execution

### 3. Run Single Test
```bash
npx playwright test -g "Scenario 1"
```

### 4. See Browser While Running
```bash
npm run test:e2e:headed
```

## Common Issues

### Test Timeout
If tests timeout, the backend might be slow or cold-starting:
- Increase timeout in `playwright.config.ts`
- Pre-warm the backend by visiting the app first

### Element Not Found
If selectors don't match:
- Check that the frontend UI hasn't changed
- Update selectors in `label-verification.spec.ts`
- Use Playwright Inspector: `npx playwright test --debug`

### Image Upload Fails
Ensure test images exist:
- Check `../test_labels/compliance_tests/` directory
- Verify file paths in test file

## CI/CD Integration

The tests are configured for CI environments:
- Retries: 2 (on CI only)
- Workers: 1 (serial execution on CI)
- Fail on `test.only` in CI

To run in CI, set the `CI` environment variable:
```bash
CI=true npm run test:e2e
```

## Adding New Tests

1. Add test scenario to `e2e/label-verification.spec.ts`
2. Follow existing test pattern:
   ```typescript
   test('Test Description', async ({ page }) => {
     // Fill form
     await page.getByLabel('Brand Name').fill('...');
     
     // Upload image
     await page.setInputFiles('input[type="file"]', testImagePath);
     
     // Submit
     await page.getByRole('button', { name: /verify label/i }).click();
     
     // Assert results
     await expect(page.getByText(/expected text/i)).toBeVisible();
   });
   ```
3. Run and verify: `npm run test:e2e:ui`

## Resources

- [Playwright Documentation](https://playwright.dev/)
- [Best Practices](https://playwright.dev/docs/best-practices)
- [Debugging Guide](https://playwright.dev/docs/debug)
- [Selectors Guide](https://playwright.dev/docs/selectors)

## Benefits Over Manual Testing

✅ **Speed:** Run all 10+ tests in seconds  
✅ **Consistency:** Same tests every time, no human error  
✅ **CI/CD Ready:** Integrate into deployment pipeline  
✅ **Regression Detection:** Catch breaks immediately  
✅ **Documentation:** Tests serve as executable documentation  
✅ **Coverage:** Test scenarios are always up to date  

---

**Note:** These E2E tests complement but don't replace the backend unit tests (`backend/tests/`). Both are important for comprehensive test coverage.
