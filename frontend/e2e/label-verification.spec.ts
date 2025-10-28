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
    
    // Wait for processing to complete
    await page.waitForSelector('text="Processing label image..."', { timeout: 5000 });
    await page.waitForSelector('text="Processing label image..."', { state: 'hidden', timeout: 60000 });
    await page.waitForTimeout(1000);
    
    // Verify the actual OCR results
    await expect(page.getByText('Verification Passed')).toBeVisible();
    await expect(page.getByText(/Brand name.*Eagle Peak.*found on label/i)).toBeVisible();
    await expect(page.getByText(/Product class.*Bourbon Whiskey.*found on label/i)).toBeVisible();
    await expect(page.getByText(/Alcohol content.*45.*matches form/i)).toBeVisible();
    await expect(page.getByText(/Net contents.*750.*found on label/i)).toBeVisible();
    await expect(page.getByText(/Government warning complies with 27 CFR/i)).toBeVisible();
    
    // Visual regression: Verify green bounding boxes are rendered
    const canvas = page.locator('canvas');
    await expect(canvas).toBeVisible();
    await expect(canvas).toHaveScreenshot('scenario1-compliant-bourbon.png', {
      maxDiffPixels: 100,
    });
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
    
    // Wait for processing to complete
    await page.waitForSelector('text="Processing label image..."', { timeout: 5000 });
    await page.waitForSelector('text="Processing label image..."', { state: 'hidden', timeout: 60000 });
    await page.waitForTimeout(1000);
    
    // Verify the actual OCR results for beer
    await expect(page.getByText('Verification Passed')).toBeVisible();
    await expect(page.getByText(/Brand name.*Summit Brew.*found on label/i)).toBeVisible();
    await expect(page.getByText(/Product class.*India Pale Ale.*found on label/i)).toBeVisible();
    await expect(page.getByText(/Alcohol content.*6\.5.*matches form/i)).toBeVisible();
    await expect(page.getByText(/Net contents.*355.*found on label/i)).toBeVisible();
    await expect(page.getByText(/Government warning complies with 27 CFR/i)).toBeVisible();
    
    // Visual regression: Verify green bounding boxes for beer label
    const canvas = page.locator('canvas');
    await expect(canvas).toBeVisible();
    await expect(canvas).toHaveScreenshot('scenario2-compliant-beer.png', {
      maxDiffPixels: 100,
    });
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
    
    // Wait for processing to complete
    await page.waitForSelector('text="Processing label image..."', { timeout: 5000 });
    await page.waitForSelector('text="Processing label image..."', { state: 'hidden', timeout: 60000 });
    await page.waitForTimeout(1000);
    
    // Verify the actual OCR results for wine
    await expect(page.getByText('Verification Passed')).toBeVisible();
    await expect(page.getByText(/Brand name.*Chateau Valley.*found on label/i)).toBeVisible();
    await expect(page.getByText(/Product class.*Cabernet Sauvignon.*found on label/i)).toBeVisible();
    await expect(page.getByText(/Alcohol content.*13\.5.*matches form/i)).toBeVisible();
    await expect(page.getByText(/Net contents.*750.*found on label/i)).toBeVisible();
    // Wine has additional sulfite requirement
    await expect(page.getByText(/Sulfite declaration found on label/i)).toBeVisible();
    
    // Visual regression: Verify green bounding boxes for wine label
    const canvas = page.locator('canvas');
    await expect(canvas).toBeVisible();
    await expect(canvas).toHaveScreenshot('scenario3-compliant-wine.png', {
      maxDiffPixels: 100,
    });
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
    
    // Wait for processing to complete
    await page.waitForSelector('text="Processing label image..."', { timeout: 5000 });
    await page.waitForSelector('text="Processing label image..."', { state: 'hidden', timeout: 60000 });
    await page.waitForTimeout(1000);
    
    // Verify non-compliant result - should show violations
    await expect(page.getByText(/does not match the form|Non-compliant/i).first()).toBeVisible();
    await expect(page.getByText(/Warning non-compliant|violation/i).first()).toBeVisible();
    
    // Visual regression: Verify red bounding boxes for violations
    const canvas = page.locator('canvas');
    await expect(canvas).toBeVisible();
    await expect(canvas).toHaveScreenshot('scenario4-noncompliant-warning.png', {
      maxDiffPixels: 100,
    });
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
    
    // Wait for processing to complete
    await page.waitForSelector('text="Processing label image..."', { timeout: 5000 });
    await page.waitForSelector('text="Processing label image..."', { state: 'hidden', timeout: 60000 });
    await page.waitForTimeout(1000);
    
    // Verify mismatch detected
    await expect(page.getByText(/does not match the form|Non-compliant/i).first()).toBeVisible();
    await expect(page.getByText(/Alcohol content.*differs|mismatch/i).first()).toBeVisible();
    
    // Visual regression: Verify red bounding boxes for mismatch
    const canvas = page.locator('canvas');
    await expect(canvas).toBeVisible();
    await expect(canvas).toHaveScreenshot('scenario5-noncompliant-mismatch.png', {
      maxDiffPixels: 100,
    });
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
    
    // Wait for processing to complete
    await page.waitForSelector('text="Processing label image..."', { timeout: 5000 });
    await page.waitForSelector('text="Processing label image..."', { state: 'hidden', timeout: 60000 });
    await page.waitForTimeout(1000);
    
    // Verify capitalization error detected
    await expect(page.getByText(/does not match the form|Non-compliant/i).first()).toBeVisible();
    await expect(page.getByText(/capital|format|SURGEON GENERAL/i).first()).toBeVisible();
    
    // Visual regression: Verify red bounding boxes for capitalization error
    const canvas = page.locator('canvas');
    await expect(canvas).toBeVisible();
    await expect(canvas).toHaveScreenshot('scenario6-noncompliant-capitalization.png', {
      maxDiffPixels: 100,
    });
  });

  test('Scenario 7: Decorative Font - Fancy Vodka (Enhanced OCR)', async ({ page }) => {
    // Capture console logs
    page.on('console', msg => {
      if (msg.text().includes('[RED BOX DEBUG]') || msg.text().includes('[GREEN BOX DEBUG]')) {
        console.log('BROWSER:', msg.text());
      }
    });
    
    // Fill in the form for Fancy Vodka label with decorative fonts
    await page.locator('#brandName').fill('Fancy Vodka');
    await page.locator('#beverageType').selectOption('spirits');
    await page.locator('#productClass').fill('Vodka');
    await page.locator('#alcoholContent').fill('40');
    await page.locator('#netContents').fill('750');
    
    // Upload the Fancy Vodka test image
    const testImagePath = path.join(__dirname, '../../test_labels/Fancy_Vodka.png');
    await page.locator('#labelImage').setInputFiles(testImagePath);
    
    // Submit the form
    await page.getByRole('button', { name: /verify/i }).click();
    
    // Wait for processing to complete
    await page.waitForSelector('text="Processing label image..."', { timeout: 5000 });
    await page.waitForSelector('text="Processing label image..."', { state: 'hidden', timeout: 60000 });
    await page.waitForTimeout(1000);
    
    // Verify the enhanced OCR successfully extracted decorative brand name
    // Brand, Product, Alcohol, and Net Contents should pass
    await expect(page.getByText(/Brand name.*Fancy Vodka.*found on label/i)).toBeVisible();
    await expect(page.getByText(/Product class.*Vodka.*found on label/i)).toBeVisible();
    await expect(page.getByText(/Alcohol content.*40.*matches form/i)).toBeVisible();
    await expect(page.getByText(/Net contents.*750.*found on label/i)).toBeVisible();
    
    // Note: Government warning will fail due to extra statement (3) - this is expected
    // The label has non-standard text about persons under 21
    
    // Visual regression: Verify bounding boxes are rendered for decorative fonts
    const canvas = page.locator('canvas');
    await expect(canvas).toBeVisible();
    
    // Wait extra time for canvas to fully render all bounding boxes
    await page.waitForTimeout(2000);
    
    await expect(canvas).toHaveScreenshot('scenario7-fancy-vodka-decorative.png', {
      maxDiffPixels: 100,
    });
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
    
    // Wait for processing to start and then complete
    await page.waitForSelector('text="Processing label image..."', { timeout: 5000 });
    await page.waitForSelector('text="Processing label image..."', { state: 'hidden', timeout: 10000 });
    
    // Check for image quality error message
    await expect(page.getByText(/image.*quality|resolution|minimum.*400|size.*small/i)).toBeVisible({ timeout: 5000 });
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
