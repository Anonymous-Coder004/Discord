# app/utils/github_test.py

from langchain_community.utilities.github import GitHubAPIWrapper
from core.config import settings

with open(settings.github_app_private_key_path, "r") as f:
    private_key = f.read()

def read_main_file():
    github = GitHubAPIWrapper(
        github_app_id=settings.github_app_id,
        github_app_private_key=private_key,
        github_repository=settings.github_repository,
    )

    content = github.read_file("backend/app/main.py")

    print("----- FILE CONTENT START -----")
    print(content)
    print("----- FILE CONTENT END -----")

    return content

read_main_file()
