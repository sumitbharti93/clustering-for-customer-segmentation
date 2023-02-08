from customer_segmentation.logger import logging, get_current_time_stamp
from customer_segmentation.exception import cs_exception
import os,sys


ROOT_DIR = os.getcwd()
CONFIG_FOLDER = 'config'
CONFIG_FILE_NAME = 'config.yaml'

CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_FOLDER, CONFIG_FILE_NAME)
CURRENT_TIME_STAMP = get_current_time_stamp()


# Training pipeline related variable
TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"

# Data Ingestion related variable

DATA_INGESTION_CONFIG_KEY = "data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR = "data_ingestion"
DATA_INGESTION_DOWNLOAD_LOCATION_KEY = "dataset_download_location"
DATA_INGESTION_INGESTED_DIR_NAME_KEY = "ingested_dir"

# Data Validation related variable 

DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY = "schema_file_name"
DATA_VALIDATION_SCHEMA_DIR_KEY = "schema_dir"
DATA_VALIDATION_ARTIFACT_DIR_NAME = "data_validation"
REPORT_FILE_NAME_KEY = 'report_file_name'


# Data Transformation related variables
DATA_TRANSFORMATION_ARTIFACT_DIR = "data_transformation"
DATA_TRANSFORMATION_CONFIG_KEY = "data_transformation_config"
DATA_TRANSFORMATION_DIR_NAME_KEY = "transformed_dir"

#Model Trainer realted variables

MODEL_TRAINER_CONFIG_KEY = "model_trainer_config"
MODEL_TRAINER_ARTIFACT_DIR = "model_trainer"
TRAINED_MODEL_DIR_KEY = "trained_model_dir"
MODEL_CONFIG_DIR_KEY = "model_config_dir"
MODEL_CONFIG_FILE_NAME_KEY = "model_config_file_name"
MODEL_FILE_NAME_KEY = "model_file_name"
SILHOUETTE_SCORE_KEY  = "silhouette_score"


# Experiment dir and file name 

EXPERIMENT_DIR_NAME="experiment"
EXPERIMENT_FILE_NAME="experiment.csv"