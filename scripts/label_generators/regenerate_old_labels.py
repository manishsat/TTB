#!/usr/bin/env python3
"""Regenerate old test labels with compliant government warnings."""

from PIL import Image, ImageDraw, ImageFont
import os

# Full compliant government warning per 27 CFR 16.21
COMPLIANT_WARNING = """GOVERNMENT WARNING: (1) According to the Surgeon
General, women should not drink alcoholic beverages
during pregnancy because of the risk of birth defects.
(2) Consumption of alcoholic beverages impairs your
ability to drive a car or operate machinery, and may
cause health problems."""

def create_label_with_warning(
    filename,
    brand_name,
    product_name,
    alcohol_content,
    net_contents,
    additional_text="",
    beverage_type="Spirit"
):
    """Create a label image with compliant government warning."""
    # Image dimensions
    width = 800
    height = 1000
    
    # Create image
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
        product_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
        info_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
        warning_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except:
        title_font = ImageFont.load_default()
        product_font = ImageFont.load_default()
        info_font = ImageFont.load_default()
        warning_font = ImageFont.load_default()
    
    y_position = 50
    
    # Brand name
    draw.text((width//2, y_position), brand_name, font=title_font, fill='black', anchor='mt')
    y_position += 80
    
    # Product name
    draw.text((width//2, y_position), product_name, font=product_font, fill='black', anchor='mt')
    y_position += 60
    
    # Alcohol content
    draw.text((width//2, y_position), f"{alcohol_content}%", font=info_font, fill='black', anchor='mt')
    y_position += 50
    
    # Net contents
    draw.text((width//2, y_position), f"{net_contents} mL", font=info_font, fill='black', anchor='mt')
    y_position += 50
    
    # Additional text (for special labels)
    if additional_text:
        draw.text((width//2, y_position), additional_text, font=info_font, fill='black', anchor='mt')
        y_position += 50
    
    # Add some spacing before warning
    y_position += 30
    
    # Government warning - wrapped text
    warning_lines = COMPLIANT_WARNING.split('\n')
    for line in warning_lines:
        draw.text((50, y_position), line, font=warning_font, fill='black')
        y_position += 22
    
    # Save image
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename)
    print(f"✓ Created: {filename}")

# Regenerate all non-compliant labels
print("Regenerating old test labels with compliant government warnings...")
print("=" * 80)

# Main test labels
create_label_with_warning(
    "test_labels/clear_bourbon.png",
    "Crystal Clear",
    "Bourbon Whiskey",
    "45",
    "750"
)

create_label_with_warning(
    "test_labels/low_contrast_vodka.png",
    "Smooth Spirit",
    "Premium Vodka",
    "40",
    "750"
)

create_label_with_warning(
    "test_labels/test_ocr.png",
    "OCR Test",
    "Bourbon Whiskey",
    "43",
    "750"
)

# Failure test labels
create_label_with_warning(
    "test_labels/failures/wrong_alcohol_content.png",
    "Mountain Peak",
    "Bourbon Whiskey",
    "50",  # Different from expected
    "750"
)

create_label_with_warning(
    "test_labels/failures/wrong_brand.png",
    "Wrong Brand Name",
    "Bourbon Whiskey",
    "45",
    "750"
)

create_label_with_warning(
    "test_labels/failures/wrong_product_type.png",
    "Mountain Peak",
    "Rye Whiskey",  # Different product type
    "45",
    "750"
)

create_label_with_warning(
    "test_labels/failures/wrong_volume.png",
    "Mountain Peak",
    "Bourbon Whiskey",
    "45",
    "700"  # Different volume
)

# OCR tolerance test
create_label_with_warning(
    "test_labels/ocr_tolerance_tests/error_tolerance_test.png",
    "Mountaln Peak",  # Intentional OCR error: "i" looks like "l"
    "Bourbon Whiskey",
    "45",
    "750"
)

# Product type specific labels
create_label_with_warning(
    "test_labels/product_types/beer_label.png",
    "Craft Brewery",
    "IPA",
    "6.5",
    "355",
    "INGREDIENTS: Water, Malted Barley, Hops, Yeast",
    "Beer"
)

create_label_with_warning(
    "test_labels/product_types/wine_label.png",
    "Vineyard Estate",
    "Cabernet Sauvignon",
    "13.5",
    "750",
    "CONTAINS SULFITES",
    "Wine"
)

print("=" * 80)
print("✅ All labels regenerated with compliant government warnings!")
