#!/usr/bin/env python
import os
import re

from loguru import logger
from typing import List, Optional

import openai


def authenticate_openai(openai_api_key: str) -> None:
    openai.api_key = openai_api_key


def list_openai_engines() -> Optional[List[dict]]:
    # Ensure the user is authenticated
    if not openai.api_key:
        raise ValueError(
            "OpenAI API key not set. Please authenticate using 'authenticate_openai(api_key)' function."
        )

    try:
        response = openai.Engine.list()
        engines = response["data"]
        return engines
    except openai.error.APIError as api_error:
        logger.error(f"API error: {api_error}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None


def extract_code_blocks_from_chatgpt_output(text: str) -> List[str]:
    code_blocks = re.findall(r"```([\s\S]*?)```", text)
    code_blocks = [code_block.strip() for code_block in code_blocks]
    return code_blocks


def get_code_block_openai(
    prompt: str, model: str = "gpt-3.5-turbo-0301"
) -> str:
    # Ensure the user is authenticated
    if not openai.api_key:
        raise ValueError(
            "OpenAI API key not set. Please authenticate using 'authenticate_openai(api_key)' function."
        )

    # Set up the API request
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 150,
        "n": 1,
        "stop": None,
        "temperature": 1.0,
    }

    try:
        logger.info(f"Sending request to OpenAI API")
        logger.debug(f"Using the following parameters:")
        logger.debug(f"  Model: {model}")
        logger.debug(f"  Prompt: {prompt}")

        # Make the API request
        response = openai.ChatCompletion.create(**data)

        # Check if there are choices in the response
        if not response.choices:
            logger.error(
                "Error: The API response does not contain any generated text."
            )
            return None

        logger.trace(response)
        logger.trace(response.choices[0].message.content)
        generated_text = response.choices[0].message.content.strip()
        logger.success("Generated text successfully received.")

        code_blocks = extract_code_blocks_from_chatgpt_output(generated_text)
        if len(code_blocks) > 0:
            return code_blocks[0]
        else:
            return generated_text

    except openai.error.APIError as api_error:
        logger.error(f"API error: {api_error}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None


if __name__ == "__main__":
    authenticate_openai(os.environ["OPENAI_API_TOKEN"])
    logger.debug(list_openai_engines())
    logger.debug(
        get_code_block_openai(
            "Generate a sample python code that adds two numbers"
        )
    )
