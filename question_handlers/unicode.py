import os
import zipfile
import csv
import logging

def sum_values_for_symbols(zip_file_path, symbols):
    """
    Process files in a zip archive with different encodings and sum values for specific symbols.

    Args:
        zip_file_path (str): Path to the zip file containing the files.
        symbols (list): List of symbols to match.

    Returns:
        float: The sum of all values associated with the specified symbols.
    """
    temp_dir = os.path.splitext(zip_file_path)[0]  # Create a temporary directory based on the zip file name
    total_sum = 0.0

    try:
        # Validate if the file is a valid zip file
        if not zipfile.is_zipfile(zip_file_path):
            raise ValueError("The uploaded file is not a valid zip file")

        # Unzip the file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Define file encodings and delimiters
        file_configs = {
            "data1.csv": {"encoding": "cp1252", "delimiter": ","},
            "data2.csv": {"encoding": "utf-8", "delimiter": ","},
            "data3.txt": {"encoding": "utf-16", "delimiter": "\t"}
        }

        # Process each file
        for file_name, config in file_configs.items():
            file_path = os.path.join(temp_dir, file_name)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"{file_name} not found in the zip file")

            with open(file_path, mode='r', encoding=config["encoding"]) as file:
                reader = csv.DictReader(file, delimiter=config["delimiter"])
                if "symbol" not in reader.fieldnames or "value" not in reader.fieldnames:
                    raise ValueError(f"The required columns are missing in {file_name}")

                for row in reader:
                    if row["symbol"] in symbols:
                        total_sum += float(row["value"])

        return total_sum

    finally:
        # Clean up the temporary directory
        if os.path.exists(temp_dir):
            for root, dirs, files in os.walk(temp_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(temp_dir)