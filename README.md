# ifcdate

A Python library and CLI to convert Unix timestamps to the International Fixed Calendar (IFC) format and vice versa.

**Note:** This implementation deviates from the original IFC proposal by placing leap year days (Year Day and Leap Day) at the end of the year.

## Features

- Convert Unix timestamps to IFC dates.
- Convert IFC dates (format `YYYY-MM-DD`) to Unix timestamps.
- Supports leap years and special days (Leap Day, Year Day).
- Handles invalid input with clear error messages.
- CLI and Python API available.
- Falls back to ISO format for unsupported output formats.

## Installation

```bash
pip install .
```

## CLI Usage
```bash
python -m ifcdate.cli --unix 1748649600
python -m ifcdate.cli --date 2025-06-15
```
## Python API Usage

```python
from ifcdate.core import unix_to_ifc, ifc_to_unix

# Convert Unix timestamp to IFC date
ifc_date = unix_to_ifc(1748649600)  # e.g. '2025-06-11'

# Convert IFC date to Unix timestamp
unix_time = ifc_to_unix('2025-13-29')  # e.g. 1767139200
```

## Testing
Run all tests and check coverage with:
```bash
pytest --cov=ifcdate --cov-branch --cov-report=term-missing
```

## Notes
- Invalid or unsupported formats raise a ValueError.
- For unknown output formats, the function falls back to the default ISO format (YYYY-MM-DD).
