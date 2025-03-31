from fastapi import FastAPI
import subprocess
import time

app = FastAPI()

def generate_api_script():
    """Generates a FastAPI script dynamically."""
    script_content = """ 
from fastapi import FastAPI

app = FastAPI()

@app.get("/execute")
def execute_function():
    return {"message": "Function executed in generated API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
    """

    with open("generated_api.py", "w") as f:
        f.write(script_content)


def generate_api():
    """Creates and starts the generated API as a subprocess."""
    generate_api_script()  # Create the script

    # Run the generated API as a subprocess
    process = subprocess.Popen(["python", "generated_api.py"])

    time.sleep(2)  # Allow some time for the server to start

    return {"message": "Generated API started on port 8001"}

