import time
import argparse
from datetime import datetime, UTC, timedelta

IFC_MONTHS = [
    "January", "February", "March", "April", "May", "June", "Sol",
    "July", "August", "September", "October", "November", "December"
]

def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def unix_to_ifc(unix_time):
    dt = datetime.fromtimestamp(unix_time, UTC)
    year = dt.year
    start_of_year = datetime(year, 1, 1, tzinfo=UTC)
    delta_days = (dt - start_of_year).days
    leap = is_leap_year(year)

    if delta_days == 364:
        month = 13
        day = 29
    elif leap and delta_days == 365:
        month = 13
        day = 30
    else:
        if delta_days > 365 or delta_days < 0:
            return f"{year}-Invalid-Invalid"
        month = (delta_days // 28) + 1
        day = (delta_days % 28) + 1

    return f"{year}-{month:02d}-{day:02d}"

def date_to_unix(date_string):
    dt = datetime.strptime(date_string, "%Y-%m-%d")
    return int(time.mktime(dt.timetuple()))

def ifc_to_unix(ifc_string):
    try:
        parts = ifc_string.strip().split("-")
        if len(parts) != 3:
            raise ValueError("IFC date must be in YYYY-MM-DD format")

        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])

        leap = is_leap_year(year)

        if month < 1 or month > 13:
            raise ValueError("Month must be between 1 and 13")
        if day < 1:
            raise ValueError("Day must be positive")

        if month == 13:
            if day > 30:
                raise ValueError("December (month 13) max day is 30")
            if day == 30 and not leap:
                raise ValueError("Leap Day (Dec 30) occurs only in leap years")
            if day > 28 and day < 29:
                raise ValueError("Days above 28 allowed only in month 13")

        else:
            if day > 28:
                raise ValueError("Day cannot be greater than 28 for months 1 to 12")

        day_of_year = (month - 1) * 28 + (day - 1)

        start_of_year = datetime(year, 1, 1, tzinfo=UTC)
        gregorian_date = start_of_year + timedelta(days=day_of_year)
        return int(gregorian_date.timestamp())

    except Exception as e:
        raise ValueError(f"Error parsing IFC date '{ifc_string}': {e}")

def print_fancy(unix_time):
    dt = datetime.fromtimestamp(unix_time, UTC)
    ifc = unix_to_ifc(unix_time)
    print("="*40)
    print(f"Gregorian Date : {dt.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"Unix Timestamp : {unix_time}")
    print(f"IFC Date       : {ifc}")
    print("="*40)

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Convert dates between Gregorian, Unix time, and International Fixed Calendar (IFC).\n\n"
            "Examples:\n"
            "  Convert Gregorian to IFC:\n"
            "    script.py -d 2025-05-31\n\n"
            "  Convert Unix to IFC:\n"
            "    script.py -u 1759257600\n\n"
            "  Convert IFC to Unix/Gregorian:\n"
            "    script.py -i 2025-05-27\n"
            "    script.py -i 2025-13-29   # Year Day\n"
            "    script.py -i 2024-13-30   # Leap Day\n\n"
            "If no argument is provided, current time is used."
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-d", "--date", help="Gregorian date (YYYY-MM-DD)")
    parser.add_argument("-u", "--unix", type=int, help="Unix timestamp")
    parser.add_argument("-i", "--ifc", help="IFC date string (YYYY-MM-DD, months 1-13, days 1-28 or 29/30 for month 13)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed output")
    args = parser.parse_args()

    try:
        if args.date:
            unix_time = date_to_unix(args.date)
            if args.verbose:
                print_fancy(unix_time)
            else:
                print(unix_to_ifc(unix_time))
        elif args.unix:
            if args.verbose:
                print_fancy(args.unix)
            else:
                print(unix_to_ifc(args.unix))
        elif args.ifc:
            unix_time = ifc_to_unix(args.ifc)
            if args.verbose:
                print_fancy(unix_time)
            else:
                print(args.ifc)
        else:
            unix_time = int(time.time())
            if args.verbose:
                print_fancy(unix_time)
            else:
                print(unix_to_ifc(unix_time))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()