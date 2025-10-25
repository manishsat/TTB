"""
Create realistic-looking label images with proper text rendering
These should work better with OCR while still testing quality scenarios
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap

def get_fonts():
    """Try to load system fonts, fallback to default"""
    try:
        title_font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 60)
        large_font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 45)
        medium_font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 35)
        small_font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 25)
        warning_font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 16)
        return title_font, large_font, medium_font, small_font, warning_font
    except:
        default = ImageFont.load_default()
        return default, default, default, default, default


def add_government_warning(draw, y_position, width, warning_font):
    """Add government warning text"""
    warning_text = "GOVERNMENT WARNING: According to the Surgeon General, women should not drink alcoholic beverages during pregnancy because of the risk of birth defects. Consumption of alcoholic beverages impairs your ability to drive a car or operate machinery, and may cause health problems."
    
    # Wrap text
    max_width = width - 100
    lines = textwrap.wrap(warning_text, width=60)
    
    for i, line in enumerate(lines):
        draw.text((width//2, y_position + i*20), line, fill='black', font=warning_font, anchor='mm')


def create_clear_bourbon_label():
    """Create a clear, high-quality bourbon label"""
    img = Image.new('RGB', (800, 1200), color='#FFFFFF')  # White background
    draw = ImageDraw.Draw(img)
    title_font, large_font, medium_font, small_font, warning_font = get_fonts()
    
    # Border
    draw.rectangle([(10, 10), (790, 1190)], outline='#000000', width=5)
    
    # Brand name - PURE BLACK on white for maximum OCR accuracy
    draw.text((400, 90), "EAGLE PEAK", fill='#000000', font=title_font, anchor='mm')
    
    # Decorative line
    draw.line([(50, 150), (750, 150)], fill='#000000', width=3)
    
    # Product type - PURE BLACK
    draw.text((400, 250), "KENTUCKY STRAIGHT", fill='#000000', font=medium_font, anchor='mm')
    draw.text((400, 300), "BOURBON WHISKEY", fill='#000000', font=large_font, anchor='mm')
    
    # Details
    draw.text((400, 400), "Aged 4 Years", fill='#000000', font=small_font, anchor='mm')
    draw.text((400, 500), "45% Alc./Vol. (90 Proof)", fill='#000000', font=medium_font, anchor='mm')
    draw.text((400, 580), "750 mL", fill='#000000', font=large_font, anchor='mm')
    
    # Government warning
    add_government_warning(draw, 700, 800, warning_font)
    
    img.save('test_labels/clear_bourbon.png')
    print("✓ Created: clear_bourbon.png (800x1200, pure black text - maximum OCR accuracy)")


def create_slightly_blurry_label():
    """Create a realistic slightly blurry photo (like quick phone snap)"""
    img = Image.new('RGB', (800, 1200), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    title_font, large_font, medium_font, small_font, warning_font = get_fonts()
    
    # Border
    draw.rectangle([(10, 10), (790, 1190)], outline='#654321', width=5)
    
    # Brand name - dark text on white
    draw.text((400, 90), "MOUNTAIN VIEW", fill='#654321', font=title_font, anchor='mm')
    
    # Decorative line
    draw.line([(50, 150), (750, 150)], fill='#654321', width=3)
    
    # Product
    draw.text((400, 250), "CRAFT", fill='#654321', font=medium_font, anchor='mm')
    draw.text((400, 300), "PALE ALE", fill='#654321', font=large_font, anchor='mm')
    
    # Details
    draw.text((400, 450), "5.5% Alc./Vol.", fill='black', font=medium_font, anchor='mm')
    draw.text((400, 530), "355 mL", fill='black', font=large_font, anchor='mm')
    
    # Government warning
    add_government_warning(draw, 700, 800, warning_font)
    
    # Apply moderate blur (realistic quick photo)
    img = img.filter(ImageFilter.GaussianBlur(radius=2))
    img.save('test_labels/slightly_blurry_beer.png')
    print("✓ Created: slightly_blurry_beer.png (800x1200, moderate blur - OCR should handle)")


def create_low_contrast_label():
    """Create a label with challenging but readable contrast"""
    img = Image.new('RGB', (800, 1200), color='#D4A574')  # Tan background
    draw = ImageDraw.Draw(img)
    title_font, large_font, medium_font, small_font, warning_font = get_fonts()
    
    # Header with low contrast
    draw.rectangle([(0, 0), (800, 180)], fill='#A0826D')
    draw.text((400, 90), "SUNSET RIDGE", fill='#8B7355', font=title_font, anchor='mm')  # Low contrast!
    
    # Product
    draw.text((400, 250), "PREMIUM", fill='#8B7355', font=medium_font, anchor='mm')
    draw.text((400, 300), "VODKA", fill='#8B7355', font=large_font, anchor='mm')
    
    # Details
    draw.text((400, 450), "40% Alc./Vol. (80 Proof)", fill='#6B5345', font=medium_font, anchor='mm')
    draw.text((400, 530), "750 mL", fill='#6B5345', font=large_font, anchor='mm')
    
    # Government warning
    add_government_warning(draw, 700, 800, warning_font)
    
    img.save('test_labels/low_contrast_vodka.png')
    print("✓ Created: low_contrast_vodka.png (800x1200, low contrast - OCR will struggle)")


def create_tiny_resolution_label():
    """Create a label with actual content but resolution too small"""
    img = Image.new('RGB', (300, 400), color='#F0E68C')  # Fails minimum!
    draw = ImageDraw.Draw(img)
    
    try:
        tiny_title = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 20)
        tiny_text = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 14)
    except:
        tiny_title = ImageFont.load_default()
        tiny_text = ImageFont.load_default()
    
    # Header
    draw.rectangle([(0, 0), (300, 60)], fill='#8B4513')
    draw.text((150, 30), "MINI DISTILLERY", fill='white', font=tiny_title, anchor='mm')
    
    # Details
    draw.text((150, 100), "Bourbon Whiskey", fill='black', font=tiny_text, anchor='mm')
    draw.text((150, 140), "45% Alc./Vol.", fill='black', font=tiny_text, anchor='mm')
    draw.text((150, 180), "750 mL", fill='black', font=tiny_text, anchor='mm')
    
    img.save('test_labels/tiny_bourbon.png')
    print("✓ Created: tiny_bourbon.png (300x400 - FAILS minimum resolution)")


def create_heavily_compressed_label():
    """Create a label then compress it heavily"""
    img = Image.new('RGB', (800, 1200), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    title_font, large_font, medium_font, small_font, warning_font = get_fonts()
    
    # Border
    draw.rectangle([(10, 10), (790, 1190)], outline='#B8860B', width=5)
    
    # Brand name
    draw.text((400, 90), "GOLDEN HOPS", fill='#B8860B', font=title_font, anchor='mm')
    
    # Decorative line
    draw.line([(50, 150), (750, 150)], fill='#B8860B', width=3)
    
    # Product
    draw.text((400, 250), "INDIA PALE ALE", fill='#B8860B', font=large_font, anchor='mm')
    
    # Details
    draw.text((400, 400), "6.5% Alc./Vol.", fill='black', font=medium_font, anchor='mm')
    draw.text((400, 480), "355 mL", fill='black', font=large_font, anchor='mm')
    
    # Government warning
    add_government_warning(draw, 650, 800, warning_font)
    
    # Save with very low quality
    img.save('test_labels/compressed_ipa.jpg', quality=15)
    print("✓ Created: compressed_ipa.jpg (800x1200, quality=15 - heavy JPEG artifacts)")


if __name__ == "__main__":
    print("Creating realistic test labels with better OCR compatibility...\n")
    create_clear_bourbon_label()
    create_slightly_blurry_label()
    create_low_contrast_label()
    create_tiny_resolution_label()
    create_heavily_compressed_label()
    print("\n✅ Done! These labels should work better with OCR.")
    print("\nTest in this order:")
    print("  1. clear_bourbon.png - Should work perfectly")
    print("  2. tiny_bourbon.png - Should FAIL validation (too small)")
    print("  3. slightly_blurry_beer.png - Should work with minor issues")
    print("  4. low_contrast_vodka.png - OCR will struggle but may extract some text")
    print("  5. compressed_ipa.jpg - OCR may struggle with compression artifacts")
