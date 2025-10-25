"""
Create test label images for different beverage types
Wine and Beer labels with type-specific fields
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_wine_label():
    """Create a wine label with sulfite declaration and vintage year"""
    
    # Create image
    width, height = 800, 1000
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Try to use system fonts, fallback to default
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 70)
        large_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 45)
        medium_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    except:
        title_font = ImageFont.load_default()
        large_font = ImageFont.load_default()
        medium_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw border
    draw.rectangle([(20, 20), (width-20, height-20)], outline='maroon', width=3)
    
    # Brand name
    brand_text = "CHATEAU VALLEY"
    bbox = draw.textbbox((0, 0), brand_text, font=title_font)
    brand_width = bbox[2] - bbox[0]
    draw.text(((width - brand_width) // 2, 80), brand_text, fill='maroon', font=title_font)
    
    # Vintage year
    year_text = "2019"
    bbox = draw.textbbox((0, 0), year_text, font=large_font)
    year_width = bbox[2] - bbox[0]
    draw.text(((width - year_width) // 2, 170), year_text, fill='maroon', font=large_font)
    
    # Separator line
    draw.line([(60, 240), (width-60, 240)], fill='maroon', width=2)
    
    # Product type
    product_line1 = "CABERNET SAUVIGNON"
    bbox1 = draw.textbbox((0, 0), product_line1, font=medium_font)
    width1 = bbox1[2] - bbox1[0]
    draw.text(((width - width1) // 2, 280), product_line1, fill='black', font=medium_font)
    
    product_line2 = "RED WINE"
    bbox2 = draw.textbbox((0, 0), product_line2, font=large_font)
    width2 = bbox2[2] - bbox2[0]
    draw.text(((width - width2) // 2, 320), product_line2, fill='black', font=large_font)
    
    # ABV
    abv_text = "13.5% Alc./Vol."
    bbox = draw.textbbox((0, 0), abv_text, font=medium_font)
    abv_width = bbox[2] - bbox[0]
    draw.text(((width - abv_width) // 2, 400), abv_text, fill='black', font=medium_font)
    
    # Net Contents
    net_text = "750 mL"
    bbox = draw.textbbox((0, 0), net_text, font=medium_font)
    net_width = bbox[2] - bbox[0]
    draw.text(((width - net_width) // 2, 460), net_text, fill='black', font=medium_font)
    
    # Sulfite Declaration
    sulfite_text = "CONTAINS SULFITES"
    bbox = draw.textbbox((0, 0), sulfite_text, font=medium_font)
    sulfite_width = bbox[2] - bbox[0]
    draw.text(((width - sulfite_width) // 2, 540), sulfite_text, fill='black', font=medium_font)
    
    # Government Warning
    warning_text = "GOVERNMENT WARNING: According to the Surgeon General, women\n" \
                   "should not drink alcoholic beverages during pregnancy\n" \
                   "because of the risk of birth defects. Consumption of\n" \
                   "alcoholic beverages impairs your ability to drive a car or\n" \
                   "operate machinery, and may cause health problems."
    
    y_position = 650
    for line in warning_text.split('\n'):
        bbox = draw.textbbox((0, 0), line, font=small_font)
        line_width = bbox[2] - bbox[0]
        draw.text(((width - line_width) // 2, y_position), line, fill='black', font=small_font)
        y_position += 25
    
    # Save image
    output_path = 'test_labels/product_types/wine_label.png'
    os.makedirs('test_labels/product_types', exist_ok=True)
    image.save(output_path, 'PNG')
    print(f"✅ Created wine label: {output_path}")
    print("\nTest with:")
    print("  Brand Name: Chateau Valley")
    print("  Beverage Type: Wine")
    print("  Product Type: Red Wine")
    print("  Alcohol Content: 13.5")
    print("  Net Contents: 750")


def create_beer_label():
    """Create a beer label with ingredients list"""
    
    # Create image
    width, height = 800, 1000
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Try to use system fonts, fallback to default
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 70)
        large_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 45)
        medium_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    except:
        title_font = ImageFont.load_default()
        large_font = ImageFont.load_default()
        medium_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw border
    draw.rectangle([(20, 20), (width-20, height-20)], outline='#D4AF37', width=3)
    
    # Brand name
    brand_text = "MOUNTAIN BREW"
    bbox = draw.textbbox((0, 0), brand_text, font=title_font)
    brand_width = bbox[2] - bbox[0]
    draw.text(((width - brand_width) // 2, 80), brand_text, fill='#D4AF37', font=title_font)
    
    # Separator line
    draw.line([(60, 180), (width-60, 180)], fill='#D4AF37', width=2)
    
    # Product type
    product_line1 = "INDIA PALE ALE"
    bbox1 = draw.textbbox((0, 0), product_line1, font=large_font)
    width1 = bbox1[2] - bbox1[0]
    draw.text(((width - width1) // 2, 220), product_line1, fill='black', font=large_font)
    
    product_line2 = "CRAFT BEER"
    bbox2 = draw.textbbox((0, 0), product_line2, font=medium_font)
    width2 = bbox2[2] - bbox2[0]
    draw.text(((width - width2) // 2, 280), product_line2, fill='black', font=medium_font)
    
    # ABV
    abv_text = "6.5% Alc./Vol."
    bbox = draw.textbbox((0, 0), abv_text, font=medium_font)
    abv_width = bbox[2] - bbox[0]
    draw.text(((width - abv_width) // 2, 350), abv_text, fill='black', font=medium_font)
    
    # Net Contents
    net_text = "355 mL"
    bbox = draw.textbbox((0, 0), net_text, font=medium_font)
    net_width = bbox[2] - bbox[0]
    draw.text(((width - net_width) // 2, 410), net_text, fill='black', font=medium_font)
    
    # Ingredients
    ingredients_title = "INGREDIENTS:"
    bbox = draw.textbbox((0, 0), ingredients_title, font=medium_font)
    title_width = bbox[2] - bbox[0]
    draw.text(((width - title_width) // 2, 490), ingredients_title, fill='#D4AF37', font=medium_font)
    
    ingredients_text = "Water, Malted Barley, Hops, Yeast"
    bbox = draw.textbbox((0, 0), ingredients_text, font=small_font)
    ingredients_width = bbox[2] - bbox[0]
    draw.text(((width - ingredients_width) // 2, 530), ingredients_text, fill='black', font=small_font)
    
    # Government Warning
    warning_text = "GOVERNMENT WARNING: According to the Surgeon General, women\n" \
                   "should not drink alcoholic beverages during pregnancy\n" \
                   "because of the risk of birth defects. Consumption of\n" \
                   "alcoholic beverages impairs your ability to drive a car or\n" \
                   "operate machinery, and may cause health problems."
    
    y_position = 640
    for line in warning_text.split('\n'):
        bbox = draw.textbbox((0, 0), line, font=small_font)
        line_width = bbox[2] - bbox[0]
        draw.text(((width - line_width) // 2, y_position), line, fill='black', font=small_font)
        y_position += 25
    
    # Save image
    output_path = 'test_labels/product_types/beer_label.png'
    os.makedirs('test_labels/product_types', exist_ok=True)
    image.save(output_path, 'PNG')
    print(f"\n✅ Created beer label: {output_path}")
    print("\nTest with:")
    print("  Brand Name: Mountain Brew")
    print("  Beverage Type: Beer")
    print("  Product Type: India Pale Ale")
    print("  Alcohol Content: 6.5")
    print("  Net Contents: 355")


if __name__ == '__main__':
    print("Creating test labels for multiple product types...\n")
    create_wine_label()
    create_beer_label()
    print("\n✅ All test labels created successfully!")
