from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/outline")
def get_country_outline(country: str = Query(..., description="The name of the country")):
    """
    Fetch the Wikipedia page of the country, extract all headings (H1 to H6),
    and create a Markdown outline for the country.

    Args:
        country (str): The name of the country.

    Returns:
        dict: A dictionary containing the Markdown outline.
    """
    try:
        country = str(country)  # Ensure the country parameter is treated as a string
        # Fetch the Wikipedia page
        wikipedia_url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
        response = requests.get(wikipedia_url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail=f"Wikipedia page for {country} not found.")

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract headings (H1 to H6)
        headings = []
        for level in range(1, 7):
            for heading in soup.find_all(f"h{level}"):
                headings.append((level, heading.get_text(strip=True)))

        # Generate Markdown outline
        markdown_outline = ["## Contents", f"# {country}"]
        for level, text in headings:
            markdown_outline.append(f"{'#' * level} {text}")

        return {"outline": "\n".join(markdown_outline)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating outline: {str(e)}")

@app.get("/api/endpoint")
def get_api_endpoint():
    """
    Return the API endpoint URL for the Wikipedia outline service.

    Returns:
        dict: A dictionary containing the API endpoint URL.
    """
    return {"api_endpoint": f"http://0.0.0.0:8000/api/outline?country=<country_name>"}