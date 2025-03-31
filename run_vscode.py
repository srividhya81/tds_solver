import subprocess

def get_vscode_output():
    """Runs the `code -s` command and returns its output."""
    try:
        result = subprocess.run(["code", "-s"], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error occurred: {e.stderr}"

if __name__ == "__main__":
    output = get_vscode_output()
    print(output)