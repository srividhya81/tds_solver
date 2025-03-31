def count_different_lines(file1_path, file2_path):
    """
    Compare two files line by line and count the number of lines that are different.

    Args:
        file1_path (str): Path to the first file.
        file2_path (str): Path to the second file.

    Returns:
        int: The number of lines that are different between the two files.
    """
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        file1_lines = file1.readlines()
        file2_lines = file2.readlines()

    # Ensure both files have the same number of lines
    if len(file1_lines) != len(file2_lines):
        raise ValueError("Files have different number of lines")

    # Count the number of differing lines
    different_lines_count = sum(1 for line1, line2 in zip(file1_lines, file2_lines) if line1 != line2)

    return different_lines_count