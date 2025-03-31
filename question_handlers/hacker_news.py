import requests
import xml.etree.ElementTree as ET

def get_latest_hn_post_with_llm(min_points=34):
    """
    Fetch the latest Hacker News post mentioning LLM with at least the specified number of points.

    Args:
        min_points (int): Minimum number of points required for the post.

    Returns:
        str: URL of the latest Hacker News post meeting the criteria, or None if no such post exists.
    """
    # HNRSS API URL for latest posts
    hn_rss_url = "https://hnrss.org/newest"

    try:
        # Fetch the RSS feed
        response = requests.get(hn_rss_url)
        response.raise_for_status()

        # Parse the RSS feed
        root = ET.fromstring(response.content)

        # Iterate over <item> elements
        for item in root.findall(".//item"):
            title = item.find("title").text if item.find("title") is not None else ""
            link = item.find("link").text if item.find("link") is not None else ""
            points = item.find("hn:points", namespaces={"hn": "https://hnrss.org/"}).text if item.find("hn:points", namespaces={"hn": "https://hnrss.org/"}) is not None else "0"

            # Check if the title contains 'LLM' and points meet the minimum requirement
            if "LLM" in title and int(points) >= min_points:
                return link

        return None  # No matching post found

    except Exception as e:
        return f"Error fetching or parsing HNRSS feed: {e}"