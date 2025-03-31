from bs4 import BeautifulSoup

def extract_hidden_input_value(html_content):
    """
    Extracts the value of a hidden input field from the given HTML content.

    Args:
        html_content (str): The HTML content as a string.

    Returns:
        str: The value of the hidden input field, or None if not found.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    hidden_input = soup.find("input", {"type": "hidden"})
    if hidden_input and "value" in hidden_input.attrs:
        return hidden_input["value"]
    return None

if __name__ == "__main__":
    # Example usage
    html = """
    <html>
        <body>
            <form>
                <input type="hidden" name="secret" value="my_secret_value">
            </form>
        </body>
    </html>
    """
    result = extract_hidden_input_value(html)
    print(result)