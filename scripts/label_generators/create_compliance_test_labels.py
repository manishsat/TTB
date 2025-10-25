"""
Create test labels to validate detailed government warning compliance
- Compliant warning (exact text)
- Non-compliant warnings (various violations)
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Official TTB warning text
COMPLIANT_WARNING = """GOVERNMENT WARNING: (1) According to the Surgeon General, women should not drink alcoholic beverages during pregnancy because of the risk of birth defects. (2) Consumption of alcoholic beverages impairs your ability to drive a car or operate machinery, and may cause health problems."""

def create_compliant_label():
    """Create a label with fully compliant government warning"""
    
    width, height = 800, 1000
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 70)
        medium_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except:
        title_font = ImageFont.load_default()
        medium_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Border
    draw.rectangle([(20, 20), (width-20, height-20)], outline='black', width=3)
    
    # Brand
    brand_text = "EAGLE PEAK"
    bbox = draw.textbbox((0, 0), brand_text, font=title_font)
    brand_width = bbox[2] - bbox[0]
    draw.text(((width - brand_width) // 2, 80), brand_text, fill='black', font=title_font)
    
    draw.line([(60, 180), (width-60, 180)], fill='black', width=2)
    
    # Product type
    product_text = "BOURBON WHISKEY"
    bbox = draw.textbbox((0, 0), product_text, font=medium_font)
    product_width = bbox[2] - bbox[0]
    draw.text(((width - product_width) // 2, 220), product_text, fill='black', font=medium_font)
    
    # ABV
    abv_text = "45% Alc./Vol."
    bbox = draw.textbbox((0, 0), abv_text, font=medium_font)
    abv_width = bbox[2] - bbox[0]
    draw.text(((width - abv_width) // 2, 280), abv_text, fill='black', font=medium_font)
    
    # Net Contents
    net_text = "750 mL"
    bbox = draw.textbbox((0, 0), net_text, font=medium_font)
    net_width = bbox[2] - bbox[0]
    draw.text(((width - net_width) // 2, 340), net_text, fill='black', font=medium_font)
    
    # COMPLIANT Government Warning
    warning_lines = [
        "GOVERNMENT WARNING: (1) According to the Surgeon General,",
        "women should not drink alcoholic beverages during pregnancy",
        "because of the risk of birth defects. (2) Consumption of",
        "alcoholic beverages impairs your ability to drive a car or",
        "operate machinery, and may cause health problems."
    ]
    
    y_position = 450
    for line in warning_lines:
        bbox = draw.textbbox((0, 0), line, font=small_font)
        line_width = bbox[2] - bbox[0]
        draw.text(((width - line_width) // 2, y_position), line, fill='black', font=small_font)
        y_position += 22
    
    # Save
    output_path = 'test_labels/compliance_tests/compliant_warning.png'
    os.makedirs('test_labels/compliance_tests', exist_ok=True)
    image.save(output_path, 'PNG')
    print(f"✅ Created compliant warning label: {output_path}")


def create_lowercase_surgeon_general_label():
    """Non-compliant: 'surgeon general' instead of 'Surgeon General'"""
    
    width, height = 800, 1000
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 70)
        medium_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except:
        title_font = ImageFont.load_default()
        medium_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    draw.rectangle([(20, 20), (width-20, height-20)], outline='black', width=3)
    
    brand_text = "TEST SPIRITS"
    bbox = draw.textbbox((0, 0), brand_text, font=title_font)
    brand_width = bbox[2] - bbox[0]
    draw.text(((width - brand_width) // 2, 80), brand_text, fill='black', font=title_font)
    
    draw.line([(60, 180), (width-60, 180)], fill='black', width=2)
    
    product_text = "VODKA"
    bbox = draw.textbbox((0, 0), product_text, font=medium_font)
    product_width = bbox[2] - bbox[0]
    draw.text(((width - product_width) // 2, 220), product_text, fill='black', font=medium_font)
    
    abv_text = "40% Alc./Vol."
    bbox = draw.textbbox((0, 0), abv_text, font=medium_font)
    abv_width = bbox[2] - bbox[0]
    draw.text(((width - abv_width) // 2, 280), abv_text, fill='black', font=medium_font)
    
    net_text = "750 mL"
    bbox = draw.textbbox((0, 0), net_text, font=medium_font)
    net_width = bbox[2] - bbox[0]
    draw.text(((width - net_width) // 2, 340), net_text, fill='black', font=medium_font)
    
    # NON-COMPLIANT: lowercase "surgeon general"
    warning_lines = [
        "GOVERNMENT WARNING: (1) According to the surgeon general,",  # ❌ lowercase
        "women should not drink alcoholic beverages during pregnancy",
        "because of the risk of birth defects. (2) Consumption of",
        "alcoholic beverages impairs your ability to drive a car or",
        "operate machinery, and may cause health problems."
    ]
    
    y_position = 450
    for line in warning_lines:
        bbox = draw.textbbox((0, 0), line, font=small_font)
        line_width = bbox[2] - bbox[0]
        draw.text(((width - line_width) // 2, y_position), line, fill='black', font=small_font)
        y_position += 22
    
    output_path = 'test_labels/compliance_tests/noncompliant_lowercase_sg.png'
    image.save(output_path, 'PNG')
    print(f"✅ Created non-compliant label (lowercase surgeon general): {output_path}")


def create_missing_statement_2_label():
    """Non-compliant: Missing statement (2)"""
    
    width, height = 800, 1000
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 70)
        medium_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except:
        title_font = ImageFont.load_default()
        medium_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    draw.rectangle([(20, 20), (width-20, height-20)], outline='black', width=3)
    
    brand_text = "TEST RUM"
    bbox = draw.textbbox((0, 0), brand_text, font=title_font)
    brand_width = bbox[2] - bbox[0]
    draw.text(((width - brand_width) // 2, 80), brand_text, fill='black', font=title_font)
    
    draw.line([(60, 180), (width-60, 180)], fill='black', width=2)
    
    product_text = "SPICED RUM"
    bbox = draw.textbbox((0, 0), product_text, font=medium_font)
    product_width = bbox[2] - bbox[0]
    draw.text(((width - product_width) // 2, 220), product_text, fill='black', font=medium_font)
    
    abv_text = "35% Alc./Vol."
    bbox = draw.textbbox((0, 0), abv_text, font=medium_font)
    abv_width = bbox[2] - bbox[0]
    draw.text(((width - abv_width) // 2, 280), abv_text, fill='black', font=medium_font)
    
    net_text = "700 mL"
    bbox = draw.textbbox((0, 0), net_text, font=medium_font)
    net_width = bbox[2] - bbox[0]
    draw.text(((width - net_width) // 2, 340), net_text, fill='black', font=medium_font)
    
    # NON-COMPLIANT: Missing statement (2)
    warning_lines = [
        "GOVERNMENT WARNING: (1) According to the Surgeon General,",
        "women should not drink alcoholic beverages during pregnancy",
        "because of the risk of birth defects.",  # ❌ Missing statement (2)
    ]
    
    y_position = 450
    for line in warning_lines:
        bbox = draw.textbbox((0, 0), line, font=small_font)
        line_width = bbox[2] - bbox[0]
        draw.text(((width - line_width) // 2, y_position), line, fill='black', font=small_font)
        y_position += 22
    
    output_path = 'test_labels/compliance_tests/noncompliant_missing_statement2.png'
    image.save(output_path, 'PNG')
    print(f"✅ Created non-compliant label (missing statement 2): {output_path}")


if __name__ == '__main__':
    print("Creating detailed compliance test labels...\n")
    create_compliant_label()
    create_lowercase_surgeon_general_label()
    create_missing_statement_2_label()
    print("\n✅ All compliance test labels created!")
    print("\nTest scenarios:")
    print("1. compliant_warning.png - Should PASS all checks")
    print("2. noncompliant_lowercase_sg.png - Should FAIL (lowercase 'surgeon general')")
    print("3. noncompliant_missing_statement2.png - Should FAIL (missing statement 2)")
