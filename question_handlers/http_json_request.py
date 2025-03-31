import requests
from urllib.parse import urlencode

def send_https_request(email: str):
    """
    Sends an HTTPS GET request to https://httpbin.org/get with the URL-encoded parameter `email`.

    Args:
        email (str): The email address to include as a parameter.

    Returns:
        dict: The JSON response body from the request.
    """
    base_url = "https://httpbin.org/get"
    params = {"email": email}
    url = f"{base_url}?{urlencode(params)}"

    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()

if __name__ == "__main__":
    email = "23ds1000022@ds.study.iitm.ac.in"  # Example email
    output = send_https_request(email)
    print(output)