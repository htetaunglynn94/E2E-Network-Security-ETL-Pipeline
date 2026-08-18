import os
import numpy as np

# Constant Information for DATA INGESTION
## Define common constant variable for training pipeline

TARGET_COLUMN = "Result"                 # dependent feature to predict
PIPELINE_NAME:str = "NetworkSecurity"
ARTIFACT_DIR:str = "artifacts"
FILE_NAME:str = "phisingData.csv"       # raw data file
TRAIN_FILE_NAME:str = "train.csv"       # traiining data file
TEST_FILE_NAME:str = "test.csv"         # testing data file
SCHEMA_FILE_PATH:str = os.path.join("data_schema", "schema.yaml")
SAVED_MODEL_DIR:str = os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"
MT_FINAL_MODEL_DIR:str = "final_model"

## Data ingestion related constant start with DI_VARNAME

DI_COLLECTION_NAME:str = "NetworkData"
DI_DB_NAME:str = "HtetAungLynn"
DI_DIR_NAME:str = "data_ingestion"
DI_FEATURE_STORE_DIR:str = "feature_store"
DI_INGESTED_DIR:str = "ingested"           
DI_TTS_RATIO:float = 0.2      # tain-test-split ratio


# Constant Information for DATA INGESTION
## Data validation related constant start with DV_VARNAME
DV_DIR_NAME:str = "data_validation"
DV_VALID_DIR:str = "valid"
DV_INVALID_DIR:str = "invalid"
DV_DRIFT_REPORT_DIR:str = "drift_report"
DV_DRIFT_REPORT_FILE_NAME:str = "report.yaml"
 
# Constant Information for DATA TRANSFORMATION
## Data transformation related constant start with DT_VARNAME
DT_DIR_NAME:str = "data_transformation"
DT_TRANSFORMED_DATA_DIR:str = "transformed_data"
DT_TRANSFORMED_OBJ_DIR:str = "transformed_object"
PREPROCESSOR_OBJ_FILE_NAME:str = "preprocessor.pkl"

## KNN imputer to replace missing values
DT_TRANSOFRMATION_IMPUTER_PARAS:dict = {"missing_values": np.nan,
                                        "n_neighbors": 3,
                                        "weights": 'uniform'}          
DT_TRAIN_FILE_PATH:str = "train.npy"
DT_TEST_FILE_PATH:str = "test.npy"

# Constant Information for MODEL TRAINING
## Model training related conatant start with MT_VARNAME
MT_DIR_NAME:str = "model_trainer"
MT_MODEL_DIR:str = "trained_model"
MT_MODEL_NAME:str = "model.pkl"
MT_EXPECTED_SCORE:float = 0.6
MT_OVER_AND_UNDER_FITTING_THRESHOLD:float = 0.05
MT_FINAL_MODEL:str = "ml_model.pkl"

# Constant Information for MODEL PREDICTION
## Model prediction related conatant start with MT_VARNAME
MP_DIR_NAME:str = "predicted_output"
MP_DATA:str = "predicted_data.csv"

# Constant Information for AWS S3
## S3 related constant start with S3_VARNAME
S3_TRAINING_BUCKET_NAME:str = "aws-s3-network-security"

