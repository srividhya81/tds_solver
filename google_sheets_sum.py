import numpy as np

def calculate_google_sheets_sum(rows: int, cols: int, start: int, step: int, constrain_rows: int, constrain_cols: int):
    """
    Simulates the Google Sheets formula =SUM(ARRAY_CONSTRAIN(SEQUENCE(rows, cols, start, step), constrain_rows, constrain_cols))

    Args:
        rows (int): Number of rows in the sequence.
        cols (int): Number of columns in the sequence.
        start (int): Starting number of the sequence.
        step (int): Step size for the sequence.
        constrain_rows (int): Number of rows to constrain.
        constrain_cols (int): Number of columns to constrain.

    Returns:
        int: The sum of the constrained array.
    """
    # Generate the sequence
    sequence = np.arange(start, start + rows * cols * step, step).reshape(rows, cols)

    # Apply the constraint
    constrained_array = sequence[:constrain_rows, :constrain_cols]

    # Calculate the sum
    return int(np.sum(constrained_array))

