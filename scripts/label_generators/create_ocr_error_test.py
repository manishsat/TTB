"""
Create a test label image with intentional OCR-like errors
to demonstrate fuzzy matching tolerance
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_ocr_error_label():
    """Create a bourbon label with OCR-like errors"""
    
    # Create image
    width, height = 800, 1000
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Try to use system fonts, fallback to default
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
        large_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 50)
        medium_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 35)
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    except:
        title_font = ImageFont.load_default()
        large_font = ImageFont.load_default()
        medium_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw border
    draw.rectangle([(20, 20), (width-20, height-20)], outline='black', width=3)
    
    # Brand name with errors: "Eagle Peak" → "Eagie Peak" (l→i)
    brand_text = "EAGIE PEAK"
    bbox = draw.textbbox((0, 0), brand_text, font=title_font)
    brand_width = bbox[2] - bbox[0]
    draw.text(((width - brand_width) // 2, 100), brand_text, fill='black', font=title_font)
    
    # Separator line
    draw.line([(60, 200), (width-60, 200)], fill='black', width=2)
    
    # Product type with errors: "BOURBON" → "B0URB0N" (O→0)
    product_line1 = "KENTUCKY STRAIGHT"
    product_line2 = "B0URB0N WHISKEY"  # O→0 errors
    
    bbox1 = draw.textbbox((0, 0), product_line1, font=medium_font)
    width1 = bbox1[2] - bbox1[0]
    draw.text(((width - width1) // 2, 260), product_line1, fill='black', font=medium_font)
    
    bbox2 = draw.textbbox((0, 0), product_line2, font=large_font)
    width2 = bbox2[2] - bbox2[0]
    draw.text(((width - width2) // 2, 310), product_line2, fill='black', font=large_font)
    
    # Age statement - missing character: "Aged 4 Years" → "Aged 4Year" (missing s)
    age_text = "Aged 4 Year"  # Missing 's'
    bbox = draw.textbbox((0, 0), age_text, font=medium_font)
    age_width = bbox[2] - bbox[0]
    draw.text(((width - age_width) // 2, 420), age_text, fill='black', font=medium_font)
    
    # ABV - correct
    abv_text = "45% Alc./Vol. (90 Proof)"
    bbox = draw.textbbox((0, 0), abv_text, font=medium_font)
    abv_width = bbox[2] - bbox[0]
    draw.text(((width - abv_width) // 2, 520), abv_text, fill='black', font=medium_font)
    
    # Net Contents - correct
    net_value = "750 mL"
    
    bbox_value = draw.textbbox((0, 0), net_value, font=large_font)
    value_width = bbox_value[2] - bbox_value[0]
    draw.text(((width - value_width) // 2, 630), net_value, fill='black', font=large_font)
    
    # Government Warning - correct
    warning_text = "GOVERNMENT WARNING: According to the Surgeon General, women\n" \
                   "should not drink alcoholic beverages during pregnancy\n" \
                   "because of the risk of birth defects. Consumption of\n" \
                   "alcoholic beverages impairs your ability to drive a car or\n" \
                   "operate machinery, and may cause health problems."
    
    y_position = 730
    for line in warning_text.split('\n'):
        bbox = draw.textbbox((0, 0), line, font=small_font)
        line_width = bbox[2] - bbox[0]
        draw.text(((width - line_width) // 2, y_position), line, fill='black', font=small_font)
        y_position += 25
    
    # Save image
    output_path = 'test_labels/ocr_tolerance_tests/error_tolerance_test.png'
    os.makedirs('test_labels/ocr_tolerance_tests', exist_ok=True)
    image.save(output_path, 'PNG')
    print(f"✅ Created test label: {output_path}")
    print("\nThis label has intentional OCR-like errors:")
    print("  - Brand: 'EAGIE PEAK' instead of 'EAGLE PEAK' (l→i)")
    print("  - Product: 'B0URB0N' instead of 'BOURBON' (O→0)")
    print("  - Age: 'Aged 4 Year' instead of 'Aged 4 Years' (missing s)")
    print("\nTest with these correct values:")
    print("  Brand Name: Eagle Peak")
    print("  Product Type: Bourbon Whiskey")
    print("  Alcohol Content: 45")
    print("  Net Contents: 750")
    print("\nFuzzy matching should PASS despite the errors!")

if __name__ == '__main__':
    create_ocr_error_label()
