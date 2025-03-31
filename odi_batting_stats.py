import requests
from bs4 import BeautifulSoup

def get_total_ducks(page_number):
    """
    Fetch the total number of ducks across players from ESPN Cricinfo's ODI batting stats for a given page number.

    Args:
        page_number (int): The page number to fetch the stats from.

    Returns:
        int: The total number of ducks across players on the specified page.
    """
    try:
        # Construct the URL for the specified page number
        base_url = "https://stats.espncricinfo.com/ci/engine/stats/index.html"
        params = {
            "class": "2",  # ODI matches
            "template": "results",
            "type": "batting",
            "page": page_number
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Fetch the page content with headers
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Debugging: Log the fetched HTML content
        with open("debug_page.html", "w", encoding="utf-8") as debug_file:
            debug_file.write(soup.prettify())

        # Find the table containing the stats
        table = soup.find("table", class_="engineTable")
        if not table:
            raise ValueError("Stats table not found on the page.")

        # Ensure the correct column is being parsed for 'Ducks'
        header_row = table.find("tr", class_="head")
        # Debugging: Log the table headers
        if header_row:
            headers = [header.get_text(strip=True) for header in header_row.find_all("th")]
            with open("debug_headers.txt", "w", encoding="utf-8") as debug_headers_file:
                debug_headers_file.write("\n".join(headers))
            if "Ducks" in headers:
                ducks_index = headers.index("Ducks")
            else:
                raise ValueError("'Ducks' column not found in the table headers.")

        # Extract the 'Ducks' column and calculate the total
        total_ducks = 0
        rows = table.find_all("tr", class_="data1")
        # Debugging: Log the rows of the table
        with open("debug_rows.txt", "w", encoding="utf-8") as debug_rows_file:
            for row in rows:
                columns = [col.get_text(strip=True) for col in row.find_all("td")]
                debug_rows_file.write("\t".join(columns) + "\n")
        for row in rows:
            columns = row.find_all("td")
            if len(columns) > ducks_index:
                ducks = columns[ducks_index].get_text(strip=True)
                if ducks.isdigit():
                    total_ducks += int(ducks)

        return total_ducks

    except Exception as e:
        return f"Error fetching ducks data: {e}"