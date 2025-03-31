import base64
import json

def create_post_request_json(image_path):
    """
    Creates a JSON body for a POST request to the OpenAI API endpoint.

    Args:
        image_path (str): The file path to the image.

    Returns:
        dict: The JSON body for the POST request.
    """
    try:
        # Read the image file and encode it to base64
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        # Create the base64 URL
        base64_url = f"data:image/jpeg;base64,{base64_image}"

        # Construct the JSON body
        json_body = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user", "content": "Extract text from this image."},
                {"role": "user", "content": base64_url}
            ]
        }

        return json_body

    except Exception as e:
        return {"error": str(e)}


    # Example usage
    image_path = "example_invoice.jpg"  # Replace with the actual image file path
    json_body = create_post_request_json(image_path)
    print(json.dumps(json_body, indent=4))