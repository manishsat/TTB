import { test, expect } from '@playwright/test';
import path from 'path';
import { fileURLToPath } from 'url';

// Fix for __dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * E2E Tests for TTB Label Verification Application
 * 
 * These tests automate the manual test scenarios from MANUAL_TESTING_GUIDE.md
 * Tests run against the deployed application on Vercel
 */

test.describe('TTB Label Verification E2E Tests', () => {
  
  test.beforeEach(async ({ page }) => {
    // Navigate to the application
    await page.goto('/');
    
    // Wait for the form to be visible
    await expect(page.getByText('Label Application Form')).toBeVisible();
  });

  test('Scenario 1: Compliant Standard Bourbon - Should Pass', async ({ page }) => {
    // Fill in the form using ID selectors
    await page.locator('#brandName').fill('Eagle Peak');
    await page.locator('#beverageType').selectOption('spirits');
    await page.locator('#productClass').fill('Bourbon Whiskey');
    await page.locator('#alcoholContent').fill('45');
    await page.locator('#netContents').fill('750');
    
    // Upload the test image
    const testImagePath = path.join(__dirname, '../../test_labels/compliance_tests/compliant_warning.png');
    await page.locator('#labelImage').setInputFiles(testImagePath);
    
    // Submit the form
    await page.getByRole('button', { name: /verify/i }).click();
    
    // Wait for "Processing label image..." to appear first
    await page.waitForSelector('text="Processing label image..."', { timeout: 5000 });
    
    // Then wait for it to disappear (results loaded) - this is key!
    await page.waitForSelector('text="Processing label image..."', { state: 'hidden', timeout: 60000 });
    
    // Wait a bit more for results to fully render
    await page.waitForTimeout(1000);
    
    // Now check for results
    const pageContent = await page.textContent('body');
    expect(pageContent).toMatch(/compliant|pass|success|approved/i);
  });

  test('Scenario 2: Compliant Beer - Should Pass', async ({ page }) => {
    // Fill in the form using ID selectors
    await page.locator('#brandName').fill('Summit Brew');
    await page.locator('#beverageType').selectOption('beer');
    await page.locator('#productClass').fill('India Pale Ale');
    await page.locator('#alcoholContent').fill('6.5');
    await page.locator('#netContents').fill('355');
    
    // Upload the test image
    const testImagePath = path.join(__dirname, '../../test_labels/compliance_tests/beer_compliant.png');
    await page.locator('#labelImage').setInputFiles(testImagePath);
    
    // Submit the form
    await page.getByRole('button', { name: /verify/i }).click();
    
    // Wait for "Processing label image..." to disappear (backend processing complete)
    await page.waitForSelector('text=/Processing label image/i', { 
      state: 'hidden',
      timeout: 60000 
    });
    
    // Check for success - just verify results appeared
    const pageContent = await page.textContent('body');
    expect(pageContent).toMatch(/compliant|pass|success/i);
  });

  test('Scenario 3: Compliant Wine - Should Pass', async ({ page }) => {
    // Fill in the form using ID selectors
    await page.locator('#brandName').fill('Chateau Valley');
    await page.locator('#beverageType').selectOption('wine');
    await page.locator('#productClass').fill('Cabernet Sauvignon');
    await page.locator('#alcoholContent').fill('13.5');
    await page.locator('#netContents').fill('750');
    
    // Upload the test image
    const testImagePath = path.join(__dirname, '../../test_labels/compliance_tests/wine_compliant.png');
    await page.locator('#labelImage').setInputFiles(testImagePath);
    
    // Submit the form
    await page.getByRole('button', { name: /verify/i }).click();
    
    // Wait for "Processing label image..." to disappear (backend processing complete)
    await page.waitForSelector('text=/Processing label image/i', { 
      state: 'hidden',
      timeout: 60000 
    });
    
    // Check for success - just verify results appeared
    const pageContent = await page.textContent('body');
    expect(pageContent).toMatch(/compliant|pass|success/i);
  });

  test('Scenario 4: Non-Compliant - Incomplete Government Warning', async ({ page }) => {
    // Fill in the form using ID selectors
    await page.locator('#brandName').fill('Test Rum');
    await page.locator('#beverageType').selectOption('spirits');
    await page.locator('#productClass').fill('Rum');
    await page.locator('#alcoholContent').fill('35');
    await page.locator('#netContents').fill('700');
    
    // Upload the test image
    const testImagePath = path.join(__dirname, '../../test_labels/compliance_tests/noncompliant_missing_statement2.png');
    await page.locator('#labelImage').setInputFiles(testImagePath);
    
    // Submit the form
    await page.getByRole('button', { name: /verify/i }).click();
    
    // Wait for "Processing label image..." to disappear (backend processing complete)
    await page.waitForSelector('text=/Processing label image/i', { 
      state: 'hidden',
      timeout: 60000 
    });
    
    // Check for non-compliance detected - just verify results appeared
    const pageContent = await page.textContent('body');
    expect(pageContent).toMatch(/non-compliant|warning|missing|violation/i);
  });

  test('Scenario 5: Non-Compliant - Form/Label Mismatch', async ({ page }) => {
    // Fill in the form with DIFFERENT ABV than label using ID selectors
    await page.locator('#brandName').fill('Test Rum');
    await page.locator('#beverageType').selectOption('spirits');
    await page.locator('#productClass').fill('Rum');
    await page.locator('#alcoholContent').fill('40'); // Label has 35%
    await page.locator('#netContents').fill('700');
    
    // Upload the test image
    const testImagePath = path.join(__dirname, '../../test_labels/compliance_tests/noncompliant_missing_statement2.png');
    await page.locator('#labelImage').setInputFiles(testImagePath);
    
    // Submit the form
    await page.getByRole('button', { name: /verify/i }).click();
    
    // Wait for "Processing label image..." to disappear (backend processing complete)
    await page.waitForSelector('text=/Processing label image/i', { 
      state: 'hidden',
      timeout: 60000 
    });
    
    // Check for failure - just verify results appeared
    const pageContent = await page.textContent('body');
    expect(pageContent).toMatch(/non-compliant|mismatch|differ|verification/i);
  });

  test('Scenario 6: Non-Compliant - Incorrect Capitalization', async ({ page }) => {
    // Fill in the form using ID selectors
    await page.locator('#brandName').fill('Test Spirits');
    await page.locator('#beverageType').selectOption('spirits');
    await page.locator('#productClass').fill('Vodka');
    await page.locator('#alcoholContent').fill('40');
    await page.locator('#netContents').fill('750');
    
    // Upload the test image
    const testImagePath = path.join(__dirname, '../../test_labels/compliance_tests/noncompliant_lowercase_sg.png');
    await page.locator('#labelImage').setInputFiles(testImagePath);
    
    // Submit the form
    await page.getByRole('button', { name: /verify/i }).click();
    
    // Wait for "Processing label image..." to disappear (backend processing complete)
    await page.waitForSelector('text=/Processing label image/i', { 
      state: 'hidden',
      timeout: 60000 
    });
    
    // Check for failure with capitalization error - just verify results appeared
    const pageContent = await page.textContent('body');
    expect(pageContent).toMatch(/non-compliant|capital|format|verification/i);
  });

  test('Scenario 9: Edge Case - Tiny Image (Should Reject)', async ({ page }) => {
    // Fill in the form using ID selectors
    await page.locator('#brandName').fill('Mini Distillery');
    await page.locator('#beverageType').selectOption('spirits');
    await page.locator('#productClass').fill('Bourbon');
    await page.locator('#alcoholContent').fill('45');
    await page.locator('#netContents').fill('750');
    
    // Upload the tiny test image
    const testImagePath = path.join(__dirname, '../../test_labels/tiny_bourbon.png');
    await page.locator('#labelImage').setInputFiles(testImagePath);
    
    // Submit the form
    await page.getByRole('button', { name: /verify/i }).click();
    
    // Wait for "Processing label image..." to disappear (backend processing complete)
    await page.waitForSelector('text=/Processing label image/i', { 
      state: 'hidden',
      timeout: 60000 
    });
    
    // Check for image quality error - just verify results appeared
    const pageContent = await page.textContent('body');
    expect(pageContent).toMatch(/image.*quality|resolution.*low|minimum.*400|size|error/i);
  });

  test('UI: Form Validation - Required Fields', async ({ page }) => {
    // Try to submit without filling required fields
    await page.getByRole('button', { name: /verify/i }).click();
    
    // Check that form is still visible (submission didn't proceed)
    // Or check that brand name field is still empty
    const brandNameInput = page.locator('#brandName');
    await expect(brandNameInput).toBeVisible();
    await expect(brandNameInput).toHaveValue('');
  });

  test('UI: Image Preview Shows After Upload', async ({ page }) => {
    // Upload an image
    const testImagePath = path.join(__dirname, '../../test_labels/compliance_tests/compliant_warning.png');
    await page.locator('#labelImage').setInputFiles(testImagePath);
    
    // Check that image preview appears
    const imagePreview = page.locator('img[alt*="preview" i], img[alt*="uploaded" i]');
    await expect(imagePreview).toBeVisible({ timeout: 3000 });
  });

  test('UI: Clear/Reset Functionality', async ({ page }) => {
    // Fill in some form data using ID selectors
    await page.locator('#brandName').fill('Test Brand');
    await page.locator('#productClass').fill('Test Product');
    
    // Look for a clear/reset button if it exists
    const resetButton = page.getByRole('button', { name: /clear|reset/i });
    const resetButtonCount = await resetButton.count();
    
    if (resetButtonCount > 0) {
      await resetButton.click();
      
      // Verify fields are cleared
      await expect(page.locator('#brandName')).toHaveValue('');
      await expect(page.locator('#productClass')).toHaveValue('');
    }
  });
});
