import os

import uvicorn
from dotenv import load_dotenv
from loguru import logger

filepaths = ['backend/app/.env', 'app/.env', 'backend/.env','.env']

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

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
