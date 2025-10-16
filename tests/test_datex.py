#!/usr/bin/env python3
"""
Tests for the dateX class - extended date functionality
"""
import unittest
import sys
import os
from datetime import date, timedelta

# Add parent directory to path to import the main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BPDatesValidator import dateX


class TestDateX(unittest.TestCase):
    """Test cases for the dateX class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_date = dateX(2023, 6, 15)  # 15/06/2023
        self.test_date_feb = dateX(2023, 2, 15)  # 15/02/2023 (non-leap year)
        self.test_date_leap = dateX(2024, 2, 15)  # 15/02/2024 (leap year)
    
    def test_str_representation(self):
        """Test string representation of dateX"""
        self.assertEqual(str(self.test_date), "15/06/2023")
        self.assertEqual(str(self.test_date_feb), "15/02/2023")
    
    def test_first_day(self):
        """Test firstDay method"""
        first_day = self.test_date.firstDay()
        self.assertEqual(first_day.day, 1)
        self.assertEqual(first_day.month, 6)
        self.assertEqual(first_day.year, 2023)
        self.assertIsInstance(first_day, dateX)
    
    def test_last_day(self):
        """Test lastDay method"""
        # Test June (30 days)
        last_day = self.test_date.lastDay()
        self.assertEqual(last_day.day, 30)
        self.assertEqual(last_day.month, 6)
        self.assertEqual(last_day.year, 2023)
        self.assertIsInstance(last_day, dateX)
        
        # Test February in non-leap year (28 days)
        last_day_feb = self.test_date_feb.lastDay()
        self.assertEqual(last_day_feb.day, 28)
        self.assertEqual(last_day_feb.month, 2)
        self.assertEqual(last_day_feb.year, 2023)
        
        # Test February in leap year (29 days)
        last_day_leap = self.test_date_leap.lastDay()
        self.assertEqual(last_day_leap.day, 29)
        self.assertEqual(last_day_leap.month, 2)
        self.assertEqual(last_day_leap.year, 2024)
    
    def test_shift_day(self):
        """Test shiftDay method"""
        # Test positive shift
        shifted = self.test_date.shiftDay(5)
        self.assertEqual(shifted.day, 20)
        self.assertEqual(shifted.month, 6)
        self.assertEqual(shifted.year, 2023)
        self.assertIsInstance(shifted, dateX)
        
        # Test negative shift
        shifted_neg = self.test_date.shiftDay(-5)
        self.assertEqual(shifted_neg.day, 10)
        self.assertEqual(shifted_neg.month, 6)
        self.assertEqual(shifted_neg.year, 2023)
        
        # Test month boundary crossing
        shifted_boundary = dateX(2023, 6, 30).shiftDay(1)
        self.assertEqual(shifted_boundary.day, 1)
        self.assertEqual(shifted_boundary.month, 7)
        self.assertEqual(shifted_boundary.year, 2023)
    
    def test_shift_month(self):
        """Test shiftMonth method"""
        # Test positive shift within same year
        shifted = self.test_date.shiftMonth(2)
        self.assertEqual(shifted.day, 15)
        self.assertEqual(shifted.month, 8)
        self.assertEqual(shifted.year, 2023)
        self.assertIsInstance(shifted, dateX)
        
        # Test negative shift within same year
        shifted_neg = self.test_date.shiftMonth(-2)
        self.assertEqual(shifted_neg.day, 15)
        self.assertEqual(shifted_neg.month, 4)
        self.assertEqual(shifted_neg.year, 2023)
        
        # Test year boundary crossing
        shifted_year = self.test_date.shiftMonth(8)
        self.assertEqual(shifted_year.day, 15)
        self.assertEqual(shifted_year.month, 2)
        self.assertEqual(shifted_year.year, 2024)
        
        # Test negative year boundary crossing
        shifted_year_neg = self.test_date.shiftMonth(-8)
        self.assertEqual(shifted_year_neg.day, 15)
        self.assertEqual(shifted_year_neg.month, 10)
        self.assertEqual(shifted_year_neg.year, 2022)
    
    def test_shift_year(self):
        """Test shiftYear method"""
        # Test positive shift
        shifted = self.test_date.shiftYear(2)
        self.assertEqual(shifted.day, 15)
        self.assertEqual(shifted.month, 6)
        self.assertEqual(shifted.year, 2025)
        self.assertIsInstance(shifted, dateX)
        
        # Test negative shift
        shifted_neg = self.test_date.shiftYear(-2)
        self.assertEqual(shifted_neg.day, 15)
        self.assertEqual(shifted_neg.month, 6)
        self.assertEqual(shifted_neg.year, 2021)
    
    def test_replace(self):
        """Test replace method"""
        # Test replacing year
        replaced = self.test_date.replace(year=2024)
        self.assertEqual(replaced.day, 15)
        self.assertEqual(replaced.month, 6)
        self.assertEqual(replaced.year, 2024)
        self.assertIsInstance(replaced, dateX)
        
        # Test replacing month
        replaced = self.test_date.replace(month=12)
        self.assertEqual(replaced.day, 15)
        self.assertEqual(replaced.month, 12)
        self.assertEqual(replaced.year, 2023)
        
        # Test replacing day
        replaced = self.test_date.replace(day=1)
        self.assertEqual(replaced.day, 1)
        self.assertEqual(replaced.month, 6)
        self.assertEqual(replaced.year, 2023)
        
        # Test replacing multiple fields
        replaced = self.test_date.replace(year=2024, month=12, day=1)
        self.assertEqual(replaced.day, 1)
        self.assertEqual(replaced.month, 12)
        self.assertEqual(replaced.year, 2024)
        
        # Test replacing no fields (should return copy)
        replaced = self.test_date.replace()
        self.assertEqual(replaced.day, 15)
        self.assertEqual(replaced.month, 6)
        self.assertEqual(replaced.year, 2023)
        self.assertIsInstance(replaced, dateX)
        self.assertIsNot(replaced, self.test_date)  # Should be different object
    
    def test_inheritance(self):
        """Test that dateX properly inherits from date"""
        # Test that it's an instance of date
        self.assertIsInstance(self.test_date, date)
        
        # Test that date methods still work
        self.assertEqual(self.test_date.weekday(), 3)  # Thursday
        self.assertEqual(self.test_date.isoweekday(), 4)  # Thursday (ISO)
        
        # Test arithmetic operations
        result = self.test_date + timedelta(days=1)
        self.assertEqual(result.day, 16)
        self.assertIsInstance(result, dateX)


if __name__ == '__main__':
    unittest.main()
