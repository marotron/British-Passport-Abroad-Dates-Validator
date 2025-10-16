# British Passport Abroad Dates Validator - Tests

This directory contains comprehensive unit tests for the British Passport Abroad Dates Validator project.

## Test Structure

The test suite is organized into the following test files:

- `test_datex.py` - Tests for the `dateX` class (extended date functionality)
- `test_datetimex.py` - Tests for the `datetimeX` class (extended datetime functionality)
- `test_flight.py` - Tests for the `Flight` class
- `test_period.py` - Tests for the `Period` class
- `test_day.py` - Tests for the `Day` class
- `test_utility_functions.py` - Tests for utility functions (`colOrCol`, `grnOrRed`)
- `test_csv_parsing.py` - Tests for CSV parsing logic
- `run_tests.py` - Test runner script
- `requirements.txt` - Test requirements (none needed - uses standard library only)

## Running Tests

### Run All Tests
```bash
python3 tests/run_tests.py
```

### Run Individual Test Files
```bash
python3 tests/test_datex.py
python3 tests/test_datetimex.py
python3 tests/test_flight.py
python3 tests/test_period.py
python3 tests/test_day.py
python3 tests/test_utility_functions.py
python3 tests/test_csv_parsing.py
```

### Run Tests with Verbose Output
```bash
python3 -m unittest discover tests -v
```

## Test Coverage

The test suite covers:

### dateX Class
- String representation
- Date manipulation methods (`firstDay`, `lastDay`, `shiftDay`, `shiftMonth`, `shiftYear`)
- `replace` method
- Inheritance from `date` class
- Edge cases (leap years, month boundaries, year boundaries)

### datetimeX Class
- String representation
- Inheritance from `datetime` class
- Date and time properties
- `replace` method
- `strptime` class method
- Arithmetic operations
- Comparison operations

### Flight Class
- Initialization with various parameters
- `getDate` method
- Different flight types (UK-UK, UK-foreign, foreign-UK, foreign-foreign)
- Airport code handling
- Boolean value handling

### Period Class
- Initialization with start and end dates
- `getDateFrom` method
- Duration calculations
- Edge cases (single day, cross-year periods, leap years)
- Integration with `dateX` methods

### Day Class
- Initialization with date and abroad status
- `getDate` method
- Boolean status handling
- Various date combinations
- Edge cases (leap day, year boundaries)

### Utility Functions
- `colOrCol` function with different color combinations
- `grnOrRed` function with various boolean inputs
- Unicode and special character handling
- Color code validation

### CSV Parsing
- Different date format parsing
- Boolean value parsing
- Complete CSV file parsing
- Cancelled flight handling
- Invalid data handling
- Whitespace handling
- Missing field handling

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Test Philosophy

The tests follow these principles:

1. **Comprehensive Coverage**: Each class and function has multiple test cases covering normal usage, edge cases, and error conditions.

2. **Isolation**: Each test is independent and can be run in any order.

3. **Clarity**: Test names clearly describe what is being tested.

4. **Maintainability**: Tests are well-organized and easy to understand.

5. **Real-world Scenarios**: Tests include realistic data that would be encountered in actual usage.

## Adding New Tests

When adding new functionality to the main codebase:

1. Create corresponding test cases in the appropriate test file
2. Follow the existing naming conventions (`test_*`)
3. Include both positive and negative test cases
4. Test edge cases and error conditions
5. Update this README if new test files are added

## Continuous Integration

These tests are designed to be run in CI/CD environments. The test runner (`run_tests.py`) returns appropriate exit codes:
- 0 for success
- 1 for failure

This allows automated systems to detect test failures and take appropriate action.
