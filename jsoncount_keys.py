import json
import logging
import re
import tempfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import os
async def process_json_file(question: str, file: UploadFile):
    """ Processes the uploaded JSON/JSONL file and counts occurrences of a key """

    if not file:
        return {"error": "No file uploaded"}

    # ✅ Extract the key from the question
    match = re.search(r"how many times does (\w+) appear as a key", question.lower())
    if not match:
        return {"error": "Could not extract the key from the question"}
    
    key = match.group(1)

    # ✅ Save the uploaded file to a temp location
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, file.filename)

    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(await file.read())  # ✅ Correct way to read an UploadFile in FastAPI

    # ✅ Count occurrences of the key in the JSON file
    result = count_key_in_json(temp_file_path, key)
    
    # ✅ Cleanup temp file
    os.remove(temp_file_path)

    return result

def count_key_in_json(file_path: str, key: str) -> dict:
    """
    Counts the occurrences of a specific key in a JSON or JSONL file.

    Args:
        file_path (str): The path to the JSON or JSONL file.
        key (str): The key to count.

    Returns:
        dict: A dictionary containing the count of the key.
    """
    
    key = key.lower()  # Ensure case-insensitive comparison

    def recursive_count(data, key):
        """ Recursively counts occurrences of `key` in nested dictionaries/lists. """
        count = 0
        if isinstance(data, dict):
            count += sum(1 for k in data if k.lower() == key)  # Count matching keys
            for v in data.values():
                count += recursive_count(v, key)  # Recursively check values
        elif isinstance(data, list):
            for item in data:
                count += recursive_count(item, key)  # Process lists
        return count

    total_count = 0

    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            first_line = json_file.readline().strip()

            if first_line.startswith("{") or first_line.startswith("["):
                # ✅ JSON file (single object or array)
                json_file.seek(0)  # Reset file pointer
                data = json.load(json_file)
                
                if isinstance(data, (dict, list)) and not data:
                    logging.warning("Empty JSON file.")
                    return {"count": 0}

                total_count = recursive_count(data, key)

            else:
                # ✅ JSONL file (line by line processing)
                json_file.seek(0)  # Reset file pointer
                for line in json_file:
                    try:
                        data = json.loads(line.strip())  # Load each JSON object
                        total_count += recursive_count(data, key)
                    except json.JSONDecodeError:
                        logging.warning(f"Skipping malformed JSON line: {line.strip()}")
                        continue  # Skip malformed lines

    except Exception as e:
        logging.error(f"Error processing JSON file: {e}")
        return {"count": 0}  # Return 0 instead of raising an exception

    return {"count": total_count}
