"""
Unit tests for OCR and verification logic
Tests the core functionality without requiring actual image processing
"""
import pytest
from app.verification import (
    fuzzy_match,
    extract_percentage,
    extract_volume,
    normalize_text,
    extract_brand_name,
    extract_product_type,
    verify_label_data
)


class TestFuzzyMatching:
    """Test fuzzy string matching for OCR error tolerance"""
    
    def test_exact_match(self):
        """Test exact string matching"""
        matched, found = fuzzy_match("Eagle Peak Bourbon", "Eagle Peak", threshold=0.75)
        assert matched is True
        assert found is not None
        
    def test_case_insensitive(self):
        """Test case-insensitive matching"""
        matched, found = fuzzy_match("EAGLE PEAK BOURBON", "eagle peak", threshold=0.75)
        assert matched is True
        
    def test_ocr_error_tolerance_l_to_i(self):
        """Test tolerance for l→i OCR error (Eagie vs Eagle)"""
        matched, found = fuzzy_match("Eagie Peak Bourbon", "Eagle Peak", threshold=0.75)
        assert matched is True
        
    def test_ocr_error_tolerance_o_to_0(self):
        """Test tolerance for O→0 OCR error (B0URB0N vs BOURBON)"""
        matched, found = fuzzy_match("B0URB0N WHISKEY", "BOURBON WHISKEY", threshold=0.75)
        assert matched is True
        
    def test_extra_whitespace(self):
        """Test handling of extra whitespace"""
        matched, found = fuzzy_match("Eagle  Peak   Bourbon", "Eagle Peak", threshold=0.75)
        assert matched is True
        
    def test_no_match(self):
        """Test that completely different strings don't match"""
        matched, found = fuzzy_match("Vodka Brand", "Bourbon Brand", threshold=0.75)
        assert matched is False
        assert found is None
        
    def test_partial_match_with_threshold(self):
        """Test that similar but not identical strings match with lower threshold"""
        matched, found = fuzzy_match("Eagle Peaks Bourbon", "Eagle Peak", threshold=0.75)
        assert matched is True


class TestTextNormalization:
    """Test text normalization functions"""
    
    def test_lowercase_conversion(self):
        """Test that text is converted to lowercase"""
        result = normalize_text("EAGLE PEAK BOURBON")
        assert result == "eagle peak bourbon"
        
    def test_whitespace_collapsing(self):
        """Test that multiple spaces are collapsed to single space"""
        result = normalize_text("Eagle   Peak    Bourbon")
        assert result == "eagle peak bourbon"
        
    def test_trim_spaces(self):
        """Test that leading/trailing spaces are removed"""
        result = normalize_text("  Eagle Peak  ")
        assert result == "eagle peak"


class TestPercentageExtraction:
    """Test alcohol percentage extraction from text"""
    
    def test_basic_percentage(self):
        """Test extraction of simple percentage"""
        result = extract_percentage("45%")
        assert result == 45.0
        
    def test_percentage_with_space(self):
        """Test extraction with space before %"""
        result = extract_percentage("45 %")
        assert result == 45.0
        
    def test_percentage_with_abv(self):
        """Test extraction from ABV notation"""
        result = extract_percentage("45% ABV")
        assert result == 45.0
        
    def test_percentage_alc_vol(self):
        """Test extraction from Alc./Vol. notation"""
        result = extract_percentage("45% Alc./Vol.")
        assert result == 45.0
        
    def test_decimal_percentage(self):
        """Test extraction of decimal percentage"""
        result = extract_percentage("45.5%")
        assert result == 45.5
        
    def test_alc_notation(self):
        """Test extraction from 'alc. 45' notation"""
        result = extract_percentage("alc. 45")
        assert result == 45.0
        
    def test_no_percentage_found(self):
        """Test that None is returned when no percentage found"""
        result = extract_percentage("Just text without numbers")
        assert result is None


class TestVolumeExtraction:
    """Test volume/net contents extraction from text"""
    
    def test_ml_volume(self):
        """Test extraction of mL volume"""
        result = extract_volume("750 mL")
        assert result == "750"
        
    def test_ml_no_space(self):
        """Test extraction of mL without space"""
        result = extract_volume("750mL")
        assert result == "750"
        
    def test_liter_volume(self):
        """Test extraction of liter volume"""
        result = extract_volume("1 L")
        assert result == "1"
        
    def test_oz_volume(self):
        """Test extraction of oz volume"""
        result = extract_volume("12 oz")
        assert result == "12"
        
    def test_fluid_oz_volume(self):
        """Test extraction of fl oz volume"""
        result = extract_volume("16 fl oz")
        assert result == "16"
        
    def test_decimal_volume(self):
        """Test extraction of decimal volume"""
        result = extract_volume("750.5 mL")
        assert result == "750.5"
        
    def test_no_volume_found(self):
        """Test that None is returned when no volume found"""
        result = extract_volume("Just text without volume")
        assert result is None


class TestBrandExtraction:
    """Test brand name extraction from OCR text"""
    
    def test_extract_first_line(self):
        """Test extraction of brand from first line"""
        text = "EAGLE PEAK\nKENTUCKY BOURBON\nAged 4 Years"
        result = extract_brand_name(text)
        assert result == "EAGLE PEAK"
        
    def test_skip_empty_lines(self):
        """Test that empty lines are skipped"""
        text = "\n\nEAGLE PEAK\nBOURBON"
        result = extract_brand_name(text)
        assert result == "EAGLE PEAK"
        
    def test_empty_text(self):
        """Test handling of empty text"""
        result = extract_brand_name("")
        assert result is None


class TestProductTypeExtraction:
    """Test product type extraction from OCR text"""
    
    def test_extract_bourbon_whiskey(self):
        """Test extraction of bourbon whiskey"""
        text = "EAGLE PEAK\nKENTUCKY STRAIGHT BOURBON WHISKEY\n45%"
        result = extract_product_type(text)
        assert "bourbon" in result.lower()
        
    def test_extract_vodka(self):
        """Test extraction of vodka"""
        text = "BRAND NAME\nPREMIUM VODKA\n40% ABV"
        result = extract_product_type(text)
        assert result.lower() == "vodka"
        
    def test_extract_longest_match(self):
        """Test that longest match is returned (Kentucky Straight Bourbon Whiskey vs Bourbon)"""
        text = "KENTUCKY STRAIGHT BOURBON WHISKEY"
        result = extract_product_type(text)
        # Should match the full phrase if available
        assert len(result) > len("Bourbon")
        
    def test_no_product_type_found(self):
        """Test that None is returned when no product type found"""
        result = extract_product_type("Just random text")
        assert result is None


class TestVerifyLabelData:
    """Integration tests for full label verification"""
    
    def test_perfect_match(self):
        """Test verification with perfect match"""
        ocr_text = """
        EAGLE PEAK
        KENTUCKY STRAIGHT BOURBON WHISKEY
        Aged 4 Years
        45% Alc./Vol. (90 Proof)
        750 mL
        GOVERNMENT WARNING: (1) According to the Surgeon General, women should not drink alcoholic beverages during pregnancy because of the risk of birth defects. (2) Consumption of alcoholic beverages impairs your ability to drive a car or operate machinery, and may cause health problems.
        """
        
        result = verify_label_data(
            extracted_text=ocr_text,
            brand_name="Eagle Peak",
            product_class="Bourbon Whiskey",
            alcohol_content=45.0,
            net_contents="750"
        )
        
        assert result.overall_match is True
        assert all(check.matched for check in result.checks)
        
    def test_brand_mismatch(self):
        """Test verification with brand name mismatch"""
        ocr_text = """
        EAGLE PEAK
        BOURBON WHISKEY
        45% ABV
        750 mL
        """
        
        result = verify_label_data(
            extracted_text=ocr_text,
            brand_name="Mountain Ridge",  # Wrong brand
            product_class="Bourbon Whiskey",
            alcohol_content=45.0,
            net_contents="750"
        )
        
        assert result.overall_match is False
        brand_check = next(c for c in result.checks if c.field_name == "Brand Name")
        assert brand_check.matched is False
        assert "eagle peak" in brand_check.found_value.lower()  # Should extract actual brand
        
    def test_alcohol_content_tolerance(self):
        """Test that ±0.5% tolerance is applied for alcohol content"""
        ocr_text = "BRAND\nBOURBON\n45.3% ABV\n750 mL"
        
        result = verify_label_data(
            extracted_text=ocr_text,
            brand_name="Brand",
            product_class="Bourbon",
            alcohol_content=45.0,  # 0.3% difference, within tolerance
            net_contents="750"
        )
        
        abv_check = next(c for c in result.checks if c.field_name == "Alcohol Content")
        assert abv_check.matched is True
        
    def test_alcohol_content_out_of_tolerance(self):
        """Test that differences > 0.5% fail"""
        ocr_text = "BRAND\nBOURBON\n45% ABV\n750 mL"
        
        result = verify_label_data(
            extracted_text=ocr_text,
            brand_name="Brand",
            product_class="Bourbon",
            alcohol_content=40.0,  # 5% difference, out of tolerance
            net_contents="750"
        )
        
        abv_check = next(c for c in result.checks if c.field_name == "Alcohol Content")
        assert abv_check.matched is False
        
    def test_net_contents_exact_match(self):
        """Test that net contents requires exact number match"""
        ocr_text = "BRAND\nBOURBON\n45% ABV\n750 mL"
        
        result = verify_label_data(
            extracted_text=ocr_text,
            brand_name="Brand",
            product_class="Bourbon",
            alcohol_content=45.0,
            net_contents="750"
        )
        
        net_check = next(c for c in result.checks if c.field_name == "Net Contents")
        assert net_check.matched is True
        
    def test_net_contents_prevents_substring_match(self):
        """Test that 750 doesn't match 1750"""
        ocr_text = "BRAND\nBOURBON\n45% ABV\n1750 mL"
        
        result = verify_label_data(
            extracted_text=ocr_text,
            brand_name="Brand",
            product_class="Bourbon",
            alcohol_content=45.0,
            net_contents="750"  # Should not match 1750
        )
        
        net_check = next(c for c in result.checks if c.field_name == "Net Contents")
        assert net_check.matched is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
