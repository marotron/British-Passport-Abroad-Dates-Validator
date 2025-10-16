#!/usr/bin/env python3
"""
Tests for CSV parsing logic
"""
import unittest
import sys
import os
import csv
import tempfile
from datetime import datetime
from io import StringIO

# Add parent directory to path to import the main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BPDatesValidator import Flight, dateX


class TestCSVParsing(unittest.TestCase):
    """Test cases for CSV parsing logic"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_csv_data = [
            "17/05/10 10:40,LIS,FALSE,EDI,TRUE,RyanAir,FR1111,FALSE",
            "27/07/10 13:10,EDI,TRUE,GDN,FALSE,RyanAir,FR2222,FALSE",
            "02/05/11 10:50,WMI,FALSE,PIK,TRUE,RyanAir,FR3333,FALSE",
            "30/07/13 12:20,EDI,TRUE,LPA,FALSE,RyanAir,FR4444,FALSE",
            "07/08/13 10:10,LPA,FALSE,GLA,TRUE,WizzAir,FR5555,FALSE"
        ]
        
        self.sample_csv_with_cancelled = [
            "17/05/10 10:40,LIS,FALSE,EDI,TRUE,RyanAir,FR1111,FALSE",
            "27/07/10 13:10,EDI,TRUE,GDN,FALSE,RyanAir,FR2222,TRUE",  # Cancelled
            "02/05/11 10:50,WMI,FALSE,PIK,TRUE,RyanAir,FR3333,FALSE"
        ]
    
    def create_temp_csv(self, data):
        """Create a temporary CSV file with given data"""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        for row in data:
            temp_file.write(row + '\n')
        temp_file.close()
        return temp_file.name
    
    def test_date_parsing_formats(self):
        """Test parsing different date formats"""
        date_formats = [
            ("17/05/10 10:40", "%d/%m/%y %H:%M"),  # With time
            ("17/05/10", "%d/%m/%y"),              # Date only
            ("17/05/2010", "%d/%m/%Y"),            # Full year
        ]
        
        for date_str, expected_format in date_formats:
            with self.subTest(date_str=date_str):
                try:
                    parsed_date = datetime.strptime(date_str.strip(), expected_format).date()
                    self.assertIsNotNone(parsed_date)
                    self.assertEqual(parsed_date.year, 2010)
                    self.assertEqual(parsed_date.month, 5)
                    self.assertEqual(parsed_date.day, 17)
                except ValueError:
                    self.fail(f"Failed to parse date: {date_str}")
    
    def test_boolean_parsing(self):
        """Test parsing boolean values from CSV"""
        boolean_tests = [
            ("TRUE", True),
            ("True", True),
            ("1", True),
            ("FALSE", False),
            ("False", False),
            ("0", False),
            ("", False),
            ("invalid", False),
        ]
        
        for value, expected in boolean_tests:
            with self.subTest(value=value):
                # Handle both string and integer comparisons
                if isinstance(value, str):
                    result = True if value == "TRUE" or value == "True" or value == "1" else False
                else:
                    result = True if value == "TRUE" or value == "True" or value == 1 else False
                self.assertEqual(result, expected)
    
    def test_csv_row_parsing(self):
        """Test parsing individual CSV rows"""
        test_row = "17/05/10 10:40,LIS,FALSE,EDI,TRUE,RyanAir,FR1111,FALSE"
        reader = csv.reader(StringIO(test_row))
        row = next(reader)
        
        # Parse date
        date_temp = datetime.strptime(row[0].strip(), '%d/%m/%y %H:%M').date()
        dt = dateX(date_temp.year, date_temp.month, date_temp.day)
        
        # Parse booleans
        origin_uk = True if row[2] == "TRUE" or row[2] == "True" or row[2] == 1 else False
        destin_uk = True if row[4] == "TRUE" or row[4] == "True" or row[4] == 1 else False
        cancelled = True if row[7] == "TRUE" or row[7] == "True" or row[7] == 1 else False
        
        # Create flight object
        flight = Flight(dt, row[1], origin_uk, row[3], destin_uk)
        
        # Assertions
        self.assertEqual(flight.date.year, 2010)
        self.assertEqual(flight.date.month, 5)
        self.assertEqual(flight.date.day, 17)
        self.assertEqual(flight.origin, "LIS")
        self.assertFalse(flight.originUK)
        self.assertEqual(flight.destin, "EDI")
        self.assertTrue(flight.destinUK)
        self.assertFalse(cancelled)
    
    def test_csv_file_parsing(self):
        """Test parsing a complete CSV file"""
        temp_file = self.create_temp_csv(self.sample_csv_data)
        
        try:
            flights = []
            cancelled = []
            
            with open(temp_file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for ro in csv_reader:
                    try:
                        date_temp = datetime.strptime(ro[0].strip(), '%d/%m/%y %H:%M').date()
                    except ValueError:
                        try:
                            date_temp = datetime.strptime(ro[0].strip(), '%d/%m/%y').date()
                        except ValueError:
                            try:
                                date_temp = datetime.strptime(ro[0].strip(), '%d/%m/%Y').date()
                            except ValueError:
                                continue  # Skip invalid dates
                    
                    dt = dateX(date_temp.year, date_temp.month, date_temp.day)
                    ro[2] = True if ro[2] == "TRUE" or ro[2] == "True" or ro[2] == 1 else False
                    ro[4] = True if ro[4] == "TRUE" or ro[4] == "True" or ro[4] == 1 else False
                    ro[7] = True if ro[7] == "TRUE" or ro[7] == "True" or ro[7] == 1 else False
                    
                    if not ro[7]:  # Not cancelled
                        flights.append(Flight(dt, ro[1], ro[2], ro[3], ro[4]))
                    else:
                        cancelled.append([dt, ro[1], ro[2], ro[3], ro[4]])
            
            # Assertions
            self.assertEqual(len(flights), 5)
            self.assertEqual(len(cancelled), 0)
            
            # Check first flight
            first_flight = flights[0]
            self.assertEqual(first_flight.date.year, 2010)
            self.assertEqual(first_flight.origin, "LIS")
            self.assertFalse(first_flight.originUK)
            self.assertEqual(first_flight.destin, "EDI")
            self.assertTrue(first_flight.destinUK)
            
        finally:
            os.unlink(temp_file)
    
    def test_csv_with_cancelled_flights(self):
        """Test parsing CSV with cancelled flights"""
        temp_file = self.create_temp_csv(self.sample_csv_with_cancelled)
        
        try:
            flights = []
            cancelled = []
            
            with open(temp_file) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for ro in csv_reader:
                    try:
                        date_temp = datetime.strptime(ro[0].strip(), '%d/%m/%y %H:%M').date()
                    except ValueError:
                        try:
                            date_temp = datetime.strptime(ro[0].strip(), '%d/%m/%y').date()
                        except ValueError:
                            try:
                                date_temp = datetime.strptime(ro[0].strip(), '%d/%m/%Y').date()
                            except ValueError:
                                continue
                    
                    dt = dateX(date_temp.year, date_temp.month, date_temp.day)
                    ro[2] = True if ro[2] == "TRUE" or ro[2] == "True" or ro[2] == 1 else False
                    ro[4] = True if ro[4] == "TRUE" or ro[4] == "True" or ro[4] == 1 else False
                    ro[7] = True if ro[7] == "TRUE" or ro[7] == "True" or ro[7] == 1 else False
                    
                    if not ro[7]:  # Not cancelled
                        flights.append(Flight(dt, ro[1], ro[2], ro[3], ro[4]))
                    else:
                        cancelled.append([dt, ro[1], ro[2], ro[3], ro[4]])
            
            # Assertions
            self.assertEqual(len(flights), 2)  # 2 non-cancelled flights
            self.assertEqual(len(cancelled), 1)  # 1 cancelled flight
            
            # Check cancelled flight
            cancelled_flight = cancelled[0]
            self.assertEqual(cancelled_flight[0].year, 2010)
            self.assertEqual(cancelled_flight[1], "EDI")
            self.assertTrue(cancelled_flight[2])  # originUK
            self.assertEqual(cancelled_flight[3], "GDN")
            self.assertFalse(cancelled_flight[4])  # destinUK
            
        finally:
            os.unlink(temp_file)
    
    def test_invalid_date_formats(self):
        """Test handling of invalid date formats"""
        invalid_dates = [
            "32/05/10 10:40",  # Invalid day
            "17/13/10 10:40",  # Invalid month
            "17/05/10 25:40",  # Invalid hour
            "17/05/10 10:70",  # Invalid minute
            "invalid date",    # Completely invalid
            "17-05-10 10:40",  # Wrong separator
        ]
        
        for invalid_date in invalid_dates:
            with self.subTest(date=invalid_date):
                with self.assertRaises(ValueError):
                    datetime.strptime(invalid_date.strip(), '%d/%m/%y %H:%M')
    
    def test_missing_csv_fields(self):
        """Test handling of missing CSV fields"""
        incomplete_row = "17/05/10 10:40,LIS,FALSE,EDI,TRUE"  # Missing airline, flight number, cancelled
        
        reader = csv.reader(StringIO(incomplete_row))
        row = next(reader)
        
        # Should handle missing fields gracefully
        self.assertEqual(len(row), 5)
        self.assertEqual(row[0], "17/05/10 10:40")
        self.assertEqual(row[1], "LIS")
        self.assertEqual(row[2], "FALSE")
        self.assertEqual(row[3], "EDI")
        self.assertEqual(row[4], "TRUE")
    
    def test_whitespace_handling(self):
        """Test handling of whitespace in CSV data"""
        row_with_spaces = " 17/05/10 10:40 , LIS , FALSE , EDI , TRUE , RyanAir , FR1111 , FALSE "
        reader = csv.reader(StringIO(row_with_spaces))
        row = next(reader)
        
        # Test that whitespace is properly stripped
        date_temp = datetime.strptime(row[0].strip(), '%d/%m/%y %H:%M').date()
        self.assertEqual(date_temp.year, 2010)
        self.assertEqual(date_temp.month, 5)
        self.assertEqual(date_temp.day, 17)
        
        self.assertEqual(row[1].strip(), "LIS")
        self.assertEqual(row[2].strip(), "FALSE")
        self.assertEqual(row[3].strip(), "EDI")
        self.assertEqual(row[4].strip(), "TRUE")


if __name__ == '__main__':
    unittest.main()
