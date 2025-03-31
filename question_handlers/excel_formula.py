import numpy as np

def calculate_excel_formula(values, sort_by, take_rows, take_cols):
    """
    Simulates the Excel formula =SUM(TAKE(SORTBY(values, sort_by), take_rows, take_cols))

    Args:
        values (list): The array of values to sort.
        sort_by (list): The array of values to sort by.
        take_rows (int): Number of rows to take.
        take_cols (int): Number of columns to take.

    Returns:
        int: The sum of the resulting array.
    """
    # Convert inputs to numpy arrays
    values = np.array(values)
    sort_by = np.array(sort_by)

    # Adjust the logic to match Microsoft 365 Excel behavior
    # Sort the values array based on the sort_by array
    sorted_indices = np.argsort(sort_by)
    sorted_values = np.array(values)[sorted_indices]

    # Take the specified rows and columns (adjusted for Excel behavior)
    taken_values = sorted_values[:take_rows * take_cols]

    # Calculate the sum
    return int(np.sum(taken_values))

