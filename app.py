import sys, os, certifi, pymongo
import pandas as pd
from dotenv import load_dotenv

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import Response, FileResponse
from uvicorn import run as app_run
from starlette.responses import RedirectResponse

from network_security.logging.logger import logging
from network_security.exception.exception import NetworkSecurityException
from network_security.pipeline.training_pipeline import TrainingPipeline
from network_security.constant.training_pipeline import DI_COLLECTION_NAME, DI_DB_NAME
from network_security.entity.config_entity import (DataTransformationConfig,
                                                   ModelTrainerConfig,
                                                   ModelPredictionConfig,
                                                   TrainingPipelineConfig)


from network_security.utils.main_utils.utils import load_object
from network_security.utils.ml_utils.model.estimator import NetworkModel
from fastapi.templating import Jinja2Templates

ca = certifi.where()
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
print(mongo_db_url)

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DI_DB_NAME]
collection = database[DI_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]
templates = Jinja2Templates(directory="./templates")

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

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile=File(...)):
    try:
        df = pd.read_csv(file.file)

        train_pipeline_conf = TrainingPipelineConfig()
        dt_conf = DataTransformationConfig(train_pipeline_conf)
        mt_conf = ModelTrainerConfig(train_pipeline_conf)
        mp_conf = ModelPredictionConfig(train_pipeline_conf)

        preprocessor = load_object(dt_conf.preprocessor_obj)
        final_model = load_object(mt_conf.mt_final_model)

        network_model = NetworkModel(preprocessor, final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        df.to_csv(mp_conf.mp_output_data)
        table_html = df.to_html(classes='table table-striped', index=False)
        
        # Render template using Jinja2
        template = templates.get_template("table.html")
        html_content = template.render({"request": request, "table": table_html})

        # Save the rendered HTML to a local file path
        output_file_path = os.path.join("templates", "predictions.html")
        with open(output_file_path, "w", encoding="utf-8") as f:
            f.write(html_content)


        return FileResponse(path=output_file_path,
                            media_type="text/html", 
                            filename='predictions.html')

    except Exception as e:
        raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)
