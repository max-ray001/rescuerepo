#!/usr/bin/env python
import os

DEFAULT_ACCESS_TOKEN = os.environ.get("GH_ACCESS_KEY")
DEFAULT_USERNAME = "matthew-mcateer"

# Default examples

DEFAULT_REPO_URL = "https://github.com/kkroening/ffmpeg-python"
DEFAULT_DOCKERFILE = """# Use the official Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install FFmpeg
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Clone the ffmpeg-python repository
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    git clone https://github.com/kkroening/ffmpeg-python.git /app/ffmpeg-python && \
    rm -rf /var/lib/apt/lists/*

# Install the required dependencies
RUN pip install --no-cache-dir -r /app/ffmpeg-python/requirements.txt

# Optional: Set the entrypoint for the container
ENTRYPOINT ["python"]
"""
DEFAULT_DEVCONTAINER_JSON = """{
    "name": "ffmpeg-python-dev-container",
    "dockerFile": "Dockerfile",
    "settings": {
        "terminal.integrated.shell.linux": "/bin/bash"
    },
    "extensions": [
        "ms-python.python"
    ],
    "forwardPorts": [],
    "postCreateCommand": "echo 'Welcome to your ffmpeg-python dev container!'"
}
"""

DEFAULT_SAMPLE_SCRIPT = """
import requests
import ffmpeg
import tempfile

# Download a video file from the internet
video_url = 'https://download.samplelib.com/mp4/sample-5s.mp4'

response = requests.get(video_url, stream=True)
response.raise_for_status()

# Save the video to a temporary file
with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video_file:
    for chunk in response.iter_content(chunk_size=8192):
        temp_video_file.write(chunk)
    temp_video_file.flush()

    # Process the video using ffmpeg-python
    input_video = ffmpeg.input(temp_video_file.name)
    output_video = input_video.filter('scale', 320, 240).output('output_video.mp4')
    output_video.run()

print("Video processing completed. The output video is saved as output_video.mp4.")
"""

# Nextflow-Flyte Conversion examples

NF_TO_FLYTE_REPO_URL = "https://github.com/AstroGlia-io/sequence_records"
NF_TO_FLYTE_DOCKERFILE = """# Use nextflow/nextflow:22.10.8 as a base image
FROM nextflow/nextflow:22.10.8

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    sudo \
    python3.9 \
    python3-pip

# Install flytekit and scikit-learn
RUN pip3 install flytekit scikit-learn

# Install Flyte
RUN curl -sL https://ctl.flyte.org/install | sudo bash -s -- -b /usr/local/bin

"""
NF_TO_FLYTE_DEVCONTAINER_JSON = """{
    "name": "nf-to-flyte-dev-container",
    "dockerFile": "Dockerfile",
    "settings": {
        "terminal.integrated.shell.linux": "/bin/bash"
    },
    "extensions": [
        "ms-python.python"
    ],
    "forwardPorts": [],
    "postCreateCommand": "echo 'Welcome to your nextflow-to-flyte dev container!'"
}
"""

NF_TO_FLYTE_SAMPLE_SCRIPT = """import subprocess
from flytekit import task, workflow

@task
def split_sequences(file_path: str) -> str:
    SPLIT = 'gcsplit' if System.properties['os.name'] == 'Mac OS X' else 'csplit'
    # file_path = "~/sample.fa" would normally be an input argument
    output_prefix = 'seq_'
    # run the csplit command, storing the outputs in files with names prefixed by 'seq_'
    subprocess.check_output(f"{SPLIT} {file_path} '%^>%' '/^>/' '{{*}}' -f {output_prefix}", shell=True)
    return output_prefix

@task
def reverse(input_prefix: str) -> str:
    # use a shell command to get a list of all files that match the prefix
    files = subprocess.check_output(f"ls {input_prefix}*", shell=True).decode().split('\n')
    reversed_sequences = []
    # iterate through each file
    for f in files:
        if f:  # skip empty names
            # reverse the content of each file and store the result
            reversed_sequences.append(subprocess.check_output(f"cat {f} | rev", shell=True).decode())
    return "\n".join(reversed_sequences)

@workflow
def reverse_workflow(file_path: str) -> str:
    prefix = split_sequences(file_path=file_path)
    return reverse(input_prefix=prefix)

"""



