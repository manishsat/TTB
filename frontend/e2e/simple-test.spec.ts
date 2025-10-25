import { test, expect } from '@playwright/test';
import path from 'path';
import { fileURLToPath } from 'url';

// Fix for __dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Single E2E Test for debugging
 * Testing Scenario 1: Compliant Standard Bourbon
 */

test('Scenario 1: Compliant Standard Bourbon - Should Pass', async ({ page }) => {
  // Increase timeout to 60 seconds for this test
  test.setTimeout(60000);
  
  // Navigate to the application
  console.log('Navigating to app...');
  await page.goto('/');
  
  // Wait for the form to be visible
  await expect(page.getByText('Label Application Form')).toBeVisible();
  console.log('Form loaded');
  
  // Fill in Brand Name using id selector
  console.log('Filling brand name...');
  await page.locator('#brandName').fill('Eagle Peak');
  
  // Select Beverage Type (already defaults to spirits, but let's be explicit)
  console.log('Selecting beverage type...');
  await page.locator('#beverageType').selectOption('spirits');
  
  // Fill in Product Class using id selector
  console.log('Filling product class...');
  await page.locator('#productClass').fill('Bourbon Whiskey');
  
  // Fill in Alcohol Content using id selector
  console.log('Filling alcohol content...');
  await page.locator('#alcoholContent').fill('45');
  
  // Fill in Net Contents using id selector (optional field)
  console.log('Filling net contents...');
  await page.locator('#netContents').fill('750');
  
  // Upload the test image
  console.log('Uploading image...');
  const testImagePath = path.join(__dirname, '../../test_labels/compliance_tests/compliant_warning.png');
  await page.locator('#labelImage').setInputFiles(testImagePath);
  
  // Wait a moment to see the preview
  await page.waitForTimeout(1000);
  console.log('Image uploaded, preview should show');
  
  // Submit the form - look for button with text containing "Verify"
  console.log('Clicking verify button...');
  await page.getByRole('button', { name: /verify/i }).click();
  
  // Wait for processing to complete
  console.log('Waiting for verification results...');
  await page.waitForSelector('text="Processing label image..."', { timeout: 5000 });
  console.log('Processing started...');
  await page.waitForSelector('text="Processing label image..."', { state: 'hidden', timeout: 60000 });
  console.log('Processing completed!');
  await page.waitForTimeout(1000);
  
  // Take a screenshot to see the results
  await page.screenshot({ path: 'test-result.png', fullPage: true });
  console.log('Screenshot saved as test-result.png');
  
  // Verify the actual OCR results from the backend
  console.log('Checking for verification results...');
  
  // Check for "Verification Passed" heading
  await expect(page.getByText('Verification Passed')).toBeVisible();
  console.log('✓ Found "Verification Passed"');
  
  // Verify all Field Verification Details:
  
  // 1. Brand Name
  await expect(page.getByText(/Brand name.*Eagle Peak.*found on label/i)).toBeVisible();
  console.log('✓ Brand Name verified');
  
  // 2. Product Class/Type
  await expect(page.getByText(/Product class.*Bourbon Whiskey.*found on label/i)).toBeVisible();
  console.log('✓ Product Class verified');
  
  // 3. Alcohol Content
  await expect(page.getByText(/Alcohol content.*45.*matches form/i)).toBeVisible();
  console.log('✓ Alcohol Content verified');
  
  // 4. Net Contents
  await expect(page.getByText(/Net contents.*750.*found on label/i)).toBeVisible();
  console.log('✓ Net Contents verified');
  
  // 5. Government Warning (Detailed)
  await expect(page.getByText('Government Warning (Detailed)')).toBeVisible();
  await expect(page.getByText(/Government warning complies with 27 CFR/i)).toBeVisible();
  console.log('✓ Government Warning verified');
  
  // 6. Visual Regression: Verify bounding boxes are rendered correctly
  console.log('Verifying bounding box rendering...');
  const canvas = page.locator('canvas');
  await expect(canvas).toBeVisible();
  
  // Verify the canvas has content (width and height > 0)
  const canvasSize = await canvas.evaluate((el: HTMLCanvasElement) => ({
    width: el.width,
    height: el.height
  }));
  expect(canvasSize.width).toBeGreaterThan(0);
  expect(canvasSize.height).toBeGreaterThan(0);
  console.log(`✓ Canvas rendered with size: ${canvasSize.width}x${canvasSize.height}`);
  
  // Visual regression test: Compare canvas screenshot with baseline
  await expect(canvas).toHaveScreenshot('compliant-bourbon-boxes.png', {
    maxDiffPixels: 100,  // Allow minor rendering differences
  });
  console.log('✓ Bounding boxes match baseline image');
  
  console.log('Test completed successfully - all 5 field verifications + visual regression passed!');
});
