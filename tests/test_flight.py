#!/usr/bin/env python3
"""
Tests for the Flight class
"""
import unittest
import sys
import os
from datetime import date

# Add parent directory to path to import the main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BPDatesValidator import Flight, dateX


class TestFlight(unittest.TestCase):
    """Test cases for the Flight class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_date = dateX(2023, 6, 15)
        self.flight_uk_to_uk = Flight(
            date=self.test_date,
            origin="LHR",
            originUK=True,
            destin="EDI",
            destinUK=True
        )
        self.flight_uk_to_foreign = Flight(
            date=self.test_date,
            origin="LHR",
            originUK=True,
            destin="CDG",
            destinUK=False
        )
        self.flight_foreign_to_uk = Flight(
            date=self.test_date,
            origin="CDG",
            originUK=False,
            destin="LHR",
            destinUK=True
        )
        self.flight_foreign_to_foreign = Flight(
            date=self.test_date,
            origin="CDG",
            originUK=False,
            destin="FCO",
            destinUK=False
        )
    
    def test_flight_initialization(self):
        """Test Flight initialization"""
        self.assertEqual(self.flight_uk_to_uk.date, self.test_date)
        self.assertEqual(self.flight_uk_to_uk.origin, "LHR")
        self.assertTrue(self.flight_uk_to_uk.originUK)
        self.assertEqual(self.flight_uk_to_uk.destin, "EDI")
        self.assertTrue(self.flight_uk_to_uk.destinUK)
    
    def test_get_date_method(self):
        """Test getDate method"""
        self.assertEqual(self.flight_uk_to_uk.getDate(), self.test_date)
        self.assertIsInstance(self.flight_uk_to_uk.getDate(), dateX)
    
    def test_flight_types(self):
        """Test different types of flights"""
        # UK to UK flight
        self.assertTrue(self.flight_uk_to_uk.originUK)
        self.assertTrue(self.flight_uk_to_uk.destinUK)
        
        # UK to foreign flight
        self.assertTrue(self.flight_uk_to_foreign.originUK)
        self.assertFalse(self.flight_uk_to_foreign.destinUK)
        
        # Foreign to UK flight
        self.assertFalse(self.flight_foreign_to_uk.originUK)
        self.assertTrue(self.flight_foreign_to_uk.destinUK)
        
        # Foreign to foreign flight
        self.assertFalse(self.flight_foreign_to_foreign.originUK)
        self.assertFalse(self.flight_foreign_to_foreign.destinUK)
    
    def test_flight_attributes(self):
        """Test flight attribute access"""
        flight = Flight(
            date=dateX(2023, 12, 25),
            origin="JFK",
            originUK=False,
            destin="LHR",
            destinUK=True
        )
        
        self.assertEqual(flight.date.year, 2023)
        self.assertEqual(flight.date.month, 12)
        self.assertEqual(flight.date.day, 25)
        self.assertEqual(flight.origin, "JFK")
        self.assertEqual(flight.destin, "LHR")
        self.assertFalse(flight.originUK)
        self.assertTrue(flight.destinUK)
    
    def test_flight_with_different_dates(self):
        """Test flights with different dates"""
        date1 = dateX(2023, 1, 1)
        date2 = dateX(2023, 6, 15)
        date3 = dateX(2023, 12, 31)
        
        flight1 = Flight(date1, "LHR", True, "CDG", False)
        flight2 = Flight(date2, "CDG", False, "LHR", True)
        flight3 = Flight(date3, "EDI", True, "GLA", True)
        
        self.assertEqual(flight1.getDate(), date1)
        self.assertEqual(flight2.getDate(), date2)
        self.assertEqual(flight3.getDate(), date3)
    
    def test_flight_airport_codes(self):
        """Test flights with various airport codes"""
        airports = ["LHR", "LGW", "STN", "LTN", "EDI", "GLA", "MAN", "BHX"]
        
        for airport in airports:
            flight = Flight(
                date=self.test_date,
                origin=airport,
                originUK=True,
                destin="CDG",
                destinUK=False
            )
            self.assertEqual(flight.origin, airport)
            self.assertTrue(flight.originUK)
            self.assertEqual(flight.destin, "CDG")
            self.assertFalse(flight.destinUK)
    
    def test_flight_boolean_values(self):
        """Test flights with different boolean combinations"""
        # Test with explicit True/False
        flight1 = Flight(self.test_date, "LHR", True, "CDG", False)
        self.assertTrue(flight1.originUK)
        self.assertFalse(flight1.destinUK)
        
        # Test with 1/0 (as might come from CSV)
        flight2 = Flight(self.test_date, "CDG", False, "LHR", True)
        self.assertFalse(flight2.originUK)
        self.assertTrue(flight2.destinUK)


if __name__ == '__main__':
    unittest.main()
