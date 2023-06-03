#!/bin/bash
set -x

# Check if the OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "OPENAI_API_KEY is not set"
    echo "Make sure you have an OpenAI API key from https://platform.openai.com/account/api-keys"
    exit 1
fi

# Check if the GH_ACCESS_TOKEN is set
if [ -z "$GH_ACCESS_TOKEN" ]; then
    echo "GH_ACCESS_TOKEN is not set"
    echo "Make sure you have a GitHub personal access token with the repo and codespaces scopes"
    exit 1
fi

# Check if the CELERY_BROKER_URL is set
if [ -z "$CELERY_BROKER_URL" ]; then
    echo "CELERY_BROKER_URL is not set"
    echo "Make sure you've set your CELERY_BROKER_URL to a valid RabbitMQ URL or Redis URL"
    echo "If you're running the demo version, ask Matthew for the Heroku Cloud RabbitMQ URL (which should be in the projct discord channel)"
    exit 1
fi

# Open the first terminal window and execute the first command for running the celery worker
osascript -e 'tell application "Terminal" to do script "cd backend && celery --app app.tasks worker --loglevel INFO"'

sleep 5

# Open the second terminal window and execute the second command for running the FastAPI server
osascript -e 'tell application "Terminal" to do script "cd backend && python main.py"'

sleep 5

# Open the third terminal window and execute the third command for running the React frontend
osascript -e 'tell application "Terminal" to do script "cd frontend && npm install && npm run start"'
