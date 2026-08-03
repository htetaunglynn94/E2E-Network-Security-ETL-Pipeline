# Constant Information for DATA INGESTION

## Define common constant variable for training pipeline

TARGET_COLUMN = "Result"                 # dependent feature to predict
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "artifacts"
FILE_NAME: str = "phisingData.csv"       # raw data file
TRAIN_FILE_NAME: str = "train.csv"       # traiining data file
TEST_FILE_NAME: str = "test.csv"         # testing data file


## Data ingestion related constant start with DI VAR NAME

DI_COLLECTION_NAME: str = "NetworkData"
DI_DB_NAME: str = "HtetAungLynn"
# DI_DIR_NAME: str = "data_ingestion"
DI_FEATURE_STORE_DIR: str = "feature_store"
DI_INGESTED_DIR: str = "ingested"           
DI_TTS_RATIO: float = 0.2      # tain-test-split ratio



