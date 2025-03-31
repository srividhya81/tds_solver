import subprocess

def daily_commit_function():
    try:
        # Get the repository URL using git command
        result = subprocess.run(["git", "config", "--get", "remote.origin.url"], capture_output=True, text=True, check=True)
        repo_url = result.stdout.strip()
        return repo_url
    except subprocess.CalledProcessError as e:
        return f"Error retrieving repository URL: {e}"