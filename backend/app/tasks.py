#!/usr/bin/env python
import base64
import os
from typing import Any

import postmark

from celery import Celery
from celery.utils.log import get_task_logger
from loguru import logger

from .gh_client_clean import (
    create_codespace_with_files,
    MissingCredentialsError,
    RepoForkError,
    BranchCreationError,
    CommitToBranchError,
    CodeSpaceCreationError,
)
from .few_shot_examples import (
    DEFAULT_DOCKERFILE,
    DEFAULT_DEVCONTAINER_JSON,
    DEFAULT_SAMPLE_SCRIPT,
)


from .llm_utils import authenticate_openai, get_code_block_openai
from .prompts import (
    PROMPT_DEVCONTAINER,
    get_dockerfile_prompt,
    get_sample_script_prompt,
)

DEFAULT_RABBITMQ_BROKER = base64.b64decode(
    "YW1xcHM6Ly9sc2x2aXhidDpjVjlBYlB3YXcyQTIyd2E5NXBFRm53c05QQUxMSTV6d0BjaGltcGFuemVlLnJtcS5jbG91ZGFtcXAuY29tL2xzbHZpeGJ0"
).decode("utf-8")

# Try getting the environment variable `CELERY_BROKER_URL` to configure broker url
# and if it doesn't exist, set it to the default value
try:
    broker = os.environ["CELERY_BROKER_URL"]
except KeyError:
    broker = DEFAULT_RABBITMQ_BROKER
    os.environ.setdefault("CELERY_BROKER_URL", DEFAULT_RABBITMQ_BROKER)

#os.environ.setdefault("BROKER_POOL_LIMIT", "1")

#celery_app = Celery(
#    "tasks",
#    broker=os.environ.get("CELERY_BROKER_URL", DEFAULT_RABBITMQ_BROKER),
#)

# set broker_pool_limit to 1 to prevent connection errors
#celery_app.conf.broker_pool_limit = 1
#celery_app.conf.broker_connection_max_retries = 50

#celery_logger = get_task_logger(__name__)

authenticate_openai(os.environ["OPENAI_API_KEY"])


def send_postmark_email(email: str, github_url: str) -> bool:
    """This function sends a welcome email to the user"""
    try:
        postmark_api_key = os.environ.get(
            "POSTMARK_API_KEY",
            base64.b64decode(
                "ODExMTEwZmEtZjQyNy00M2M2LWJiZDctYTM0NDcwY2UxYjI5"
            ).decode("utf-8"),
        )
    except KeyError:
        print("POSTMARK_API_KEY environment variable not set. ")
        return False
    client = postmark.Client(api_token=postmark_api_key)
    message = postmark.Message(
        sender="matthew@astroglia.io",
        to=email,
        subject="Your development environment is ready!",
        text_body=f"Your codespace of your fork of {github_url} is ready!\n\nYou can access it here https://github.com/codespaces",
    )
    try:
        client.send(message)
        return True
    except postmark.exceptions.PostmarkException as e:
        print("Error sending email:", e.message)
        return False


#@celery_app.task
def create_development_environment(
    github_repo_url: str,
    user_email: str,
    github_access_token: str,
    username: str = "matthew-mcateer",
    test_mode: bool = True,
    send_email: bool = False,
) -> str:
    logger.info("Creating development environment")

    # Get user
    if test_mode == False:
        username = username
    else:
        username = "matthew-mcateer"

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
    try:
        #TODO: Delete this line to enable getting the token directly from the user
        github_access_token = os.environ["GH_ACCESS_TOKEN"]
        create_codespace_with_files(
            username=username,
            access_token=github_access_token,
            repo_url=github_repo_url,
            docker_file=dockerfile_string,
            devcontainer_json=devcontainer_string,
            sample_script=sample_script_string,
        )
    except MissingCredentialsError as e:
        print(e)
        return "Error obtaining credentials. Full error message: " + str(e)
    except RepoForkError as e:
        print(e)
        return "Error forking repo. Full error message: " + str(e)
    except BranchCreationError as e:
        print(e)
        return (
            "Successfully forked repo, but error creating a new branch in the repo. Full error message: "
            + str(e)
        )
    except CommitToBranchError as e:
        print(e)
        return (
            "Forked repo, created new branch, but error committing files to branch. Full error message: "
            + str(e)
        )
    except CodeSpaceCreationError as e:
        print(e)
        return (
            "Forked repo, created new branch, comitted files, but error creating new CodeSpace. Full error message: "
            + str(e)
        )
    if send_email==True:
        send_postmark_email(email=user_email, github_url=github_repo_url)
    return "Development environment created"

