#!/usr/bin/env python
import base64
import os

import postmark

from celery import Celery
from celery.utils.log import get_task_logger
from loguru import logger

from .gh_client import (
    create_codespace_with_files,
    MissingCredentialsError,
    RepoForkError,
    BranchCreationError,
    CommitToBranchError,
    CodeSpaceCreationError,
)
from .few_shot_examples import (
    DEFAULT_ACCESS_TOKEN,
    DEFAULT_DEVCONTAINER_JSON_FEW_SHOT_EXAMPLE,
    DEFAULT_DOCKERFILE_FEW_SHOT_EXAMPLE,
    DEFAULT_REPO_URL_FEW_SHOT_EXAMPLE,
    DEFAULT_SAMPLE_SCRIPT_FEW_SHOT_EXAMPLE,
    NF_TO_FLYTE_DEVCONTAINER_JSON_FEW_SHOT_EXAMPLE,
    NF_TO_FLYTE_DOCKERFILE_FEW_SHOT_EXAMPLE,
    NF_TO_FLYTE_REPO_URL_FEW_SHOT_EXAMPLE,
    NF_TO_FLYTE_SAMPLE_SCRIPT_FEW_SHOT_EXAMPLE,
    LUCIDRAINS_PROGEN_DEVCONTAINER_JSON_FEW_SHOT_EXAMPLE,
    LUCIDRAINS_PROGEN_DOCKERFILE_FEW_SHOT_EXAMPLE,
    LUCIDRAINS_PROGEN_REPO_URL_FEW_SHOT_EXAMPLE,
    LUCIDRAINS_PROGEN_SAMPLE_SCRIPT_FEW_SHOT_EXAMPLE,
)


from .llm_utils import authenticate_openai, get_code_block_openai
from .prompts import (
    PROMPT_DEVCONTAINER,
    get_dockerfile_prompt,
    get_sample_script_prompt,
)

# Try getting the environment variable `CELERY_BROKER_URL` to configure broker url
# and if it doesn't exist, set it to the default value
broker = os.environ["CELERY_BROKER_URL"]

# set broker_pool_limit to 1 to prevent connection errors
# celery_app.conf.broker_pool_limit = 1
# celery_app.conf.broker_connection_max_retries = 50
os.environ.setdefault("BROKER_POOL_LIMIT", "1")

celery_app = Celery(
    "tasks",
    broker=os.environ["CELERY_BROKER_URL"],
)

celery_logger = get_task_logger(__name__)

authenticate_openai(os.environ["OPENAI_API_KEY"])

def send_postmark_email(email: str, github_url: str) -> bool:
    """This function sends a welcome email to the user"""
    try:
        postmark_api_key = os.environ["POSTMARK_API_KEY"]
    except KeyError:
        logger.error(
            "POSTMARK_API_KEY environment variable not set, and default key is expired."
        )
        return False
    client = postmark.Client(api_token=postmark_api_key)
    message = postmark.Message(
        sender="example@example.com",
        to=email,
        subject="Your development environment is ready!",
        text_body=f"Your codespace of your fork of {github_url} is ready!\n\nYou can access it here https://github.com/codespaces",
    )
    try:
        client.send(message)
        return True
    except postmark.exceptions.PostmarkException as e:
        logger.error(f"Error sending email: {e.message}")
        return False


def get_environment_details(github_repo_url):
    few_shot_examples = {
        DEFAULT_REPO_URL_FEW_SHOT_EXAMPLE: {
            "repo_url": DEFAULT_REPO_URL_FEW_SHOT_EXAMPLE,
            "docker_file": DEFAULT_DOCKERFILE_FEW_SHOT_EXAMPLE,
            "devcontainer_json": DEFAULT_DEVCONTAINER_JSON_FEW_SHOT_EXAMPLE,
            "sample_script": DEFAULT_SAMPLE_SCRIPT_FEW_SHOT_EXAMPLE,
        },
        NF_TO_FLYTE_REPO_URL_FEW_SHOT_EXAMPLE: {
            "repo_url": NF_TO_FLYTE_REPO_URL_FEW_SHOT_EXAMPLE,
            "docker_file": NF_TO_FLYTE_DOCKERFILE_FEW_SHOT_EXAMPLE,
            "devcontainer_json": NF_TO_FLYTE_DEVCONTAINER_JSON_FEW_SHOT_EXAMPLE,
            "sample_script": NF_TO_FLYTE_SAMPLE_SCRIPT_FEW_SHOT_EXAMPLE,
        },
        LUCIDRAINS_PROGEN_REPO_URL_FEW_SHOT_EXAMPLE: {
            "repo_url": LUCIDRAINS_PROGEN_REPO_URL_FEW_SHOT_EXAMPLE,
            "docker_file": LUCIDRAINS_PROGEN_DOCKERFILE_FEW_SHOT_EXAMPLE,
            "devcontainer_json": LUCIDRAINS_PROGEN_DEVCONTAINER_JSON_FEW_SHOT_EXAMPLE,
            "sample_script": LUCIDRAINS_PROGEN_SAMPLE_SCRIPT_FEW_SHOT_EXAMPLE,
        },
    }

    return few_shot_examples.get(github_repo_url, {})


def create_development_environment(
    github_repo_url: str,
    user_email: str,
    github_access_token: str = os.environ.get("GH_ACCESS_TOKEN", ""),
    username: str = "matthew-mcateer",
    send_email: bool = False,
) -> str:
    logger.info("Creating development environment")

    if github_repo_url == "":
        return "Error: No repo url provided"
    if github_access_token == "":
        return "Error: No access token provided"
    if user_email == "":
        return "Error: No email provided"

    environment_details = get_environment_details(github_repo_url)

    if github_access_token != DEFAULT_ACCESS_TOKEN:
        github_access_token = DEFAULT_ACCESS_TOKEN

    logger.debug(f"Username: {username}")
    logger.trace(f"Github access token: {github_access_token}")
    logger.debug(f"Github repo url: {github_repo_url}")
    logger.trace(f"Environment details: {environment_details}")

    if environment_details:
        try:
            create_codespace_with_files(
                username=username,
                access_token=github_access_token,
                **environment_details,
            )
        except (
            MissingCredentialsError,
            RepoForkError,
            BranchCreationError,
            CommitToBranchError,
            CodeSpaceCreationError,
        ) as e:
            logger.error(f"{e}")
            return f"Error: {e}"
    else:
        return handle_other_cases(
            github_repo_url,
            username,
            github_access_token,
        )

    if send_email == True:
        send_postmark_email(email=user_email, github_url=github_repo_url)
    return "Development environment created"


def handle_other_cases(github_repo_url, username, github_access_token):
    # Get dockerfile
    prompt_dockerfile = get_dockerfile_prompt(github_repo_url)
    dockerfile_string = get_code_block_openai(prompt_dockerfile)
    if dockerfile_string == "":
        return "Error: No dockerfile found"

    # Get devcontainer.json
    devcontainer_string = get_code_block_openai(PROMPT_DEVCONTAINER)
    if devcontainer_string == "":
        return "Error: No devcontainer.json found"

    # Get sample script
    prompt_sample_script = get_sample_script_prompt(PROMPT_DEVCONTAINER)
    sample_script_string = get_code_block_openai(prompt_sample_script)
    if sample_script_string == "":
        return "Error: No sample script found"

    # Fork a repo and create codespace on top of that
    logger.trace(f"Sample script string: \n{sample_script_string}")
    try:
        create_codespace_with_files(
            username=username,
            access_token=github_access_token,
            repo_url=github_repo_url,
            docker_file=dockerfile_string,
            devcontainer_json=devcontainer_string,
            sample_script=sample_script_string,
        )
    except (
        MissingCredentialsError,
        RepoForkError,
        BranchCreationError,
        CommitToBranchError,
        CodeSpaceCreationError,
    ) as e:
        logger.error(f"{e}")
        return f"Error: {e}"

    return ""


@celery_app.task
def create_dev_environment_task(
    github_repo_url: str,
    user_email: str,
    github_access_token: str,
    username: str = "matthew-mcateer",
    send_email: bool = False,
) -> str:
    return create_development_environment(
        github_repo_url=github_repo_url,
        user_email=user_email,
        github_access_token=github_access_token,
        username=username,
        send_email=send_email,
    )
