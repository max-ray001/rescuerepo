#!/usr/bin/env python
import base64
import json
import os
import random
import requests

from requests import Response
from typing import Any, Dict, Optional, Tuple

from github import Github

from defaults import (
    DEFAULT_ACCESS_TOKEN,
    DEFAULT_DEVCONTAINER_JSON,
    DEFAULT_DOCKERFILE,
    DEFAULT_REPO_URL,
    DEFAULT_SAMPLE_SCRIPT,
    DEFAULT_USERNAME,
)


class MissingCredentialsError(Exception):
    """Exception raised for errors in setting credentials."""

    def __init__(
        self,
        message="An error occurred when obtaining credentials or access keys",
    ):
        self.message = message
        super().__init__(self.message)


class RepoForkError(Exception):
    """Exception raised for errors in the forking process."""

    def __init__(self, message="An error occurred when forking a GitHub Repo"):
        self.message = message
        super().__init__(self.message)


class BranchCreationError(Exception):
    """Exception raised for errors in the branch creation process."""

    def __init__(
        self, message="An error occurred when creating a branch of a repo"
    ):
        self.message = message
        super().__init__(self.message)


class CommitToBranchError(Exception):
    """Exception raised for errors in the commit creation process."""

    def __init__(
        self, message="An error occurred when creating a commit of a branch"
    ):
        self.message = message
        super().__init__(self.message)


class CodeSpaceCreationError(Exception):
    """Exception raised for errors in the codespace creation process."""

    def __init__(
        self, message="An error occurred when creating a GitHub codespace"
    ):
        self.message = message
        super().__init__(self.message)


def check_if_repo_exists(
    repo_owner: str, repo_name: str, headers: dict[str, str]
) -> bool:
    """Check if a repo exists via GET request to GitHub API."""
    repositories_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    repo_response = requests.get(repositories_url, headers=headers)

    # print the response body
    if repo_response.status_code == 200:
        print("Repo exists!!")
        return True
    else:
        if repo_response.status_code == 301:
            print(
                f"Error 301: Repository {repo_owner}/{repo_name} moved permenantly\n",
                repo_response.json(),
            )
        elif repo_response.status_code == 401:
            raise RepoForkError(
                "Error 401: Bad Credentials\n"
                + str(repo_response.json())
                + "\n"
                + str(headers)
            )
        elif repo_response.status_code == 403:
            print(
                f"Error 403: Repository {repo_owner}/{repo_name} not found. Forbidden\n",
                repo_response.json(),
            )
        elif repo_response.status_code == 404:
            print(
                f"Repository with name {repo_owner}/{repo_name} doesn't exist yet."
            )
        else:
            print(
                f"Unknown error checking repository {repo_owner}/{repo_name}\n"
                + str(repo_response.json())
            )
    return False


def fork_repository(
    username: str, repo_owner: str, repo_name: str, headers: dict[str, str]
) -> Tuple[int, Dict[str, Any]]:
    """Fork a repository using the GitHub API."""
    fork_api_url = (
        f"https://api.github.com/repos/{repo_owner}/{repo_name}/forks"
    )
    fork_response = requests.post(fork_api_url, headers=headers)
    # Define the required parameters
    fork_data = {"name": repo_name, "default_branch_only": True}
    # Send the POST request
    fork_response = requests.post(
        fork_api_url, headers=headers, data=json.dumps(fork_data)
    )
    if fork_response.status_code == 202:
        print("Repository forked successfully.")
    else:
        if fork_response.status_code == 403:
            print("Error forking the repository. Bad Request")
        elif fork_response.status_code == 404:
            print("Error forking the repository. Resource not found")
        elif fork_response.status_code == 422:
            print(
                "Error forking the repository. Validation failed, or the endpoint has been spammed."
            )
        else:
            print("Error forking the repository.")

        print("Status code:", fork_response.status_code)
        print("Error message:", fork_response.json())
    return int(fork_response.status_code), fork_response.json()


def create_new_branch(
    username: str,
    repo_name: str,
    new_branch_name: str,
    headers: dict[str, str],
) -> None:
    api_base_url: str = f"https://api.github.com/repos/{username}/{repo_name}"
    branches_api_url: str = f"{api_base_url}/git/refs/heads"

    branches_response: Response = requests.get(
        branches_api_url, headers=headers
    )
    branches = branches_response.json()

    main_branch_sha = None
    for branch in branches:
        if branch["ref"] == "refs/heads/main":
            main_branch_sha = branch["object"]["sha"]
            break

    if not main_branch_sha:
        print("Error: Couldn't find the main branch.")
        return

    new_branch_data: dict[str, Any] = {
        "ref": f"refs/heads/{new_branch_name}",
        "sha": main_branch_sha,
    }

    new_branch_response: Response = requests.post(
        branches_api_url, headers=headers, json=new_branch_data
    )

    if new_branch_response.status_code == 201:
        print(f"New branch '{new_branch_name}' created successfully.")
    else:
        print("Error creating the new branch.")
        print("Status code:", new_branch_response.status_code)
        print("Error message:", new_branch_response.json())


def commit_files_to_branch(
    repo_owner: str,
    repo_name: str,
    new_branch_name: str,
    devcontainer_json_content: str,
    dockerfile_content: str,
    sample_script_content: str,
    headers: dict[str, str],
) -> None:
    api_base_url: str = (
        f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    )

    # Get default branch and its commit SHA
    repo_info = requests.get(api_base_url, headers=headers).json()
    print(repo_info)
    default_branch = repo_info["default_branch"]
    default_branch_sha = requests.get(
        f"{api_base_url}/git/ref/heads/master", headers=headers
    ).json()["object"]["sha"]

    devcontainer_json_blob_sha = requests.post(
        f"{api_base_url}/git/blobs",
        headers=headers,
        json={
            "content": base64.b64encode(
                devcontainer_json_content.encode()
            ).decode(),
            "encoding": "base64",
        },
    ).json()["sha"]

    dockerfile_blob_sha = requests.post(
        f"{api_base_url}/git/blobs",
        headers=headers,
        json={
            "content": base64.b64encode(dockerfile_content.encode()).decode(),
            "encoding": "base64",
        },
    ).json()["sha"]

    sample_script_blob_sha = requests.post(
        f"{api_base_url}/git/blobs",
        headers=headers,
        json={
            "content": base64.b64encode(
                sample_script_content.encode()
            ).decode(),
            "encoding": "base64",
        },
    ).json()["sha"]

    # Get latest commit tree
    latest_commit_tree_sha = requests.get(
        f"{api_base_url}/git/commits/{default_branch_sha}", headers=headers
    ).json()["tree"]["sha"]
    print("Latest commit tree SHA:", latest_commit_tree_sha)

    # Create a new tree with the new blobs
    new_tree_response = requests.post(
        f"{api_base_url}/git/trees",
        headers=headers,
        json={
            "base_tree": latest_commit_tree_sha,
            "tree": [
                {
                    "path": ".devcontainer/devcontainer.json",
                    "mode": "100644",
                    "type": "blob",
                    "sha": devcontainer_json_blob_sha,
                },
                {
                    "path": ".devcontainer/Dockerfile",
                    "mode": "100644",
                    "type": "blob",
                    "sha": dockerfile_blob_sha,
                },
                {
                    "path": "sample_script.py",
                    "mode": "100644",
                    "type": "blob",
                    "sha": sample_script_blob_sha,
                },
            ],
        },
    )

    if new_tree_response.status_code == 201:
        new_tree = new_tree_response.json()
        print("New tree created successfully.")
        print("New tree SHA:", new_tree["sha"])
    else:
        print("Error creating the new tree.")
        print("Status code:", new_tree_response.status_code)
        print("Error message:", new_tree_response.json())
        exit(1)

    # Create a new commit with the new tree
    new_commit_response = requests.post(
        f"{api_base_url}/git/commits",
        headers=headers,
        json={
            "message": "Add devcontainer.json and Dockerfile",
            "tree": new_tree["sha"],
            "parents": [default_branch_sha],
        },
    )

    if new_commit_response.status_code == 201:
        new_commit = new_commit_response.json()
        print("New commit created successfully.")
        print("New commit SHA:", new_commit["sha"])
    else:
        print("Error creating the new commit.")
        print("Status code:", new_commit_response.status_code)
        print("Error message:", new_commit_response.json())
        exit(1)

    # Create new branch on the forked repository with the new commit SHA
    new_branch_ref = f"refs/heads/{new_branch_name}"
    create_branch_response = requests.post(
        f"{api_base_url}/git/refs",
        headers=headers,
        json={"ref": new_branch_ref, "sha": new_commit["sha"]},
    )

    if create_branch_response.status_code == 201:
        print(
            f"New branch '{new_branch_name}' created successfully on the forked repository with devcontainer.json and Dockerfile."
        )
    else:
        print("Error creating the new branch on the forked repository.")
        print("Status code:", create_branch_response.status_code)
        print("Error message:", create_branch_response.json())
        exit(1)


def create_new_github_codespace(
    repo_owner: str,
    repo_name: str,
    new_branch_name: str,
    headers: dict[str, str],
) -> str:
    api_base_url: str = (
        f"https://api.github.com/repos/{repo_owner}/{repo_name}/codespaces"
    )

    create_codespace_payload = {"ref": new_branch_name}

    create_codespace_response = requests.post(
        api_base_url, headers=headers, json=create_codespace_payload
    )

    if create_codespace_response.status_code == 201:
        print("Codespace creation request is successful.")
        print("Waiting for the Codespace to be created...")
        codespace = create_codespace_response.json()

        # Poll the Codespace's status until it becomes 'available'
        codespace_id = codespace["id"]
        print("GitHub Codespace ID: ", codespace_id)
        print("GitHub Codespace info:\n")
        print(json.dumps(codespace, indent=4))

        codespace_status = codespace["state"]
        print("Codespace Status: ", codespace_status)
        return codespace_id
        # while codespace_status != 'Available':
        #    time.sleep(10)
        #    codespace_response = requests.get(f'{api_base_url}/{codespace_id}', headers=headers)
        #    codespace = codespace_response.json()
        #    import ipdb
        #    ipdb.set_trace()
        #    codespace_status = codespace['state']
        #    print(f"Current Codespace status: {codespace_status}")
        #
        # print(f"Codespace is available! ID: {codespace_id}")

    else:
        print("Error creating the Codespace.")
        print("Status code:", create_codespace_response.status_code)
        print("Error message:", create_codespace_response.json())


def create_codespace_with_files(
    username: str,
    access_token: str,
    repo_url: str,
    docker_file: str,
    devcontainer_json: str,
    sample_script: str,
) -> str:
    # Extract repository owner and name from the repo URL
    repo_parts = repo_url.split("/")
    print("repo_parts", repo_parts)
    repo_owner = repo_parts[-2]
    print("repo_owner", repo_owner)
    repo_name = repo_parts[-1].replace(".git", "")
    print("repo_name", repo_name)

    # check that access token has been set
    if not access_token:
        print("access_token is None")
        access_token = os.environ.get("GH_ACCESS_KEY")
        if not access_token:
            raise MissingCredentialsError(
                "access_token is None and 'GH_ACCESS_KEY' environment variable not set."
            )

    # Configure headers for the GitHub API
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {access_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    try:
        # Check if the repo we're trying to fork exists
        origin_repo_exists = check_if_repo_exists(
            repo_owner=repo_owner, repo_name=repo_name, headers=headers
        )
        # Check that we haven't already created a fork with the same name as the original
        new_repo_exists = check_if_repo_exists(
            repo_owner=username, repo_name=repo_name, headers=headers
        )
    except RepoForkError as e:
        print(e)
        raise e

    if (not new_repo_exists) and origin_repo_exists:
        # Fork the repository
        response_code, forked_repo = fork_repository(
            username=username,
            repo_owner=repo_owner,
            repo_name=repo_name,
            headers=headers,
        )
        print(forked_repo)
        if response_code == 202:
            print("Forked! Fork now available at ", forked_repo["html_url"])
        else:
            if (
                forked_repo["message"]
                == "Resource not accessible by personal access token"
            ):
                print("You do not have permissions to fork this repository.")
                print(
                    "GitHub returned the following error message: ",
                    forked_repo,
                )
            else:
                print("Error forking the repository.")
                print(
                    f"GitHub returned an error code {response_code} error message: ",
                    forked_repo["message"],
                )
            raise RepoForkError(
                f"Error forking the repository {repo_name}.\nResponse code {response_code}.\nerror message: "
                + str(forked_repo["message"]),
            )

    else:
        print(f"Repository with the name {repo_name} already exists.")

    # Create a new branch in the forked repository
    new_branch_name = "devcontainer-setup-" + str(random.randint(1, 1000))
    try:
        create_new_branch(
            username=username,
            repo_name=repo_name,
            new_branch_name=new_branch_name,
            headers=headers,
        )
    except BranchCreationError as e:
        print(e)
        raise BranchCreationError(
            f"Error creating the new branch {new_branch_name} in the repository {repo_name}."
        )

    # Commit devcontainer.json, Dockerfile, and sample_script to the new branch
    try:
        commit_files_to_branch(
            repo_owner=username,
            repo_name=repo_name,
            new_branch_name=new_branch_name,
            devcontainer_json_content=devcontainer_json,
            dockerfile_content=docker_file,
            sample_script_content=sample_script,
            headers=headers,
        )
    except CommitToBranchError as e:
        print(e)
        raise CommitToBranchError(
            f"Error committing files to the branch {new_branch_name} in the repository {repo_name}."
        )
    print("Branch created and committed files")

    # Create a new Codespace using the new branch
    try:
        codespace_id = create_new_github_codespace(
            repo_owner=username,
            repo_name=repo_name,
            new_branch_name=new_branch_name,
            headers=headers,
        )
    except CodeSpaceCreationError as e:
        print(e)
        raise CodeSpaceCreationError(
            f"Error creating the Codespace for the branch {new_branch_name} in the repository {repo_name}."
        )

    return codespace_id


if __name__ == "__main__":
    try:
        create_codespace_with_files(
            username=DEFAULT_USERNAME,
            access_token=DEFAULT_ACCESS_TOKEN,
            repo_url=DEFAULT_REPO_URL,
            docker_file=DEFAULT_DOCKERFILE,
            devcontainer_json=DEFAULT_DEVCONTAINER_JSON,
            sample_script=DEFAULT_SAMPLE_SCRIPT,
        )
    except MissingCredentialsError as e:
        print(e)
        exit(1)
    except RepoForkError as e:
        print(e)
        exit(1)
    except BranchCreationError as e:
        print(e)
        exit(1)
    except CommitToBranchError as e:
        print(e)
        exit(1)
    except CodeSpaceCreationError as e:
        print(e)
        exit(1)

