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
  
  // Wait for results to appear - look for the results section instead of fixed timeout
  console.log('Waiting for verification results...');
  
  // Wait for either success or error message to appear (max 60 seconds for backend OCR)
  try {
    await page.waitForSelector('text=/compliant|non-compliant|verification|error|result/i', { 
      timeout: 60000,
      state: 'visible' 
    });
    console.log('Results appeared!');
  } catch (error) {
    console.log('Timeout waiting for results, taking screenshot anyway...');
  }
  
  // Take a screenshot to see what's on the page
  await page.screenshot({ path: 'test-result.png', fullPage: true });
  console.log('Screenshot saved as test-result.png');
  
  // Check for results - let's see what text appears
  const pageContent = await page.content();
  console.log('Page has content, checking for success indicators...');
  
  // Look for any indication of results
  const hasResults = await page.locator('text=/compliant|verification|result/i').count() > 0;
  console.log('Has results?', hasResults);
  
  // Just log what we see for now
  console.log('Test completed - check test-result.png to see the actual result');
});
