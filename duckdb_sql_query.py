import re
import logging

def extract_query_params(question: str):
    """
    Extracts the timestamp and min_useful_stars from the question string.

    Args:
        question (str): The input question string.

    Returns:
        tuple: A tuple containing the timestamp (str) and min_useful_stars (int).
    """
    logging.info(f"Extracting parameters from question: {question}")
    timestamp_match = re.search(r'after ([\d\-T:.Z]+)', question)
    stars_match = re.search(r'at least (\d+) useful stars', question)

    if not timestamp_match or not stars_match:
        logging.error("Invalid question format. Could not extract parameters.")
        raise ValueError("Invalid question format. Could not extract parameters.")

    timestamp = timestamp_match.group(1)
    min_useful_stars = int(stars_match.group(1))
    logging.info(f"Extracted timestamp: {timestamp}, min_useful_stars: {min_useful_stars}")

    return timestamp, min_useful_stars

def generate_duckdb_query(timestamp: int, min_useful_stars: int):
    return f"""
        SELECT post_id
        FROM social_media
        WHERE timestamp > {timestamp}
        AND EXISTS (
            SELECT 1
            FROM json_each(social_media.comments) AS t
            WHERE t.key = 'stars' AND t.value::INTEGER >= {min_useful_stars}
        )
        ORDER BY post_id ASC;
    """