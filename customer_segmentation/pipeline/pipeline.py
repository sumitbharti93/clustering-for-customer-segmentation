from customer_segmentation.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, \
DataTransformationArtifact, ModelTrainerArtifact
from customer_segmentation.configuration.configuration import Configuration
from customer_segmentation.exception import cs_exception
from customer_segmentation.logger import logging 
from customer_segmentation.component.data_ingestion_st1 import DataIngestion
from customer_segmentation.component.data_validation_st2 import DataValidation
from customer_segmentation.component.data_transformation_st3 import DataTransformation
from customer_segmentation.component.model_trainer_st4 import ModelTrainer
from customer_segmentation.component.cluster_saver_st5 import ClusterSaver




import sys, os
import pandas as pd
from collections import namedtuple
from datetime import datetime 
from customer_segmentation.entity.config_entity import DataIngestionConfig



config = Configuration()
os.makedirs(config.training_pipeline_config.artifact_dir,exist_ok=True)

class Pipeline():

    def __init__(self,config:Configuration = config)->None:
        try:           
            self.config=config
        except Exception as e:
            raise cs_exception(e,sys) from e
    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise cs_exception(e, sys) from e
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact)-> DataValidationArtifact:
        try:
            data_validation = DataValidation(self.config.get_data_validation_config(), data_ingestion_artifact=data_ingestion_artifact)
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise cs_exception(e, sys) from e
        
    def start_data_transformation(self,
                                data_ingestion_artifact: DataIngestionArtifact,
                                data_validation_artifact: DataValidationArtifact
                                ) -> DataTransformationArtifact:
        try:
            data_transformation = DataTransformation(
                data_transformation_config=self.config.get_data_transformation_config(),
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise cs_exception(e, sys) 
        
    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(model_trainer_config=self.config.get_model_trainer_config(),
                                            data_transformation_artifact=data_transformation_artifact
                                            )
            return model_trainer.initiate_model_trainer()
        except Exception as e:
            raise cs_exception(e, sys) from e
    
    def start_cluster_saver(self, data_ingestion_artifact, data_transformation_artifact, model_trainer_artifact):
        try:
            cluster_saver = ClusterSaver(cluster_saver_config=self.config.get_cluster_saver_config(),data_ingestion_artifact=data_ingestion_artifact,
                                         data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_artifact=model_trainer_artifact)
            return cluster_saver.initiate_cluster_formation()
        except Exception as e:
            raise cs_exception(e, sys) from e 
        
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()       
            data_validation_artifact = self.start_data_validation(
                data_ingestion_artifact=data_ingestion_artifact)

            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            ) 

            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)

            cluster_saver_artifact = self.start_cluster_saver(data_ingestion_artifact=data_ingestion_artifact,
                                                              data_transformation_artifact=data_transformation_artifact,
                                                              model_trainer_artifact=model_trainer_artifact)
        except Exception as e:
            raise cs_exception(e, sys) from e

    def run(self):
        try:
            self.run_pipeline()
        except Exception as e:
            raise e

