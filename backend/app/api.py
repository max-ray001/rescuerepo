#!/usr/bin/env python
from typing import Dict

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from .tasks import create_development_environment, create_dev_environment_task

USE_TASK_QUEUE = False

app = FastAPI(
    title="backend",
    description="Backend API for the Dev Environments project.",
    version="0.0.1",
    docs_url="/documentation",
    redoc_url="/redocumentation",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

origins = [
    "*"  # You can set here your allowed origins, using "*" allows all origins.
    #"http://localhost:3000",
    #"localhost:3000"
]

# Allow all for now, you can fine-tune this later.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index() -> FileResponse:
    import os
    # get the current working directory
    current_working_directory = os.getcwd()
    # print output to the console
    logger.trace(f"Current working directory: {current_working_directory}")

    return FileResponse("../frontend/build/index.html")

#async def healthz() -> Dict[str, str]:
#    # Return a 200 response to indicate that the application is healthy.
#    return {"status": "ok"}


@app.post("/create-dev-environment")
async def create_dev_environment(request: Request) -> Dict[str, bool]:
    data = await request.json()

    logger.trace(f"Data: {data}")
    
    githubRepoUrl = data.get("githubRepoUrl")
    email = data.get("email")
    access_token = data.get("githubAccessToken")

    logger.debug(f"GitHub Repo URL: {githubRepoUrl}", )
    logger.debug(f"email: {email}")

    if not (githubRepoUrl and email and access_token):
        raise HTTPException(status_code=400, detail="Missing required fields.")
    
    if USE_TASK_QUEUE==True:
        create_dev_environment_task.delay(
            github_repo_url=githubRepoUrl,
            user_email=email,
            github_access_token=access_token,
            username="matthew-mcateer",
            send_email=True
        )
    else:
        create_development_environment(
            github_repo_url=githubRepoUrl,
            user_email=email,
            github_access_token=access_token,
            username="matthew-mcateer",
            send_email=False,
        )

    return {"success": True}
