#!/usr/bin/env python
from requests import Response

from flask import Flask, send_from_directory, request
from flask_cors import CORS, cross_origin

from backend.tasks import create_development_environment

app = Flask(__name__, static_url_path="", static_folder="frontend/build")
CORS(app)


@app.route("/")
def index() -> Response:
    return send_from_directory(app.static_folder, "index.html")


@app.route("/create-dev-environment", methods=["POST"])
@cross_origin()
def create_dev_environment() -> dict[str, bool]:
    email = request.form.get("email")

    githubRepoUrl = request.json["githubRepoUrl"]
    email = request.json["email"]
    access_token = request.json["githubAccessToken"]
    create_development_environment.delay(githubRepoUrl, email, access_token)

    return {"success": True}
