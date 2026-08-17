import sys, os, certifi, pymongo
import pandas as pd
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import Response
from uvicorn import run as app_run
from starlette.responses import RedirectResponse

from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException
from network_security.pipeline.training_pipeline import TrainingPipeline
from network_security.constant.training_pipeline import DI_COLLECTION_NAME, DI_DB_NAME

from network_security.utils.main_utils.utils import load_object

ca = certifi.where()
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
print(mongo_db_url)

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DI_DB_NAME]
collection = database[DI_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware( CORSMiddleware,
                    allow_origins = origins,
                    allow_credentials = True,
                    allow_methods = ["*"],
                    allow_headers = ["*"])

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Training is successful.")

    except Exception as e:
        raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)
