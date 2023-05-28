#!/usr/bin/env python
import os
from typing import Any

import postmark

from celery import Celery
from celery.utils.log import get_task_logger

from backend.gh_client_clean import create_codespace_with_files
from backend.defaults import (
    DEFAULT_DOCKERFILE,
    DEFAULT_DEVCONTAINER_JSON,
    DEFAULT_SAMPLE_SCRIPT,
)


from llms.llm_utils import authenticate_openai, get_code_block_openai
from llms.prompts import (
    PROMPT_DEVCONTAINER,
    get_dockerfile_prompt,
    get_sample_script_prompt,
)

app = Celery("tasks", broker=os.getenv("CELERY_BROKER_URL"))
logger = get_task_logger(__name__)

authenticate_openai(os.environ["OPENAI_API_KEY"])


def send_postmark_email(email: str, github_url: str) -> bool:
    """This function sends a welcome email to the user"""
    try:
        postmark_api_key = os.environ["POSTMARK_API_KEY"]
    except KeyError:
        print("POSTMARK_API_KEY environment variable not set")
        return False
    client = postmark.Client(api_token=postmark_api_key)
    message = postmark.Message(
        sender="sender@example.com",
        to=email,
        subject="Your development environment is ready!",
        text_body=f"Your codespace is ready! You can access it here: {github_url}",
    )
    try:
        client.send(message)
        return True
    except postmark.exceptions.PostmarkException as e:
        print("Error sending email:", e.message)
        return False


@app.task
def create_development_environment(
    github_repo_url: str,
    github_access_token: str,
    user_email: str,
    test_mode: bool = True,
) -> str:
    logger.info("Creating development environment")

    # Get dockerfile
    if test_mode == False:
        prompt_dockerfile = get_dockerfile_prompt(github_repo_url)
        dockerfile_string = get_code_block_openai(prompt_dockerfile)
    else:
        dockerfile_string = DEFAULT_DOCKERFILE
    # Get devcontainer.json
    if test_mode == False:
        devcontainer_string = get_code_block_openai(PROMPT_DEVCONTAINER)
    else:
        devcontainer_string = DEFAULT_DEVCONTAINER_JSON

    # Get sample script
    if test_mode == False:
        prompt_sample_script = get_sample_script_prompt(PROMPT_DEVCONTAINER)
        sample_script_string = get_code_block_openai(prompt_sample_script)
    else:
        sample_script_string = DEFAULT_SAMPLE_SCRIPT

    # Fork a repo and create codespace on top of that
    print(sample_script_string)

    # Add a function to send an email
    create_codespace_with_files(
        username="matthew-mcateer",
        access_token=os.environ["GH_ACCESS_TOKEN"],
        repo_url=github_repo_url,
        docker_file=dockerfile_string,
        devcontainer_json=devcontainer_string,
        sample_script=sample_script_string,
    )
    return "Development environment created"


@app.task
def add(x: Any, y: Any) -> Any:
    logger.info(f"Adding {x} + {y}")
    return x + y
