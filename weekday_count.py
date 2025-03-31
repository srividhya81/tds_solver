from datetime import datetime, timedelta

def count_weekdays_in_range(start_date: str, end_date: str, weekday: str) -> int:
    """
    Counts the number of occurrences of a specific weekday in a given date range.

    Args:
        start_date (str): The start date in the format 'YYYY-MM-DD'.
        end_date (str): The end date in the format 'YYYY-MM-DD'.
        weekday (str): The name of the weekday (e.g., 'Monday', 'Tuesday').

    Returns:
        int: The number of occurrences of the specified weekday in the date range.
    """
    # Convert weekday name to its corresponding integer (0=Monday, 6=Sunday)
    weekday_map = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6
    }

    if weekday not in weekday_map:
        raise ValueError(f"Invalid weekday: {weekday}")

    weekday_int = weekday_map[weekday]

    # Parse the start and end dates
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    if start > end:
        raise ValueError("Start date must be before or equal to end date")

    # Count the occurrences of the specified weekday
    count = 0
    current_date = start

    while current_date <= end:
        if current_date.weekday() == weekday_int:
            count += 1
        current_date += timedelta(days=1)

    return count

if __name__ == "__main__":
    # Example usage
    start_date = "1983-11-29"
    end_date = "2013-03-27"
    weekday = "Wednesday"
    result = count_weekdays_in_range(start_date, end_date, weekday)
    print(result)