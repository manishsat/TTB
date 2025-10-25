"""
Create test labels for different beverage types with compliant warnings
- Wine label with sulfites and compliant warning
- Beer label with ingredients and compliant warning
"""
from PIL import Image, ImageDraw, ImageFont
import os

COMPLIANT_WARNING = """GOVERNMENT WARNING: (1) According to the Surgeon General, women should not drink alcoholic beverages during pregnancy because of the risk of birth defects. (2) Consumption of alcoholic beverages impairs your ability to drive a car or operate machinery, and may cause health problems."""

def create_wine_label():
    """Create a wine label with sulfites and compliant warning"""
    
    width, height = 800, 1100
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
        medium_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except:
        title_font = ImageFont.load_default()
        medium_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Border
    draw.rectangle([(20, 20), (width-20, height-20)], outline='darkred', width=4)
    
    # Brand
    brand_text = "CHÂTEAU VALLEY"
    bbox = draw.textbbox((0, 0), brand_text, font=title_font)
    brand_width = bbox[2] - bbox[0]
    draw.text(((width - brand_width) // 2, 70), brand_text, fill='darkred', font=title_font)
    
    draw.line([(60, 160), (width-60, 160)], fill='darkred', width=2)
    
    # Product type
    product_text = "CABERNET SAUVIGNON"
    bbox = draw.textbbox((0, 0), product_text, font=medium_font)
    product_width = bbox[2] - bbox[0]
    draw.text(((width - product_width) // 2, 200), product_text, fill='black', font=medium_font)
    
    # Vintage
    vintage_text = "2019"
    bbox = draw.textbbox((0, 0), vintage_text, font=medium_font)
    vintage_width = bbox[2] - bbox[0]
    draw.text(((width - vintage_width) // 2, 250), vintage_text, fill='black', font=medium_font)
    
    # ABV
    abv_text = "13.5% Alc./Vol."
    bbox = draw.textbbox((0, 0), abv_text, font=medium_font)
    abv_width = bbox[2] - bbox[0]
    draw.text(((width - abv_width) // 2, 310), abv_text, fill='black', font=medium_font)
    
    # Net Contents
    net_text = "750 mL"
    bbox = draw.textbbox((0, 0), net_text, font=medium_font)
    net_width = bbox[2] - bbox[0]
    draw.text(((width - net_width) // 2, 370), net_text, fill='black', font=medium_font)
    
    # SULFITES WARNING
    sulfites_text = "CONTAINS SULFITES"
    bbox = draw.textbbox((0, 0), sulfites_text, font=medium_font)
    sulfites_width = bbox[2] - bbox[0]
    draw.text(((width - sulfites_width) // 2, 430), sulfites_text, fill='black', font=medium_font)
    
    # COMPLIANT Government Warning
    warning_lines = [
        "GOVERNMENT WARNING: (1) According to the Surgeon General,",
        "women should not drink alcoholic beverages during pregnancy",
        "because of the risk of birth defects. (2) Consumption of",
        "alcoholic beverages impairs your ability to drive a car or",
        "operate machinery, and may cause health problems."
    ]
    
    y_position = 520
    for line in warning_lines:
        bbox = draw.textbbox((0, 0), line, font=small_font)
        line_width = bbox[2] - bbox[0]
        draw.text(((width - line_width) // 2, y_position), line, fill='black', font=small_font)
        y_position += 22
    
    # Save
    output_path = 'test_labels/compliance_tests/wine_compliant.png'
    os.makedirs('test_labels/compliance_tests', exist_ok=True)
    image.save(output_path, 'PNG')
    print(f"✅ Created wine label with compliant warning: {output_path}")


def create_beer_label():
    """Create a beer label with ingredients and compliant warning"""
    
    width, height = 800, 1100
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 70)
        medium_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
    except:
        title_font = ImageFont.load_default()
        medium_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Border
    draw.rectangle([(20, 20), (width-20, height-20)], outline='goldenrod', width=4)
    
    # Brand
    brand_text = "SUMMIT BREW"
    bbox = draw.textbbox((0, 0), brand_text, font=title_font)
    brand_width = bbox[2] - bbox[0]
    draw.text(((width - brand_width) // 2, 70), brand_text, fill='darkorange', font=title_font)
    
    draw.line([(60, 170), (width-60, 170)], fill='goldenrod', width=2)
    
    # Product type
    product_text = "INDIA PALE ALE"
    bbox = draw.textbbox((0, 0), product_text, font=medium_font)
    product_width = bbox[2] - bbox[0]
    draw.text(((width - product_width) // 2, 210), product_text, fill='black', font=medium_font)
    
    # ABV
    abv_text = "6.5% Alc./Vol."
    bbox = draw.textbbox((0, 0), abv_text, font=medium_font)
    abv_width = bbox[2] - bbox[0]
    draw.text(((width - abv_width) // 2, 270), abv_text, fill='black', font=medium_font)
    
    # Net Contents
    net_text = "355 mL"
    bbox = draw.textbbox((0, 0), net_text, font=medium_font)
    net_width = bbox[2] - bbox[0]
    draw.text(((width - net_width) // 2, 330), net_text, fill='black', font=medium_font)
    
    # INGREDIENTS
    ingredients_title = "INGREDIENTS:"
    bbox = draw.textbbox((0, 0), ingredients_title, font=medium_font)
    ing_width = bbox[2] - bbox[0]
    draw.text(((width - ing_width) // 2, 390), ingredients_title, fill='black', font=medium_font)
    
    ingredients_text = "Water, Malted Barley, Hops, Yeast"
    bbox = draw.textbbox((0, 0), ingredients_text, font=small_font)
    ing_text_width = bbox[2] - bbox[0]
    draw.text(((width - ing_text_width) // 2, 425), ingredients_text, fill='black', font=small_font)
    
    # COMPLIANT Government Warning
    warning_lines = [
        "GOVERNMENT WARNING: (1) According to the Surgeon General,",
        "women should not drink alcoholic beverages during pregnancy",
        "because of the risk of birth defects. (2) Consumption of",
        "alcoholic beverages impairs your ability to drive a car or",
        "operate machinery, and may cause health problems."
    ]
    
    y_position = 510
    for line in warning_lines:
        bbox = draw.textbbox((0, 0), line, font=small_font)
        line_width = bbox[2] - bbox[0]
        draw.text(((width - line_width) // 2, y_position), line, fill='black', font=small_font)
        y_position += 22
    
    # Save
    output_path = 'test_labels/compliance_tests/beer_compliant.png'
    image.save(output_path, 'PNG')
    print(f"✅ Created beer label with compliant warning: {output_path}")


if __name__ == '__main__':
    print("Creating beverage type test labels with compliant warnings...\n")
    create_wine_label()
    create_beer_label()
    print("\n✅ All beverage type compliance labels created!")
    print("\nTest scenarios:")
    print("1. wine_compliant.png - Wine with SULFITES + compliant warning")
    print("2. beer_compliant.png - Beer with INGREDIENTS + compliant warning")
