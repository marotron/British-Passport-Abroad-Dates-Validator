#!/usr/bin/env python3
"""
Test runner for British Passport Abroad Dates Validator
"""
import unittest
import sys
import os

# Add parent directory to path to import the main module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all test modules
from test_datex import TestDateX
from test_datetimex import TestDateTimeX
from test_flight import TestFlight
from test_period import TestPeriod
from test_day import TestDay
from test_utility_functions import TestUtilityFunctions
from test_csv_parsing import TestCSVParsing


def create_test_suite():
    """Create and return a test suite with all tests"""
    suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestDateX,
        TestDateTimeX,
        TestFlight,
        TestPeriod,
        TestDay,
        TestUtilityFunctions,
        TestCSVParsing,
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    return suite


def run_tests():
    """Run all tests and return the result"""
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result


if __name__ == '__main__':
    print("Running British Passport Abroad Dates Validator Tests")
    print("=" * 60)
    
    result = run_tests()
    
    print("\n" + "=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
