#!/usr/bin/env python
import base64
import requests
import time

from requests import Response
from typing import Any, Dict, Literal, LiteralString, Optional

from github import Github

from backend.defaults import (
    DEFAULT_ACCESS_TOKEN,
    DEFAULT_DEVCONTAINER_JSON,
    DEFAULT_DOCKERFILE,
    DEFAULT_REPO_URL,
    DEFAULT_SAMPLE_SCRIPT,
    DEFAULT_USERNAME,
)


def create_gh_client(access_token: str) -> Github:
    """Create a Github client instance using an access token"""
    return Github(access_token)


def print_all_repos(hostname: str, access_token: str) -> None:
    """Print all repos for the authenticated user"""
    # Github Enterprise with custom hostname
    g = Github(
        base_url="https://{hostname}/api/v3", login_or_token=access_token
    )
    for repo in g.get_user().get_repos():
        print(repo.name)


def fork_repository(
    username: str, repo_owner: str, repo_name: str, headers: dict[str, str]
) -> Optional[Dict[str, Any]]:
    fork_api_url = (
        f"https://api.github.com/repos/{repo_owner}/{repo_name}/forks"
    )
    fork_response = requests.post(fork_api_url, headers=headers)

    if fork_response.status_code == 202:
        print("Repository forked successfully.")
        return fork_response.json()
    else:
        print("Error forking the repository.")
        print("Status code:", fork_response.status_code)
        print("Error message:", fork_response.json())
        return None


def create_new_branch(
    username: str,
    repo_name: str,
    new_branch_name: str,
    headers: dict[str, str],
) -> None:
    api_base_url = f"https://api.github.com/repos/{username}/{repo_name}"
    branches_api_url = f"{api_base_url}/git/refs/heads"

    response = requests.get(branches_api_url, headers=headers)
    branches = response.json()

    main_branch_sha = None
    for branch in branches:
        if branch["ref"] == "refs/heads/main":
            main_branch_sha = branch["object"]["sha"]
            break

    if not main_branch_sha:
        print("Error: Couldn't find the main branch.")
        return

    new_branch_data = {
        "ref": f"refs/heads/{new_branch_name}",
        "sha": main_branch_sha,
    }

    response = requests.post(
        branches_api_url, headers=headers, json=new_branch_data
    )

    if response.status_code == 201:
        print(f"New branch '{new_branch_name}' created successfully.")
    else:
        print("Error creating the new branch.")
        print("Status code:", response.status_code)
        print("Error message:", response.json())


def commit_files_to_branch(
    username: str,
    repo_name: str,
    branch_name: str,
    devcontainer_json: str,
    docker_file: str,
    sample_script: str,
    headers: dict[str, str],
) -> None:
    # Encode file contents as Base64
    devcontainer_json_content: str = base64.b64encode(
        devcontainer_json.encode("utf-8")
    ).decode("utf-8")
    docker_file_content: str = base64.b64encode(
        docker_file.encode("utf-8")
    ).decode("utf-8")
    sample_script_content: str = base64.b64encode(
        sample_script.encode("utf-8")
    ).decode("utf-8")

    # Get the latest commit on the main branch
    api_base_url: str = f"https://api.github.com/repos/{username}/{repo_name}"
    latest_commit_response: Response = requests.get(
        f"{api_base_url}/git/ref/heads/main", headers=headers
    )
    latest_commit_sha = latest_commit_response.json()["object"]["sha"]

    # Get the tree of the latest commit
    latest_commit_tree_response: Response = requests.get(
        f"{api_base_url}/git/trees/{latest_commit_sha}", headers=headers
    )
    latest_commit_tree_sha = latest_commit_tree_response.json()["sha"]

    # Create a new tree with the new blobs
    new_tree_data: dict[str, Any] = {
        "base_tree": latest_commit_tree_sha,
        "tree": [
            {
                "path": ".devcontainer/devcontainer.json",
                "mode": "100644",
                "type": "blob",
                "content": devcontainer_json,
            },
            {
                "path": "Dockerfile",
                "mode": "100644",
                "type": "blob",
                "content": docker_file,
            },
            {
                "path": "sample_script.py",
                "mode": "100644",
                "type": "blob",
                "content": sample_script,
            },
        ],
    }
    new_tree_response: Response = requests.post(
        f"{api_base_url}/git/trees", headers=headers, json=new_tree_data
    )
    new_tree_sha = new_tree_response.json()["sha"]

    # Create a new commit
    new_commit_data: dict[str, Any] = {
        "message": "Add devcontainer files",
        "parents": [latest_commit_sha],
        "tree": new_tree_sha,
    }
    new_commit_response: Response = requests.post(
        f"{api_base_url}/git/commits", headers=headers, json=new_commit_data
    )
    new_commit_sha: Any = new_commit_response.json()["sha"]

    # Create the new branch with the new commit
    new_branch_data: dict[str, Any] = {
        "ref": f"refs/heads/{branch_name}",
        "sha": new_commit_sha,
    }
    _ = requests.post(
        f"{api_base_url}/git/refs", headers=headers, json=new_branch_data
    )


def create_codespace(
    username: str, repo_name: str, branch_name: str, headers: dict[str, str]
) -> str:
    api_base_url: LiteralString = f"https://api.github.com"

    # Set up the Codespace creation request
    codespace_data = {
        "repository": f"{username}/{repo_name}",
        "branch": branch_name,
    }

    # Send the Codespace creation request
    codespace_response = requests.post(
        f"{api_base_url}/user/codespaces", headers=headers, json=codespace_data
    )

    if codespace_response.status_code == 201:
        print(
            "Codespace creation request is successful. Waiting for the Codespace to be created..."
        )
        codespace_id: str = codespace_response.json()["id"]
    else:
        raise Exception(
            f"Error creating Codespace: {codespace_response.status_code} - {codespace_response.json()['message']}"
        )

    # Poll the Codespace status until it is ready
    codespace_status: str = "creating"
    while codespace_status != "ready":
        time.sleep(5)
        codespace_status_response = requests.get(
            f"{api_base_url}/codespaces/{codespace_id}", headers=headers
        )
        codespace_status = codespace_status_response.json()["state"]

    print(f"Codespace is ready. ID: {codespace_id}")
    return str(codespace_id)


def create_codespace_with_files(
    username: str,
    access_token: str,
    repo_url: str,
    docker_file: str,
    devcontainer_json: str,
    sample_script: str,
):
    # Extract repository owner and name from the repo URL
    repo_parts: list[str] = repo_url.split("/")
    repo_owner: str = repo_parts[-2]
    repo_name: str = repo_parts[-1].replace(".git", "")

    # Configure headers for the GitHub API
    headers: dict[str, str] = {
        "Authorization": f"token {access_token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
    }

    # Fork the repository
    forked_repo = fork_repository(username, repo_owner, repo_name, headers)
    print("Forked!")

    # Create a new branch in the forked repository
    new_branch_name: Literal["devcontainer-setup"] = "devcontainer-setup"

    # Commit devcontainer.json, Dockerfile, and sample_script to the new branch
    commit_files_to_branch(
        username=username,
        repo_name=repo_name,
        new_branch_name=new_branch_name,
        devcontainer_json=devcontainer_json,
        docker_file=docker_file,
        sample_script=sample_script,
        headers=headers,
    )
    print("Branch created and committed files")

    # Create a new Codespace using the new branch
    codespace_id = create_codespace(
        username, repo_name, new_branch_name, headers
    )
    print("Created Codespace ID: ", codespace_id)

    return codespace_id


if __name__ == "__main__":
    create_codespace_with_files(
        username=DEFAULT_USERNAME,
        access_token=DEFAULT_ACCESS_TOKEN,
        repo_url=DEFAULT_REPO_URL,
        docker_file=DEFAULT_DOCKERFILE,
        devcontainer_json=DEFAULT_DEVCONTAINER_JSON,
        sample_script=DEFAULT_SAMPLE_SCRIPT,
    )

