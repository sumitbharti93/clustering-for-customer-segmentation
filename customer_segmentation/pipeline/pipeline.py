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

from customer_segmentation.constant import *

import uuid 

from multiprocessing import Process
from threading import Thread
import sys, os
import pandas as pd
from collections import namedtuple
from datetime import datetime 
from customer_segmentation.entity.config_entity import DataIngestionConfig

Experiment = namedtuple("Experiment", ["experiment_id", "initialization_timestamp", "artifact_time_stamp",
                                       "running_status", "start_time", "stop_time", "execution_time", "message",
                                       "experiment_file_path"])

config = Configuration()
os.makedirs(config.training_pipeline_config.artifact_dir,exist_ok=True)

class Pipeline(Thread):
    experiment: Experiment = Experiment(*([None] * 9))
    experiment_file_path = os.path.join(config.training_pipeline_config.artifact_dir,
                                        EXPERIMENT_DIR_NAME, EXPERIMENT_FILE_NAME)

    def __init__(self,config:Configuration = config)->None:
        try:           
            super().__init__(daemon=False, name = 'pipeline')
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
            if Pipeline.experiment.running_status:
                logging.info("Pipeline is already running")
                return Pipeline.experiment
            # data ingestion
            logging.info("Pipeline starting.")

            experiment_id = str(uuid.uuid4())

            Pipeline.experiment = Experiment(experiment_id=experiment_id,
                                             initialization_timestamp=self.config.time_stamp,
                                             artifact_time_stamp=self.config.time_stamp,
                                             running_status=True,
                                             start_time=datetime.now(),
                                             stop_time=None,
                                             execution_time=None,
                                             experiment_file_path=Pipeline.experiment_file_path,
                                             message="Pipeline has been started."
                                             )
            logging.info(f"Pipeline experiment: {Pipeline.experiment}")

            self.save_experiment()

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
            
            stop_time = datetime.now()
            Pipeline.experiment = Experiment(experiment_id=Pipeline.experiment.experiment_id,
                                             initialization_timestamp=self.config.time_stamp,
                                             artifact_time_stamp=self.config.time_stamp,
                                             running_status=False,
                                             start_time=Pipeline.experiment.start_time,
                                             stop_time=stop_time,
                                             execution_time=stop_time - Pipeline.experiment.start_time,
                                             message="Pipeline has been completed.",
                                             experiment_file_path=Pipeline.experiment_file_path,
                                             )
            logging.info(f"Pipeline experiment: {Pipeline.experiment}")
            self.save_experiment()

        except Exception as e:
            raise cs_exception(e, sys) from e

    def run(self):
        try:
            self.run_pipeline()
        except Exception as e:
            raise e
        
    def save_experiment(self):
        try:
            if Pipeline.experiment.experiment_id is not None:
                experiment = Pipeline.experiment
                experiment_dict = experiment._asdict()
                experiment_dict: dict = {key: [value] for key, value in experiment_dict.items()}

                experiment_dict.update({
                    "created_time_stamp": [datetime.now()],
                    "experiment_file_path": [os.path.basename(Pipeline.experiment.experiment_file_path)]})

                experiment_report = pd.DataFrame(experiment_dict)

                os.makedirs(os.path.dirname(Pipeline.experiment_file_path), exist_ok=True)
                if os.path.exists(Pipeline.experiment_file_path):
                    experiment_report.to_csv(Pipeline.experiment_file_path, index=False, header=False, mode="a")
                else:
                    experiment_report.to_csv(Pipeline.experiment_file_path, mode="w", index=False, header=True)
            else:
                print("First start experiment")
        except Exception as e:
            raise cs_exception(e, sys) from e

    @classmethod
    def get_experiments_status(cls, limit: int = 5) -> pd.DataFrame:
        try:
            if os.path.exists(Pipeline.experiment_file_path):
                df = pd.read_csv(Pipeline.experiment_file_path)
                limit = -1 * int(limit)
                return df[limit:].drop(columns=["experiment_file_path", "initialization_timestamp"], axis=1)
            else:
                return pd.DataFrame()
        except Exception as e:
            raise cs_exception(e, sys) from e
