"""
Create failure test images for testing mismatch detection
These images are intentionally wrong to test verification logic
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

# Create failures directory
os.makedirs('test_labels/failures', exist_ok=True)

def get_fonts():
    """Try to load system fonts, fallback to default"""
    try:
        title_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 70)
        large_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 50)
        medium_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 30)
        warning_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 18)
        return title_font, large_font, medium_font, warning_font
    except:
        default = ImageFont.load_default()
        return default, default, default, default


def add_government_warning(draw, y_position, width, warning_font):
    """Add government warning text"""
    warning_text = "GOVERNMENT WARNING: According to the Surgeon General, women should not drink alcoholic beverages during pregnancy because of the risk of birth defects. Consumption of alcoholic beverages impairs your ability to drive a car or operate machinery, and may cause health problems."
    
    lines = textwrap.wrap(warning_text, width=70)
    for i, line in enumerate(lines):
        draw.text((width//2, y_position + i*25), line, fill='black', font=warning_font, anchor='mm')


def create_wrong_alcohol_content():
    """Label with WRONG alcohol percentage"""
    img = Image.new('RGB', (800, 1200), color='white')
    draw = ImageDraw.Draw(img)
    title_font, large_font, medium_font, warning_font = get_fonts()
    
    draw.rectangle([(10, 10), (790, 1190)], outline='black', width=5)
    draw.text((400, 80), 'WRONG PROOF DISTILLERY', fill='black', font=title_font, anchor='mm')
    draw.line([(50, 140), (750, 140)], fill='black', width=2)
    draw.text((400, 220), 'KENTUCKY STRAIGHT', fill='black', font=medium_font, anchor='mm')
    draw.text((400, 280), 'BOURBON WHISKEY', fill='black', font=large_font, anchor='mm')
    draw.text((400, 380), 'Aged 4 Years', fill='black', font=medium_font, anchor='mm')
    
    # WRONG: Label shows 40% but form will say 45%
    draw.text((400, 460), '40% Alc./Vol. (80 Proof)', fill='black', font=large_font, anchor='mm')
    draw.text((400, 540), '750 mL', fill='black', font=large_font, anchor='mm')
    
    add_government_warning(draw, 650, 800, warning_font)
    
    img.save('test_labels/failures/wrong_alcohol_content.png')
    print("✓ Created: wrong_alcohol_content.png")
    print("   Form values: Brand='Wrong Proof Distillery', Type='Bourbon Whiskey', ABV=45%, Net=750")
    print("   Expected: FAIL - Alcohol content mismatch (40% vs 45%)")


def create_wrong_volume():
    """Label with WRONG net contents"""
    img = Image.new('RGB', (800, 1200), color='white')
    draw = ImageDraw.Draw(img)
    title_font, large_font, medium_font, warning_font = get_fonts()
    
    draw.rectangle([(10, 10), (790, 1190)], outline='black', width=5)
    draw.text((400, 80), 'WRONG SIZE BREWERY', fill='black', font=title_font, anchor='mm')
    draw.line([(50, 140), (750, 140)], fill='black', width=2)
    draw.text((400, 220), 'CRAFT', fill='black', font=medium_font, anchor='mm')
    draw.text((400, 280), 'PALE ALE', fill='black', font=large_font, anchor='mm')
    draw.text((400, 460), '5.5% Alc./Vol.', fill='black', font=large_font, anchor='mm')
    
    # WRONG: Label shows 355 mL but form will say 750
    draw.text((400, 540), '355 mL', fill='black', font=large_font, anchor='mm')
    
    add_government_warning(draw, 650, 800, warning_font)
    
    img.save('test_labels/failures/wrong_volume.png')
    print("✓ Created: wrong_volume.png")
    print("   Form values: Brand='Wrong Size Brewery', Type='Pale Ale', ABV=5.5%, Net=750")
    print("   Expected: FAIL - Net contents mismatch (355 mL vs 750)")


def create_wrong_brand():
    """Label with DIFFERENT brand name"""
    img = Image.new('RGB', (800, 1200), color='white')
    draw = ImageDraw.Draw(img)
    title_font, large_font, medium_font, warning_font = get_fonts()
    
    draw.rectangle([(10, 10), (790, 1190)], outline='black', width=5)
    
    # Label says "SUNSET DISTILLERY" but form will say "Eagle Peak"
    draw.text((400, 80), 'SUNSET DISTILLERY', fill='black', font=title_font, anchor='mm')
    draw.line([(50, 140), (750, 140)], fill='black', width=2)
    draw.text((400, 220), 'KENTUCKY STRAIGHT', fill='black', font=medium_font, anchor='mm')
    draw.text((400, 280), 'BOURBON WHISKEY', fill='black', font=large_font, anchor='mm')
    draw.text((400, 380), 'Aged 8 Years', fill='black', font=medium_font, anchor='mm')
    draw.text((400, 460), '45% Alc./Vol. (90 Proof)', fill='black', font=large_font, anchor='mm')
    draw.text((400, 540), '750 mL', fill='black', font=large_font, anchor='mm')
    
    add_government_warning(draw, 650, 800, warning_font)
    
    img.save('test_labels/failures/wrong_brand.png')
    print("✓ Created: wrong_brand.png")
    print("   Form values: Brand='Eagle Peak', Type='Bourbon Whiskey', ABV=45%, Net=750")
    print("   Expected: FAIL - Brand name mismatch (Sunset Distillery vs Eagle Peak)")


def create_wrong_product_type():
    """Label with WRONG product class"""
    img = Image.new('RGB', (800, 1200), color='white')
    draw = ImageDraw.Draw(img)
    title_font, large_font, medium_font, warning_font = get_fonts()
    
    draw.rectangle([(10, 10), (790, 1190)], outline='black', width=5)
    draw.text((400, 80), 'MOUNTAIN SPIRITS', fill='black', font=title_font, anchor='mm')
    draw.line([(50, 140), (750, 140)], fill='black', width=2)
    
    # WRONG: Label says "RYE WHISKEY" but form will say "Bourbon Whiskey"
    draw.text((400, 220), 'STRAIGHT', fill='black', font=medium_font, anchor='mm')
    draw.text((400, 280), 'RYE WHISKEY', fill='black', font=large_font, anchor='mm')
    draw.text((400, 380), 'Aged 4 Years', fill='black', font=medium_font, anchor='mm')
    draw.text((400, 460), '45% Alc./Vol. (90 Proof)', fill='black', font=large_font, anchor='mm')
    draw.text((400, 540), '750 mL', fill='black', font=large_font, anchor='mm')
    
    add_government_warning(draw, 650, 800, warning_font)
    
    img.save('test_labels/failures/wrong_product_type.png')
    print("✓ Created: wrong_product_type.png")
    print("   Form values: Brand='Mountain Spirits', Type='Bourbon Whiskey', ABV=45%, Net=750")
    print("   Expected: FAIL - Product type mismatch (Rye Whiskey vs Bourbon Whiskey)")


def create_missing_government_warning():
    """Label WITHOUT government warning"""
    img = Image.new('RGB', (800, 1200), color='white')
    draw = ImageDraw.Draw(img)
    title_font, large_font, medium_font, warning_font = get_fonts()
    
    draw.rectangle([(10, 10), (790, 1190)], outline='black', width=5)
    draw.text((400, 80), 'ILLEGAL BREWERY', fill='black', font=title_font, anchor='mm')
    draw.line([(50, 140), (750, 140)], fill='black', width=2)
    draw.text((400, 220), 'CRAFT', fill='black', font=medium_font, anchor='mm')
    draw.text((400, 280), 'PALE ALE', fill='black', font=large_font, anchor='mm')
    draw.text((400, 460), '6.0% Alc./Vol.', fill='black', font=large_font, anchor='mm')
    draw.text((400, 540), '355 mL', fill='black', font=large_font, anchor='mm')
    
    # NO GOVERNMENT WARNING!
    draw.text((400, 750), 'Enjoy Responsibly', fill='gray', font=warning_font, anchor='mm')
    
    img.save('test_labels/failures/missing_warning.png')
    print("✓ Created: missing_warning.png")
    print("   Form values: Brand='Illegal Brewery', Type='Pale Ale', ABV=6%, Net=355")
    print("   Expected: WARNING - Government warning not detected")


def create_multiple_errors():
    """Label with MULTIPLE errors"""
    img = Image.new('RGB', (800, 1200), color='white')
    draw = ImageDraw.Draw(img)
    title_font, large_font, medium_font, warning_font = get_fonts()
    
    draw.rectangle([(10, 10), (790, 1190)], outline='black', width=5)
    
    # Wrong brand (should be "Eagle Peak")
    draw.text((400, 80), 'FAKE DISTILLERY', fill='black', font=title_font, anchor='mm')
    draw.line([(50, 140), (750, 140)], fill='black', width=2)
    draw.text((400, 220), 'KENTUCKY STRAIGHT', fill='black', font=medium_font, anchor='mm')
    
    # Wrong type (should be "Bourbon Whiskey")
    draw.text((400, 280), 'VODKA', fill='black', font=large_font, anchor='mm')
    
    # Wrong alcohol (should be 45%)
    draw.text((400, 460), '35% Alc./Vol.', fill='black', font=large_font, anchor='mm')
    
    # Wrong volume (should be 750)
    draw.text((400, 540), '1000 mL', fill='black', font=large_font, anchor='mm')
    
    # No warning
    
    img.save('test_labels/failures/multiple_errors.png')
    print("✓ Created: multiple_errors.png")
    print("   Form values: Brand='Eagle Peak', Type='Bourbon Whiskey', ABV=45%, Net=750")
    print("   Expected: FAIL - ALL fields mismatch")


if __name__ == "__main__":
    print("Creating failure test images...\n")
    create_wrong_alcohol_content()
    print()
    create_wrong_volume()
    print()
    create_wrong_brand()
    print()
    create_wrong_product_type()
    print()
    create_missing_government_warning()
    print()
    create_multiple_errors()
    print("\n✅ Done! All failure test images created in test_labels/failures/")
    print("\nThese images are designed to FAIL verification to test error detection.")
