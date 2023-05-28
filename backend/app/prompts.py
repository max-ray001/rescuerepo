#!/usr/bin/env python
from .defaults import DEFAULT_REPO_URL

PROMPT_DEVCONTAINER = f"""
Based on what you know about dev containers, here are some reference pages
https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/introduction-to-dev-containers
https://docs.github.com/en/codespaces/setting-up-your-project-for-codespaces/adding-a-dev-container-configuration/setting-up-your-python-project-for-codespaces.
Generate a devcontainer.json that uses the dockerfile you just generated
"""

def get_dockerfile_prompt(repo_url: str = DEFAULT_REPO_URL) -> str:
    prompt_dockerfile = f"""
Here is the repo url: {prompt_dockerfile}.
Based on contents of its README, generate an alpine based docker file with the library in that repo installed
"""
    return prompt_dockerfile

def get_sample_script_prompt(repo_url: str = DEFAULT_REPO_URL) -> str:
    prompt_sample_script = f"""
Using the repo you are working with, generate a cool python script that can be run inside the docker container you first generated using files accessible on the internet. 
"""
    return prompt_sample_script
