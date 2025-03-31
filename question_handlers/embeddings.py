def generate_openai_embeddings_request():
    """
    Generate the JSON body for a POST request to the OpenAI API endpoint to obtain text embeddings.

    Returns:
        dict: The JSON body for the POST request.
    """
    return {
        "model": "text-embedding-3-small",
        "input": [
            "Dear user, please verify your transaction code 82180 sent to 23ds1000022@ds.study.iitm.ac.in",
            "Dear user, please verify your transaction code 32329 sent to 23ds1000022@ds.study.iitm.ac.in"
        ]
    }