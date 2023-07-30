#!/usr/bin/env python
import os
import sys
from typing import Dict

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from .tasks import create_development_environment, create_dev_environment_task

filepaths = ['api/.env', '.env']
USE_TASK_QUEUE = False

found_path = False
for filepath in filepaths:
    if os.path.exists(filepath):
        load_dotenv(filepath)
        found_path = True
        logger.info(f"Loaded dotenv file: {filepath}")
        break

if not found_path:
    load_dotenv()
    logger.debug("Loaded default dotenv file.")


load_dotenv()

app = FastAPI(
    title="rescuerepo-api",
    description="Backend API for RescueRepo.",
    version="0.0.1",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# You can set here your allowed origins.
# Using "*" allows all origins (not recommended in production)
origins = [
    "http://localhost:3000",
]

# Allow all for now, you can fine-tune this later.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/python")
def hello_world():
    # Get and print the python version
    return {"message": f"Hello World, Python version: {sys.version}"}


@app.get("/api/healthchecker")
def healthchecker():
    return {"status": "success", "message": "Integrate FastAPI Framework with Next.js"}


@app.post("/api/create-dev-environment")
async def create_dev_environment(request: Request) -> Dict[str, bool]:
    data = await request.json()

    logger.debug(f"Data: {data}")
    
    input_username = data.get("githubUsername") 
    github_repo_url = data.get("githubRepoUrl")
    email = data.get("email")
    access_token = data.get("githubAccessToken")

    logger.debug(f"GitHub Repo URL: {github_repo_url}")
    logger.debug(f"GitHub Username: {github_repo_url}")
    logger.debug(f"email: {email}")

    if not (github_repo_url and email and access_token and input_username):
        raise HTTPException(status_code=400, detail="Missing required fields.")
    
    if USE_TASK_QUEUE==True:
        create_dev_environment_task.delay(
            github_repo_url=github_repo_url,
            user_email=email,
            github_access_token=access_token,
            username=input_username,
            send_email=True
        )
    else:
        create_development_environment(
            github_repo_url=github_repo_url,
            user_email=email,
            github_access_token=access_token,
            username=input_username,
            send_email=False,
        )

    return {"success": True}
