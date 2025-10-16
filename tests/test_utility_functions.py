#!/usr/bin/env python3
"""
Tests for utility functions (colOrCol, grnOrRed)
"""
import unittest
import sys
import os

# Add parent directory to path to import the main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BPDatesValidator import colOrCol, grnOrRed
from term_style import ctyle


class TestUtilityFunctions(unittest.TestCase):
    """Test cases for utility functions"""
    
    def test_col_or_col_true_condition(self):
        """Test colOrCol function with True condition"""
        result = colOrCol(ctyle.GRN, ctyle.RED, True, "test text")
        expected = f'{ctyle.GRN}test text{ctyle.END}'
        self.assertEqual(result, expected)
    
    def test_col_or_col_false_condition(self):
        """Test colOrCol function with False condition"""
        result = colOrCol(ctyle.GRN, ctyle.RED, False, "test text")
        expected = f'{ctyle.RED}test text{ctyle.END}'
        self.assertEqual(result, expected)
    
    def test_col_or_col_with_different_colors(self):
        """Test colOrCol function with different color combinations"""
        # Test with blue and yellow
        result = colOrCol(ctyle.BLU, ctyle.YEL, True, "blue text")
        expected = f'{ctyle.BLU}blue text{ctyle.END}'
        self.assertEqual(result, expected)
        
        result = colOrCol(ctyle.BLU, ctyle.YEL, False, "yellow text")
        expected = f'{ctyle.YEL}yellow text{ctyle.END}'
        self.assertEqual(result, expected)
    
    def test_col_or_col_with_empty_text(self):
        """Test colOrCol function with empty text"""
        result = colOrCol(ctyle.GRN, ctyle.RED, True, "")
        expected = f'{ctyle.GRN}{ctyle.END}'
        self.assertEqual(result, expected)
        
        result = colOrCol(ctyle.GRN, ctyle.RED, False, "")
        expected = f'{ctyle.RED}{ctyle.END}'
        self.assertEqual(result, expected)
    
    def test_col_or_col_with_special_characters(self):
        """Test colOrCol function with special characters"""
        special_text = "test@#$%^&*()_+{}|:<>?[]\\;'\",./"
        result = colOrCol(ctyle.GRN, ctyle.RED, True, special_text)
        expected = f'{ctyle.GRN}{special_text}{ctyle.END}'
        self.assertEqual(result, expected)
    
    def test_grn_or_red_true_condition(self):
        """Test grnOrRed function with True condition"""
        result = grnOrRed(True, "success text")
        expected = f'{ctyle.GRN}success text{ctyle.END}'
        self.assertEqual(result, expected)
    
    def test_grn_or_red_false_condition(self):
        """Test grnOrRed function with False condition"""
        result = grnOrRed(False, "error text")
        expected = f'{ctyle.RED}error text{ctyle.END}'
        self.assertEqual(result, expected)
    
    def test_grn_or_red_with_boolean_values(self):
        """Test grnOrRed function with various boolean values"""
        # Test with True
        result = grnOrRed(True, "text")
        expected = f'{ctyle.GRN}text{ctyle.END}'
        self.assertEqual(result, expected)
        
        # Test with False
        result = grnOrRed(False, "text")
        expected = f'{ctyle.RED}text{ctyle.END}'
        self.assertEqual(result, expected)
        
        # Test with truthy values
        result = grnOrRed(1, "text")
        expected = f'{ctyle.GRN}text{ctyle.END}'
        self.assertEqual(result, expected)
        
        result = grnOrRed("non-empty", "text")
        expected = f'{ctyle.GRN}text{ctyle.END}'
        self.assertEqual(result, expected)
        
        # Test with falsy values
        result = grnOrRed(0, "text")
        expected = f'{ctyle.RED}text{ctyle.END}'
        self.assertEqual(result, expected)
        
        result = grnOrRed("", "text")
        expected = f'{ctyle.RED}text{ctyle.END}'
        self.assertEqual(result, expected)
        
        result = grnOrRed(None, "text")
        expected = f'{ctyle.RED}text{ctyle.END}'
        self.assertEqual(result, expected)
    
    def test_grn_or_red_with_different_texts(self):
        """Test grnOrRed function with different text inputs"""
        texts = [
            "UK",
            "NON-UK",
            "LHR",
            "CDG",
            "123",
            "Flight FR1234",
            "True",
            "False"
        ]
        
        for text in texts:
            # Test with True condition
            result_true = grnOrRed(True, text)
            expected_true = f'{ctyle.GRN}{text}{ctyle.END}'
            self.assertEqual(result_true, expected_true)
            
            # Test with False condition
            result_false = grnOrRed(False, text)
            expected_false = f'{ctyle.RED}{text}{ctyle.END}'
            self.assertEqual(result_false, expected_false)
    
    def test_function_consistency(self):
        """Test that functions are consistent with their expected behavior"""
        # Test that grnOrRed is equivalent to colOrCol with green and red
        text = "test consistency"
        
        result_grn_or_red = grnOrRed(True, text)
        result_col_or_col = colOrCol(ctyle.GRN, ctyle.RED, True, text)
        self.assertEqual(result_grn_or_red, result_col_or_col)
        
        result_grn_or_red = grnOrRed(False, text)
        result_col_or_col = colOrCol(ctyle.GRN, ctyle.RED, False, text)
        self.assertEqual(result_grn_or_red, result_col_or_col)
    
    def test_color_codes_presence(self):
        """Test that color codes are properly included in output"""
        result = grnOrRed(True, "test")
        
        # Check that green color code is present
        self.assertIn(ctyle.GRN, result)
        
        # Check that end code is present
        self.assertIn(ctyle.END, result)
        
        # Check that red color code is not present
        self.assertNotIn(ctyle.RED, result)
        
        result = grnOrRed(False, "test")
        
        # Check that red color code is present
        self.assertIn(ctyle.RED, result)
        
        # Check that end code is present
        self.assertIn(ctyle.END, result)
        
        # Check that green color code is not present
        self.assertNotIn(ctyle.GRN, result)
    
    def test_unicode_and_multibyte_text(self):
        """Test functions with unicode and multibyte text"""
        unicode_texts = [
            "café",
            "naïve",
            "résumé",
            "测试",
            "тест",
            "🚀✈️",
            "αβγδε"
        ]
        
        for text in unicode_texts:
            result = grnOrRed(True, text)
            expected = f'{ctyle.GRN}{text}{ctyle.END}'
            self.assertEqual(result, expected)
            
            result = grnOrRed(False, text)
            expected = f'{ctyle.RED}{text}{ctyle.END}'
            self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
