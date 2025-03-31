import zipfile
import os
import csv
import logging

def extract_answer_from_csv(zip_file_path):
    """
    Extracts the value in the "answer" column of the CSV file inside the given zip file.

    Args:
        zip_file_path (str): The path to the zip file containing the CSV file.

    Returns:
        list: A list of values from the "answer" column in the CSV file.
    """
    temp_dir = os.path.splitext(zip_file_path)[0]  # Create a temporary directory based on the zip file name

    try:
        # Log the first few bytes of the file for debugging
        with open(zip_file_path, 'rb') as f:
            file_signature = f.read(4)
            logging.info(f"File signature: {file_signature}")

        # Validate if the file is a valid zip file
        if not zipfile.is_zipfile(zip_file_path):
            raise ValueError("The uploaded file is not a valid zip file")

        # Unzip the file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Find the CSV file inside the extracted folder
        csv_file_path = os.path.join(temp_dir, "extract.csv")
        if not os.path.exists(csv_file_path):
            raise FileNotFoundError("extract.csv not found in the zip file")

        # Read the "answer" column from the CSV file
        answers = []
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            if "answer" not in reader.fieldnames:
                raise ValueError("The 'answer' column is missing in the CSV file")

            for row in reader:
                answers.append(row["answer"])

        return answers

    finally:
        # Clean up the temporary directory
        if os.path.exists(temp_dir):
            for root, dirs, files in os.walk(temp_dir, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(temp_dir)




