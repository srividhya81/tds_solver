import requests
import logging

def get_bounding_box_coordinate(location, country, coordinate_type):
    """
    Fetch the bounding box coordinate (minimum/maximum latitude/longitude) for a given location and country using the Nominatim API.

    Args:
        location (str): The name of the city or location.
        country (str): The name of the country.
        coordinate_type (str): The type of coordinate to fetch (e.g., 'min_lat', 'max_lat', 'min_lon', 'max_lon').

    Returns:
        float: The requested coordinate value.
    """
    try:
        # Log the received parameters
        logging.info(f"Received location: {location}, country: {country}, coordinate_type: {coordinate_type}")
        logging.info(f"Debugging: location={location}, country={country}, coordinate_type={coordinate_type}")

        # Validate the parameters
        if not location or not country:
            logging.error("Validation failed: Both location and country must be provided.")
            raise ValueError("Both location and country must be provided.")
            
        # Ensure the location and country are formatted correctly
        if not location or not country:
            raise ValueError("Both location and country must be provided.")

        formatted_query = f"{location.strip()}, {country.strip()}"
        logging.info(f"Formatted query for Nominatim API: {formatted_query}")

        # URL-encode the query
        import urllib.parse
        encoded_query = urllib.parse.quote(formatted_query)
        logging.info(f"Encoded query for Nominatim API: {encoded_query}")

        # Nominatim API URL
        url = f"https://nominatim.openstreetmap.org/search"

        # Query parameters
        params = {
            "q": f"{location}, {country}",
            "format": "json",
            "addressdetails": 1,
            "limit": 1,
            "polygon_geojson": 0
        }

        # Log the request details
        logging.info(f"Sending request to Nominatim with location: {location}, country: {country}, coordinate_type: {coordinate_type}")
        logging.info(f"Debugging before API call: location={location}, country={country}, coordinate_type={coordinate_type}")
        logging.info(f"Final parameters before API call: location={location}, country={country}, coordinate_type={coordinate_type}")

        # Make the API request
        response = requests.get(url, params=params)
        response.raise_for_status()

        # Log the full request URL and parameters
        logging.info(f"Request URL: {response.url}")
        logging.info(f"Response status code: {response.status_code}")
        logging.info(f"Response content: {response.text}")

        # Parse the response
        data = response.json()
        if not data:
            raise ValueError(f"No data found for location: {location}, country: {country}")

        # Extract the bounding box
        bounding_box = data[0].get("boundingbox", [])
        if len(bounding_box) != 4:
            raise ValueError("Bounding box data is incomplete.")

        # Map coordinate type to bounding box index
        coordinate_map = {
            "min_lat": float(bounding_box[0]),
            "max_lat": float(bounding_box[1]),
            "min_lon": float(bounding_box[2]),
            "max_lon": float(bounding_box[3])
        }

        # Return the requested coordinate
        return coordinate_map.get(coordinate_type, None)

    except Exception as e:
        return f"Error fetching bounding box coordinate: {e}"