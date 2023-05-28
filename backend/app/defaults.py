#!/usr/bin/env python
import os

DEFAULT_ACCESS_TOKEN = os.environ.get("GH_TOKEN")
DEFAULT_USERNAME = "matthew-mcateer"
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

