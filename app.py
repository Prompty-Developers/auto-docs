from github import Github
from dotenv import load_dotenv
import os
load_dotenv()

# Replace 'your_token' with your personal access token
g = Github(os.getenv('GH_TOKEN'))

repository_name = os.getenv('TEST_REPO')
pr = 594

repo = g.get_repo(repository_name)

pull_request = repo.get_pull(pr)

files_changed = pull_request.get_files()

for file in files_changed:
    print(f"File: {file.filename}")
    print(f"Diff: {file.patch}")
    print("\n")