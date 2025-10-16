#!/usr/bin/env python3
"""
Tests for the Period class
"""
import unittest
import sys
import os
from datetime import date

# Add parent directory to path to import the main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BPDatesValidator import Period, dateX


class TestPeriod(unittest.TestCase):
    """Test cases for the Period class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.start_date = dateX(2023, 1, 1)
        self.end_date = dateX(2023, 12, 31)
        self.period = Period(self.start_date, self.end_date)
        
        # Additional test periods
        self.short_period = Period(dateX(2023, 6, 1), dateX(2023, 6, 30))
        self.single_day_period = Period(dateX(2023, 6, 15), dateX(2023, 6, 15))
        self.cross_year_period = Period(dateX(2022, 12, 1), dateX(2023, 1, 31))
    
    def test_period_initialization(self):
        """Test Period initialization"""
        self.assertEqual(self.period.dateFrom, self.start_date)
        self.assertEqual(self.period.dateTo, self.end_date)
        self.assertIsInstance(self.period.dateFrom, dateX)
        self.assertIsInstance(self.period.dateTo, dateX)
    
    def test_get_date_from_method(self):
        """Test getDateFrom method"""
        self.assertEqual(self.period.getDateFrom(), self.start_date)
        self.assertIsInstance(self.period.getDateFrom(), dateX)
    
    def test_period_duration(self):
        """Test period duration calculations"""
        # Full year period
        duration = (self.end_date - self.start_date).days
        self.assertEqual(duration, 364)  # 2023 is not a leap year
        
        # Short period (June)
        duration_short = (self.short_period.dateTo - self.short_period.dateFrom).days
        self.assertEqual(duration_short, 29)  # June has 30 days, so 30-1=29
        
        # Single day period
        duration_single = (self.single_day_period.dateTo - self.single_day_period.dateFrom).days
        self.assertEqual(duration_single, 0)
        
        # Cross year period
        duration_cross = (self.cross_year_period.dateTo - self.cross_year_period.dateFrom).days
        self.assertEqual(duration_cross, 61)  # Dec 1 to Jan 31
    
    def test_period_with_different_dates(self):
        """Test periods with various date combinations"""
        # Test with leap year
        leap_start = dateX(2024, 1, 1)
        leap_end = dateX(2024, 12, 31)
        leap_period = Period(leap_start, leap_end)
        leap_duration = (leap_end - leap_start).days
        self.assertEqual(leap_duration, 365)  # 2024 is a leap year
        
        # Test with February
        feb_start = dateX(2023, 2, 1)
        feb_end = dateX(2023, 2, 28)
        feb_period = Period(feb_start, feb_end)
        feb_duration = (feb_end - feb_start).days
        self.assertEqual(feb_duration, 27)  # 28-1=27
        
        # Test with February in leap year
        feb_leap_start = dateX(2024, 2, 1)
        feb_leap_end = dateX(2024, 2, 29)
        feb_leap_period = Period(feb_leap_start, feb_leap_end)
        feb_leap_duration = (feb_leap_end - feb_leap_start).days
        self.assertEqual(feb_leap_duration, 28)  # 29-1=28
    
    def test_period_edge_cases(self):
        """Test period edge cases"""
        # Same start and end date
        same_date = dateX(2023, 6, 15)
        same_period = Period(same_date, same_date)
        self.assertEqual(same_period.dateFrom, same_date)
        self.assertEqual(same_period.dateTo, same_date)
        self.assertEqual((same_period.dateTo - same_period.dateFrom).days, 0)
        
        # Very short period (2 days)
        short_start = dateX(2023, 6, 15)
        short_end = dateX(2023, 6, 16)
        short_period = Period(short_start, short_end)
        self.assertEqual((short_period.dateTo - short_period.dateFrom).days, 1)
    
    def test_period_attributes_access(self):
        """Test direct attribute access"""
        period = Period(dateX(2023, 3, 1), dateX(2023, 3, 31))
        
        # Test direct attribute access
        self.assertEqual(period.dateFrom.year, 2023)
        self.assertEqual(period.dateFrom.month, 3)
        self.assertEqual(period.dateFrom.day, 1)
        
        self.assertEqual(period.dateTo.year, 2023)
        self.assertEqual(period.dateTo.month, 3)
        self.assertEqual(period.dateTo.day, 31)
        
        # Test getDateFrom method
        start_date = period.getDateFrom()
        self.assertEqual(start_date.year, 2023)
        self.assertEqual(start_date.month, 3)
        self.assertEqual(start_date.day, 1)
    
    def test_period_with_datex_methods(self):
        """Test period with dateX methods"""
        start = dateX(2023, 6, 15)
        end = start.shiftDay(30)  # 30 days later
        
        period = Period(start, end)
        self.assertEqual(period.dateFrom, start)
        self.assertEqual(period.dateTo, end)
        
        # Test with shifted dates
        shifted_start = start.shiftMonth(1)
        shifted_end = end.shiftMonth(1)
        shifted_period = Period(shifted_start, shifted_end)
        
        self.assertEqual(shifted_period.dateFrom.month, 7)
        self.assertEqual(shifted_period.dateTo.month, 8)  # end was 30 days later, so it becomes August


if __name__ == '__main__':
    unittest.main()
