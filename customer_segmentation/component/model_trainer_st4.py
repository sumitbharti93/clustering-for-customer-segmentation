from customer_segmentation.exception import cs_exception
import sys
import pandas as pd
from customer_segmentation.logger import logging
from typing import List
from customer_segmentation.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from customer_segmentation.entity.config_entity import ModelTrainerConfig
from customer_segmentation.util.util import save_object,load_object
from customer_segmentation.entity.model_factory import MetricInfoArtifact, ModelFactory,GridSearchedBestModel
from customer_segmentation.entity.model_factory import evaluate_cluster_model




class ModelTrainer:

    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            logging.info(f"{'>>' * 30}Model trainer log started.{'<<' * 30} ")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise cs_exception(e, sys) from e

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            logging.info(f"Loading transformed dataset")
            transformed_data_file_path = self.data_transformation_artifact.transformed_data_file_path
            transformed_data = pd.read_csv(transformed_data_file_path, index_col="CustomerID")

            logging.info(f"Extracting model config file path")
            model_config_file_path = self.model_trainer_config.model_config_file_path

            logging.info(f"Initializing model factory class using above model config file: {model_config_file_path}")
            model_factory = ModelFactory(model_config_path=model_config_file_path)
            
            
            silhouette_score = self.model_trainer_config.silhouette_score
            logging.info(f"Expected accuracy: {silhouette_score}")

            logging.info(f"Initiating operation model selection")
            best_model = model_factory.get_best_model(transformed_data,slh_score=silhouette_score)
            
            logging.info(f"Best model found on transformed dataset: {best_model}")

            trained_model_file_path=self.model_trainer_config.trained_model_file_path
            logging.info(f"Saving model at path: {trained_model_file_path}")
            save_object(file_path=trained_model_file_path,obj=best_model.model)


            model_trainer_artifact=  ModelTrainerArtifact(is_trained=True,message="Model Trained successfully",
            trained_model_file_path=trained_model_file_path,
            silhouette_score=best_model.slh_score
            )

            logging.info(f"Model Trainer Artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise cs_exception(e, sys) from e

    def __del__(self):
        logging.info(f"{'>>' * 30}Model trainer log completed.{'<<' * 30} ")



#loading transformed training and testing datset
#reading model config file 
#getting best model on training datset
#evaludation models on both training & testing datset -->model object
#loading preprocessing pbject
#custom model object by combining both preprocessing obj and model obj
#saving custom model object
#return model_trainer_artifact