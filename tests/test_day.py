#!/usr/bin/env python3
"""
Tests for the Day class
"""
import unittest
import sys
import os
from datetime import date

# Add parent directory to path to import the main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BPDatesValidator import Day, dateX


class TestDay(unittest.TestCase):
    """Test cases for the Day class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_date = dateX(2023, 6, 15)
        self.day_in_uk = Day(date=self.test_date, abroad=False)
        self.day_abroad = Day(date=self.test_date, abroad=True)
        
        # Additional test days
        self.new_year = Day(dateX(2023, 1, 1), abroad=False)
        self.christmas = Day(dateX(2023, 12, 25), abroad=True)
        self.leap_day = Day(dateX(2024, 2, 29), abroad=False)
    
    def test_day_initialization(self):
        """Test Day initialization"""
        self.assertEqual(self.day_in_uk.date, self.test_date)
        self.assertFalse(self.day_in_uk.abroad)
        
        self.assertEqual(self.day_abroad.date, self.test_date)
        self.assertTrue(self.day_abroad.abroad)
    
    def test_get_date_method(self):
        """Test getDate method"""
        self.assertEqual(self.day_in_uk.getDate(), self.test_date)
        self.assertIsInstance(self.day_in_uk.getDate(), dateX)
        
        self.assertEqual(self.day_abroad.getDate(), self.test_date)
        self.assertIsInstance(self.day_abroad.getDate(), dateX)
    
    def test_day_abroad_status(self):
        """Test different abroad status values"""
        # Test with True
        day_true = Day(self.test_date, abroad=True)
        self.assertTrue(day_true.abroad)
        
        # Test with False
        day_false = Day(self.test_date, abroad=False)
        self.assertFalse(day_false.abroad)
        
        # Test with 1 (as might come from CSV processing)
        day_one = Day(self.test_date, abroad=1)
        self.assertTrue(day_one.abroad)
        
        # Test with 0 (as might come from CSV processing)
        day_zero = Day(self.test_date, abroad=0)
        self.assertFalse(day_zero.abroad)
    
    def test_day_with_different_dates(self):
        """Test days with various dates"""
        dates = [
            dateX(2023, 1, 1),   # New Year
            dateX(2023, 6, 15),  # Mid year
            dateX(2023, 12, 31), # New Year's Eve
            dateX(2024, 2, 29),  # Leap day
        ]
        
        for date_obj in dates:
            day_in_uk = Day(date_obj, abroad=False)
            day_abroad = Day(date_obj, abroad=True)
            
            self.assertEqual(day_in_uk.getDate(), date_obj)
            self.assertFalse(day_in_uk.abroad)
            
            self.assertEqual(day_abroad.getDate(), date_obj)
            self.assertTrue(day_abroad.abroad)
    
    def test_day_attributes_access(self):
        """Test direct attribute access"""
        day = Day(dateX(2023, 6, 15), abroad=True)
        
        # Test direct attribute access
        self.assertEqual(day.date.year, 2023)
        self.assertEqual(day.date.month, 6)
        self.assertEqual(day.date.day, 15)
        self.assertTrue(day.abroad)
        
        # Test getDate method
        date_obj = day.getDate()
        self.assertEqual(date_obj.year, 2023)
        self.assertEqual(date_obj.month, 6)
        self.assertEqual(date_obj.day, 15)
        self.assertIsInstance(date_obj, dateX)
    
    def test_day_with_datex_methods(self):
        """Test day with dateX methods"""
        base_date = dateX(2023, 6, 15)
        
        # Test with shifted dates
        shifted_date = base_date.shiftDay(10)
        day_shifted = Day(shifted_date, abroad=False)
        self.assertEqual(day_shifted.getDate(), shifted_date)
        self.assertEqual(day_shifted.getDate().day, 25)
        
        # Test with month-shifted dates
        month_shifted_date = base_date.shiftMonth(1)
        day_month_shifted = Day(month_shifted_date, abroad=True)
        self.assertEqual(day_month_shifted.getDate(), month_shifted_date)
        self.assertEqual(day_month_shifted.getDate().month, 7)
    
    def test_day_edge_cases(self):
        """Test day edge cases"""
        # Test with first day of year
        first_day = Day(dateX(2023, 1, 1), abroad=False)
        self.assertEqual(first_day.getDate().day, 1)
        self.assertEqual(first_day.getDate().month, 1)
        self.assertFalse(first_day.abroad)
        
        # Test with last day of year
        last_day = Day(dateX(2023, 12, 31), abroad=True)
        self.assertEqual(last_day.getDate().day, 31)
        self.assertEqual(last_day.getDate().month, 12)
        self.assertTrue(last_day.abroad)
        
        # Test with leap day
        leap_day = Day(dateX(2024, 2, 29), abroad=False)
        self.assertEqual(leap_day.getDate().day, 29)
        self.assertEqual(leap_day.getDate().month, 2)
        self.assertEqual(leap_day.getDate().year, 2024)
        self.assertFalse(leap_day.abroad)
    
    def test_day_boolean_combinations(self):
        """Test all boolean combinations"""
        test_date = dateX(2023, 6, 15)
        
        # Test all possible boolean values
        boolean_values = [True, False, 1, 0]
        
        for value in boolean_values:
            day = Day(test_date, abroad=value)
            expected_abroad = bool(value)
            self.assertEqual(day.abroad, expected_abroad)
            self.assertEqual(day.getDate(), test_date)
    
    def test_day_consistency(self):
        """Test day consistency across operations"""
        original_date = dateX(2023, 6, 15)
        day = Day(original_date, abroad=True)
        
        # Test that date remains consistent
        self.assertEqual(day.getDate(), original_date)
        self.assertEqual(day.date, original_date)
        
        # Test that abroad status remains consistent
        self.assertTrue(day.abroad)
        
        # Test that date object is not modified
        self.assertEqual(original_date.year, 2023)
        self.assertEqual(original_date.month, 6)
        self.assertEqual(original_date.day, 15)


if __name__ == '__main__':
    unittest.main()
