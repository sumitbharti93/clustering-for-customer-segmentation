from customer_segmentation.logger import logging
from customer_segmentation.exception import cs_exception
from customer_segmentation.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,\
     DataValidationConfig, DataTransformationConfig, ModelTrainerConfig, ClusterSaverConfig
import os,sys
from customer_segmentation.constant import *
from customer_segmentation.util.util import read_yaml_file


class Configuration():
    def __init__(self, config_info:CONFIG_FILE_PATH = CONFIG_FILE_PATH, current_time_stamp:CURRENT_TIME_STAMP = CURRENT_TIME_STAMP):
        self.config_info = read_yaml_file(config_info)
        self.training_pipeline_config = self.get_training_pipeline_config()
        self.time_stamp = current_time_stamp
    
    def get_data_ingestion_config(self)->DataIngestionConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir = os.path.join(artifact_dir, DATA_INGESTION_ARTIFACT_DIR,
                                        self.time_stamp)

            data_ingestion_info = self.config_info[DATA_INGESTION_CONFIG_KEY]

            dataset_download_location = data_ingestion_info[DATA_INGESTION_DOWNLOAD_LOCATION_KEY]

            ingested_data_dir = os.path.join(
                        data_ingestion_artifact_dir,
                        data_ingestion_info[DATA_INGESTION_INGESTED_DIR_NAME_KEY]
                    )
            
            data_ingestion_config=DataIngestionConfig(
                        dataset_download_location=dataset_download_location,
                        ingested_data_dir=ingested_data_dir
                    )
            logging.info(f"Data Ingestion Config':{data_ingestion_config}")
            return data_ingestion_config
        
        except Exception as e:
            raise cs_exception(e, sys) from e 
    
    def get_data_validation_config(self):
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_validation_artifact_dir = os.path.join(artifact_dir, DATA_VALIDATION_ARTIFACT_DIR_NAME,
                            self.time_stamp)
            
            data_validation_info = self.config_info[DATA_VALIDATION_CONFIG_KEY]
            schema_file_path = os.path.join(ROOT_DIR, 
                data_validation_info[DATA_VALIDATION_SCHEMA_DIR_KEY],
                data_validation_info[DATA_VALIDATION_SCHEMA_FILE_NAME_KEY]
                )
            report_file_path = os.path.join(data_validation_artifact_dir, data_validation_info[REPORT_FILE_NAME_KEY])
            data_validation_config = DataValidationConfig(schema_file_path=schema_file_path, report_file_path= report_file_path)
            logging.info(f"data_validation_config :{data_validation_config}")
            return data_validation_config

        except Exception as e:
            raise cs_exception(e,sys) from e 

    def get_data_transformation_config(self)->DataTransformationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_transformation_artifact_dir = os.path.join(artifact_dir, DATA_TRANSFORMATION_ARTIFACT_DIR,
                                            self.time_stamp)
            data_transformation_info = self.config_info[DATA_TRANSFORMATION_CONFIG_KEY]

            transformed_file_dir = os.path.join(data_transformation_artifact_dir, data_transformation_info[DATA_TRANSFORMATION_DIR_NAME_KEY])
            
            data_transformation_config = DataTransformationConfig(transformed_file_dir=transformed_file_dir)
            logging.info(f"data_transformation_config: {data_transformation_config}")

            return data_transformation_config

        except Exception as e:
            raise cs_exception(e, sys) from e 
    
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir

            model_trainer_artifact_dir=os.path.join(
                artifact_dir,
                MODEL_TRAINER_ARTIFACT_DIR,
                self.time_stamp
            )
            model_trainer_config_info = self.config_info[MODEL_TRAINER_CONFIG_KEY]
            
            trained_model_file_path = os.path.join(model_trainer_artifact_dir,
            model_trainer_config_info[TRAINED_MODEL_DIR_KEY],
            model_trainer_config_info[MODEL_FILE_NAME_KEY]
            )

            model_config_file_path = os.path.join(model_trainer_config_info[MODEL_CONFIG_DIR_KEY],
            model_trainer_config_info[MODEL_CONFIG_FILE_NAME_KEY]
            )

            silhouette_score = model_trainer_config_info[SILHOUETTE_SCORE_KEY]

            model_trainer_config = ModelTrainerConfig(
                trained_model_file_path= trained_model_file_path,
                silhouette_score = silhouette_score,
                model_config_file_path= model_config_file_path
            )
            logging.info(f"Model trainer config: {model_trainer_config}")
            return model_trainer_config
        
        except Exception as e:
            raise cs_exception(e,sys) from e
    
    def get_cluster_saver_config(self)->ClusterSaverConfig:
        try:
            cluster_saver_config = os.path.join(ROOT_DIR, 'saved_clusters', self.time_stamp)

            cluster_saver_config = ClusterSaverConfig(cluster_file_path=cluster_saver_config)

            return cluster_saver_config 
        except Exception as e:
            raise cs_exception(e, sys) from e 

    def get_training_pipeline_config(self)->TrainingPipelineConfig:
        try:
                training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
                artifact_dir = os.path.join(ROOT_DIR,training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
                training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
                )

                training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
                logging.info(f"Training pipeline config: {training_pipeline_config}")
                return training_pipeline_config
        except Exception as e:
            raise cs_exception(e,sys) from e 