import subprocess
import hashlib

def process_readme_file(file_path):
    """
    Processes the README.md file using npx prettier and calculates its SHA-256 checksum.

    Args:
        file_path (str): The path to the README.md file.

    Returns:
        str: The SHA-256 checksum of the formatted file.
    """
    try:
        # Run npx prettier on the file
        result = subprocess.run(
            ["npx", "-y", "prettier@3.4.2", file_path],
            capture_output=True,
            text=True,
            check=True
        )

        # Get the formatted content
        formatted_content = result.stdout

        # Calculate the SHA-256 checksum
        sha256_hash = hashlib.sha256(formatted_content.encode('utf-8')).hexdigest()

        return sha256_hash

    except subprocess.CalledProcessError as e:
        return f"Error running npx prettier: {e.stderr}"
    except Exception as e:
        return f"Error processing README.md: {e}"

if __name__ == "__main__":
    # Example usage
    file_path = "README.md"  # Replace with the actual file path
    output = process_readme_file(file_path)
    print(output)