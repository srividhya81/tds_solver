import logging
import os
import re
import csv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def count_unique_students(file_path):
    """
    Count the number of unique students in a text file containing student marks.
    The function identifies students uniquely by their alphanumeric IDs (e.g., UA1OB2H69A).
    
    Args:
        file_path (str): Path to the text file containing student marks
        
    Returns:
        dict: {"count": int} or {"error": str} if an error occurs
    """
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return {"error": f"File not found: {file_path}"}
    
    if os.path.getsize(file_path) == 0:
        logger.warning(f"File is empty: {file_path}")
        return {"count": 0, "note": "The file is empty."}
    
    try:
        unique_student_ids = set()
        
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    # Extract the student ID using a regex for alphanumeric IDs
                    match = re.match(r'([A-Za-z0-9]+)', line)
                    if match:
                        student_id = match.group(1).strip()
                        unique_student_ids.add(student_id)
        
        logger.info(f"Found {len(unique_student_ids)} unique student IDs in {file_path}")
        return {"count": len(unique_student_ids)}
    
    except Exception as e:
        logger.exception(f"Error processing student marks file: {e}")
        return {"error": f"Error processing file: {str(e)}"}

