import re
import pandas as pd
import logging
from datetime import datetime
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_total_margin(file_path, question):
    """
    Calculate the total margin for transactions based on the uploaded Excel file.
    The function extracts the product, location, and date from the question and filters the data accordingly.

    Args:
        file_path (str): Path to the uploaded Excel file.
        question (str): The question containing product, location, and date details.

    Returns:
        dict: {"total_margin": float} or {"error": str} if an error occurs.
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return {"error": f"File not found: {file_path}"}

    try:
        # Extract product, location, and date from the question
        product_match = re.search(r'for (\w+) sold', question)
        location_match = re.search(r'in (.+?) \(', question)
        date_match = re.search(r'before (.+?) \(', question)

        if not product_match or not location_match or not date_match:
            return {"error": "Could not extract product, location, or date from the question."}

        product = product_match.group(1).strip()
        location = location_match.group(1).strip()
        date_str = date_match.group(1).strip()

        # Parse the date
        try:
            # Adjusted to handle the date format without parentheses around the timezone
            date_limit = datetime.strptime(date_str, "%a %b %d %Y %H:%M:%S GMT%z")
        except ValueError as e:
            logger.error(f"Error parsing date: {e}")
            return {"error": "Invalid date format in the question."}

        # Check if the file is empty
        if os.path.getsize(file_path) == 0:
            logger.error("The uploaded file is empty.")
            return {"error": "The uploaded file is empty. Please upload a valid .xlsx file."}

        # Enhanced validation to provide detailed diagnostics
        try:
            with open(file_path, 'rb') as f:
                header = f.read(4)
                if header != b'PK\x03\x04':  # Check for the ZIP file magic number
                    logger.error(f"Invalid file header: {header}")
                    return {"error": "The uploaded file is not a valid .xlsx file. Please ensure the file is correctly formatted."}
        except Exception as e:
            logger.error(f"Error validating file format: {e}")
            return {"error": "Failed to validate the file format. Please check the file and try again."}

        # Load the Excel file with the openpyxl engine explicitly specified
        df = pd.read_excel(file_path, engine='openpyxl')

        # Ensure required columns exist
        required_columns = {"Product", "Location", "Date", "Margin"}
        if not required_columns.issubset(df.columns):
            return {"error": f"Missing required columns in the Excel file. Required columns: {required_columns}"}

        # Normalize the location column for case-insensitive matching and handle misspellings/abbreviations
        df["Location"] = df["Location"].str.lower()
        location_variants = [
            location.lower(),
            "us", "united states", "america", "u.s.", "u.s.a.", "usa", "states"
        ]

        # Use fuzzy matching to handle misspellings
        from rapidfuzz import fuzz
        def is_location_match(loc):
            return any(fuzz.ratio(loc, variant) > 80 for variant in location_variants)

        df = df[df["Location"].apply(is_location_match)]

        # Filter the data
        filtered_df = df[
            (df["Product"].str.contains(product, case=False, na=False)) &
            (pd.to_datetime(df["Date"]) < date_limit)
        ]

        # Calculate the total margin
        total_margin = filtered_df["Margin"].sum()

        logger.info(f"Total margin calculated: {total_margin}")
        return {"total_margin": total_margin}

    except Exception as e:
        logger.exception(f"Error processing the Excel file: {e}")
        return {"error": f"Error processing the file: {str(e)}"}

# Example usage
if __name__ == "__main__":
    file_path = "path/to/transactions.xlsx"
    question = "What is the total margin for transactions before Sat Nov 12 2022 23:33:09 GMT+0530 (India Standard Time) for Theta sold in US?"
    result = calculate_total_margin(file_path, question)
    print(result)