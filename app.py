#!/usr/bin/env python
from typing import Dict

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from backend.tasks import create_development_environment

app = FastAPI()

origins = [
    "*"  # You can set here your allowed origins, using "*" allows all origins.
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
    return FileResponse("frontend/build/index.html")


@app.post("/create-dev-environment")
async def create_dev_environment(request: Request) -> Dict[str, bool]:
    data = await request.json()
    
    githubRepoUrl = data.get("githubRepoUrl")
    email = data.get("email")
    access_token = data.get("githubAccessToken")

    if not (githubRepoUrl and email and access_token):
        raise HTTPException(status_code=400, detail="Missing required fields.")

    create_development_environment.delay(githubRepoUrl, email, access_token)

    return {"success": True}
