import subprocess

def start_similarity_api():
    """
    Start the similarity API in the background and return the API URL endpoint.

    Returns:
        str: The API URL endpoint.
    """
    # Start the API in the background
    subprocess.Popen(["uvicorn", "similarity_api:app", "--host", "127.0.0.1", "--port", "8000"], cwd="/Users/srividhyaanand/project2_tds_solver/venv/fastapi-app/src", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Return the API URL endpoint
    return "http://127.0.0.1:8000/similarity"