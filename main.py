import os
import tempfile
import re
import json
import importlib
import inspect
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from question_handlers.duckdb_sql_query import extract_query_params, generate_duckdb_query
from question_handlers.apache_log_topipaddress import process_apache_logs
from question_handlers.apache_log_get_requests import process_apache_logs_get_requests
from question_handlers.unique_students_txt import count_unique_students
from question_handlers.calculate_total_margin import calculate_total_margin
from question_handlers.pdf_to_markdown import pdf_to_markdown
from question_handlers.daily_commit_function import daily_commit_function
from question_handlers.json_sort import sort_json_array
import logging


logging.basicConfig(level=logging.INFO)

app = FastAPI()

# ✅ Enable CORS (for frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

# ✅ Step 1: **Load Functions Dynamically from `question_handlers/`**
QUESTION_FUNCTION_MAP = {}

current_dir = os.path.dirname(os.path.abspath(__file__))
# Explicitly set the path to the `question_handlers` directory
question_handlers_dir = "/project2_tds_solver/src/question_handlers"
logging.info(f"Explicitly set question_handlers_dir path: {question_handlers_dir}")

if not os.path.exists(question_handlers_dir):
    raise FileNotFoundError(f"Error: The directory '{question_handlers_dir}' does not exist.")
else:
    print(f"Contents of '{question_handlers_dir}': {os.listdir(question_handlers_dir)}")

import sys

# Ensure the question_handlers directory is in the Python module search path
if question_handlers_dir not in sys.path:
    sys.path.append(question_handlers_dir)
    logging.info(f"Added question_handlers_dir to sys.path: {question_handlers_dir}")

# Add detailed logging to debug function loading and regex matching
logging.info("Starting function loading from question_handlers directory...")
logging.info(f"Scanning directory: {question_handlers_dir}")
logging.info(f"Files in directory: {os.listdir(question_handlers_dir)}")
for filename in os.listdir(question_handlers_dir):
    logging.info(f"Inspecting file: {filename}")
    if filename == "extract_pdf_table.py":
        logging.info("Found extract_pdf_table.py, attempting to load functions.")
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = f"question_handlers.{filename[:-3]}"
        try:
            # Add logging to confirm module import and function inspection
            logging.info(f"Attempting to import module: {module_name}")
            module = importlib.import_module(module_name)
            logging.info(f"Module imported successfully: {module_name}")
            logging.info(f"Inspecting functions in module: {module_name}")
            for name, func in inspect.getmembers(module, inspect.isfunction):
                logging.info(f"Function found: {name} in module: {module_name}")
                QUESTION_FUNCTION_MAP[name] = func
                logging.info(f"Function added to QUESTION_FUNCTION_MAP: {name}")
        except Exception as e:
            logging.error(f"Failed to load module {module_name}: {e}")

logging.info(f"Final QUESTION_FUNCTION_MAP: {QUESTION_FUNCTION_MAP}")

# Add the new function to the QUESTION_FUNCTION_MAP
from question_handlers.run_vscode import get_vscode_output


# ✅ Step 2: **Define Question-Function Mapping**
# Simplify the regex pattern for better matching
QUESTION_TO_FUNCTION = {
    r"how many times does .* appear as a key\\?": "count_key_in_json",
    r".*duckdb sql query.*find all posts IDs after ([\\dT:.-Z]+) with at least (\\d+) useful stars.*": "generate_duckdb_query",
    r".*duckdb sql query.*find all posts IDs after ([\\dT:.-Z]+) with at least (\\d+) comment with (\\d+) useful stars.*": "generate_duckdb_query",
    r".*reconstruct.*image.*": "reconstruct_image",
    r".*audiobook.*(?:from|between) (\d+(?:\.\d+)?) (?:to|and) (\d+(?:\.\d+)?) seconds.*": "transcribe_audio_from_url",
    r".*parse partial json.*": "parse_partial_json",
    r".*what is the total sales value.*parse partial json.*": "parse_partial_json",
    r".*total sales value.*": "parse_partial_json",
    r"how many units of (\w+) were sold in (\w+) on transactions with at least (\d+) units(?: in (.+\.json))?\?": "clean_up_and_calculate",
    r".*bytes did the top IP address .* download.*": "process_apache_logs",
    r".*requests under (\w+)/ on (\d{4}-\d{2}-\d{2}).*top IP address.*": "process_apache_logs",
    r".*Apache.*log.*top IP.*download.*": "process_apache_logs",
    r".*successful GET requests.*under /(\w+)/.*from (\d{1,2}):(\d{2}).*until before (\d{1,2}):(\d{2}).*on (\w+).*": "process_apache_logs_get_requests",
    r".*number of successful GET requests.*under /(\w+)/.*from (\d{1,2}).*until before (\d{1,2}).*on (\w+).*": "process_apache_logs_get_requests",
    r".*how many GET requests.*under /(\w+)/.*from (\d{1,2}).*to (\d{1,2}).*on (\w+).*": "process_apache_logs_get_requests",
    r"how many unique students are there in the file\?": "count_unique_students",
    r"what is the total margin for transactions before (.+?) for (\w+) sold in (.+?)\\?": "calculate_total_margin",
    r"what is the markdown content of the PDF, formatted with prettier@([\d.]+)\?": "pdf_to_markdown",
    r"what is the total (\w+) marks of students who scored (\d+) or more marks in (\w+) in groups (\d+)-(\d+) \(including both groups\)\?": "extract_total_marks",
    r"Enter your repository URL \(format: https://github.com/USER/REPO\):": "daily_commit",
    r"What is the link to the latest Hacker News post mentioning LLM having at least (\d+) points\?": "get_latest_hn_post_with_llm",
    r"What is the (minimum|maximum) (latitude|longitude) of the bounding box of the city (.+?) in the country (.+?) on the Nominatim API\?": "get_bounding_box_coordinate",
    r"What is the JSON weather forecast description for (.+?)\?": "get_weather_forecast",
    r"Write a web application that exposes an API with a single query parameter: \?country=.*create a Markdown outline for the country.*what is the url of your API endpoint": "get_country_outline",
    r"What is the total number of ducks across players on page number (\d+) of ESPN Cricinfo's ODI batting stats\?": "get_total_ducks",
    r"Analyze the sentiment of this \(meaningless\) text into GOOD, BAD or NEUTRAL\.": "analyze_sentiment",
    r"What is the output of code -s\?": "get_vscode_output",
    r"Send a HTTPS request to https://httpbin.org/get with the URL encoded parameter email set to (.+?)": "send_https_request",
    r"Download .* make sure it is called README\.md, and run npx -y prettier@3\.4\.2 README\.md \| sha256sum\.": "process_readme_file",
    r"=SUM\(ARRAY_CONSTRAIN\(SEQUENCE\((\d+), (\d+), (\d+), (\d+)\), (\d+), (\d+)\)\)": "calculate_google_sheets_sum",
    r"=SUM\(TAKE\(SORTBY\(\{(.+?)\}, \{(.+?)\}\), (\d+), (\d+)\)\)": "calculate_excel_formula",
    r"Just above this paragraph, there's a hidden input with a secret value\.": "extract_hidden_input_value",
    r"How many (\w+)s are there in the date range (\d{4}-\d{2}-\d{2}) to (\d{4}-\d{2}-\d{2})\?": "count_weekdays_in_range",
    r"Download and unzip file which has a single extract\.csv file inside\. What is the value in the \"answer\" column of the CSV file\?": "extract_answer_from_csv",
    r"sort (?:this|the) JSON array of objects? by the value of the (\w+) field(?:\. In case of a tie, sort by the (\w+) field)?": "sort_json_array"
}

# Add regex for comparing files and counting differing lines
QUESTION_TO_FUNCTION.update({
    r"how many lines are different between (\w+\.txt) and (\w+\.txt)\?": "count_different_lines"
})

# Update regex for generating total sales SQL query to make it more flexible
QUESTION_TO_FUNCTION.update({
    r"what is the total sales of all the items in the (\w+) ticket type\??(?: write sql to calculate it\.)?": "generate_total_sales_query"
})

# Update regex for sorting JSON arrays to make it more flexible
QUESTION_TO_FUNCTION.update({
    r"sort (?:this|the) JSON array of objects? by the value of the (\w+) field(?:\. In case of a tie, sort by the (\w+) field)?": "sort_json_array"
})

# Add regex for returning the raw GitHub URL for email.json
QUESTION_TO_FUNCTION.update({
    r"enter the raw github url of email\.json so we can verify it\.": "get_github_raw_url"
})

# Update the function to extract symbols from the question and process the zip file
QUESTION_TO_FUNCTION.update({
    r"sum up all the values where the symbol matches (.+?) across all three files\.": "sum_values_for_symbols"
})

# Add regex for starting the similarity API and returning the URL
QUESTION_TO_FUNCTION.update({
    r"what is the api url endpoint for your implementation\?": "start_similarity_api"
})

# Add regex for generating OpenAI embeddings request JSON
QUESTION_TO_FUNCTION.update({
    r"write the json body for a post request that will be sent to the openai api endpoint to obtain the text embedding.*": "generate_openai_embeddings_request"
})

# Add regex for generating JSON body for image processing
QUESTION_TO_FUNCTION.update({
    r"write the json body for a post request that will be sent to the openai api endpoint to extract text from an image.*": "create_post_request_json"
})

# Correcting the problematic regex pattern
QUESTION_TO_FUNCTION.update({
    r".*requests under (\\w+)/ on (\\d{4}-\\d{2}-\\d{2}).*top IP address.*": "process_apache_logs"
})

# Update regex for generating JSON body for image processing to make it more flexible
QUESTION_TO_FUNCTION.update({
    r".*json body.*post request.*openai api endpoint.*extract text from an image.*": "create_post_request_json"
})

# Update regex for generating JSON body for image processing to handle variations and optional characters
QUESTION_TO_FUNCTION.update({
    r".*json body.*post request.*openai api endpoint.*extract text from an image.*(-F)?": "create_post_request_json"
})

# Update regex for generating JSON body for image processing to be more generic and robust
QUESTION_TO_FUNCTION.update({
    r".*json body.*post request.*openai.*extract.*image.*": "create_post_request_json"
})

# Update regex for generating JSON body for image processing to match the exact phrasing in the curl command
QUESTION_TO_FUNCTION.update({
    r"Write just the JSON body \(not the URL, nor headers\) for the POST request that sends these two pieces of content \(text and image URL\) to the OpenAI API endpoint.*": "create_post_request_json"
})

# ✅ Step 3: **Define API Endpoint**
# Update the API endpoint to handle file uploads and pass the image path to the function
# Add debugging to log file handling in the API endpoint
# Add debugging to log file upload details
@app.post("/api")
async def handle_question(
    question: str = Form(...),
    file: UploadFile = File(None),
    product: str = Form(None),
    location: str = Form(None),
    min_units: int = Form(None),
    url: str = Form(None),
    html: str = Form(None),
    mapping: str = Form(None)
):
    logging.info(f"Received question: {question}")

    if file is None:
        logging.error("No file uploaded in the request.")
        raise HTTPException(status_code=400, detail="Missing required image file for JSON body generation")

    logging.info(f"Uploaded file details: filename={file.filename}, content_type={file.content_type}")

    # ✅ Step 4: **Find Matching Function**
    matched_function = None
    func_args = {}

    # Add logging to print the question and regex patterns being tested
    logging.info(f"Processing question: {question}")
    logging.info("Starting regex matching for question...")
    logging.info(f"Exact question string: {question}")
    # Update the regex matching logic to ensure case-insensitivity and proper matching
    for pattern, func_name in QUESTION_TO_FUNCTION.items():
        # Add detailed logging to debug regex matching
        logging.info(f"Testing regex pattern: {pattern}")
        logging.info(f"Input question for regex matching: '{question}'")  # Log the exact input question
        match = re.search(pattern, question, re.IGNORECASE)  # Perform regex matching
        if match:
            logging.info(f"Regex pattern matched: {pattern}")
            matched_function = QUESTION_FUNCTION_MAP.get(func_name, None)
            if matched_function:
                logging.info(f"Matched function: {func_name}")
            else:
                logging.error(f"Function {func_name} not found in QUESTION_FUNCTION_MAP")
                raise HTTPException(status_code=400, detail=f"Function {func_name} not found")

            # Handle file uploads for `create_post_request_json`
            if func_name == "create_post_request_json":
                if not file:
                    logging.error("Missing required image file for JSON body generation")
                    raise HTTPException(status_code=400, detail="Missing required image file for JSON body generation")
                try:
                    temp_dir = tempfile.gettempdir()
                    temp_file_path = os.path.join(temp_dir, file.filename)
                    logging.info(f"Saving uploaded file to: {temp_file_path}")
                    with open(temp_file_path, "wb") as temp_file:
                        temp_file.write(file.file.read())
                    logging.info(f"File saved successfully: {temp_file_path}")
                    func_args["image_path"] = temp_file_path
                except Exception as e:
                    logging.error(f"Error saving uploaded file: {e}")
                    raise HTTPException(status_code=500, detail=f"Error saving uploaded file: {str(e)}")

            break  # Stop checking once a match is found
        else:
            logging.info(f"Regex pattern did not match: {pattern}")
    else:
        logging.error("No regex pattern matched the question")

    if not matched_function:
        raise HTTPException(status_code=400, detail="No matching function found")

    print(f"Matched Function: {matched_function.__name__}")

    # ✅ Step 6: **Execute Function**
    try:
        result = matched_function(**func_args)
        logging.info(f"Result from {matched_function.__name__}: {result}")
        return result
    except Exception as e:
        logging.error(f"Error executing function {matched_function.__name__}: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

# Add a debug endpoint to inspect the QUESTION_FUNCTION_MAP
@app.get("/debug/functions")
async def debug_functions():
    return {"loaded_functions": list(QUESTION_FUNCTION_MAP.keys())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
