#!/usr/bin/env python3
"""
Tests for the datetimeX class - extended datetime functionality
"""
import unittest
import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path to import the main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BPDatesValidator import datetimeX


class TestDateTimeX(unittest.TestCase):
    """Test cases for the datetimeX class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_datetime = datetimeX(2023, 6, 15, 14, 30)  # 15/06/2023 14:30
        self.test_datetime_midnight = datetimeX(2023, 12, 31, 0, 0)  # 31/12/2023 00:00
        self.test_datetime_end_day = datetimeX(2023, 6, 15, 23, 59)  # 15/06/2023 23:59
    
    def test_str_representation(self):
        """Test string representation of datetimeX"""
        self.assertEqual(str(self.test_datetime), "15/06/2023 14:30")
        self.assertEqual(str(self.test_datetime_midnight), "31/12/2023 00:00")
        self.assertEqual(str(self.test_datetime_end_day), "15/06/2023 23:59")
    
    def test_inheritance(self):
        """Test that datetimeX properly inherits from datetime"""
        # Test that it's an instance of datetime
        self.assertIsInstance(self.test_datetime, datetime)
        
        # Test that datetime methods still work
        self.assertEqual(self.test_datetime.weekday(), 3)  # Thursday
        self.assertEqual(self.test_datetime.isoweekday(), 4)  # Thursday (ISO)
        self.assertEqual(self.test_datetime.hour, 14)
        self.assertEqual(self.test_datetime.minute, 30)
        
        # Test arithmetic operations
        result = self.test_datetime + timedelta(hours=1)
        self.assertEqual(result.hour, 15)
        self.assertIsInstance(result, datetimeX)
    
    def test_date_property(self):
        """Test that date property returns dateX instance"""
        date_part = self.test_datetime.date()
        self.assertIsInstance(date_part, type(self.test_datetime).__bases__[0].__bases__[0])  # Should be dateX
        self.assertEqual(date_part.day, 15)
        self.assertEqual(date_part.month, 6)
        self.assertEqual(date_part.year, 2023)
    
    def test_time_property(self):
        """Test that time property works correctly"""
        time_part = self.test_datetime.time()
        self.assertEqual(time_part.hour, 14)
        self.assertEqual(time_part.minute, 30)
        self.assertEqual(time_part.second, 0)
    
    def test_replace_method(self):
        """Test replace method"""
        # Test replacing year
        replaced = self.test_datetime.replace(year=2024)
        self.assertEqual(replaced.year, 2024)
        self.assertEqual(replaced.month, 6)
        self.assertEqual(replaced.day, 15)
        self.assertEqual(replaced.hour, 14)
        self.assertEqual(replaced.minute, 30)
        self.assertIsInstance(replaced, datetimeX)
        
        # Test replacing multiple fields
        replaced = self.test_datetime.replace(year=2024, month=12, day=25, hour=10, minute=45)
        self.assertEqual(replaced.year, 2024)
        self.assertEqual(replaced.month, 12)
        self.assertEqual(replaced.day, 25)
        self.assertEqual(replaced.hour, 10)
        self.assertEqual(replaced.minute, 45)
    
    def test_strptime_method(self):
        """Test strptime class method"""
        # Test parsing with time
        parsed = datetimeX.strptime("15/06/2023 14:30", "%d/%m/%Y %H:%M")
        self.assertEqual(parsed.year, 2023)
        self.assertEqual(parsed.month, 6)
        self.assertEqual(parsed.day, 15)
        self.assertEqual(parsed.hour, 14)
        self.assertEqual(parsed.minute, 30)
        self.assertIsInstance(parsed, datetimeX)
        
        # Test parsing date only
        parsed_date = datetimeX.strptime("15/06/2023", "%d/%m/%Y")
        self.assertEqual(parsed_date.year, 2023)
        self.assertEqual(parsed_date.month, 6)
        self.assertEqual(parsed_date.day, 15)
        self.assertEqual(parsed_date.hour, 0)
        self.assertEqual(parsed_date.minute, 0)
    
    def test_arithmetic_operations(self):
        """Test arithmetic operations with timedelta"""
        # Test addition
        result = self.test_datetime + timedelta(days=1, hours=2, minutes=15)
        self.assertEqual(result.day, 16)
        self.assertEqual(result.hour, 16)
        self.assertEqual(result.minute, 45)
        self.assertIsInstance(result, datetimeX)
        
        # Test subtraction
        result = self.test_datetime - timedelta(days=1, hours=2, minutes=15)
        self.assertEqual(result.day, 14)
        self.assertEqual(result.hour, 12)
        self.assertEqual(result.minute, 15)
        self.assertIsInstance(result, datetimeX)
    
    def test_comparison_operations(self):
        """Test comparison operations"""
        earlier = datetimeX(2023, 6, 15, 10, 0)
        later = datetimeX(2023, 6, 15, 18, 0)
        
        self.assertTrue(earlier < later)
        self.assertTrue(later > earlier)
        self.assertTrue(earlier <= later)
        self.assertTrue(later >= earlier)
        self.assertFalse(earlier == later)
        self.assertTrue(earlier != later)
        
        # Test equality
        same = datetimeX(2023, 6, 15, 14, 30)
        self.assertTrue(self.test_datetime == same)
        self.assertFalse(self.test_datetime != same)


if __name__ == '__main__':
    unittest.main()
