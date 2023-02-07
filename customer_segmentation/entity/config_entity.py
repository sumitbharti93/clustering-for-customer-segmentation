from collections import namedtuple

DataIngestionConfig = namedtuple("DataIngestionConfig",
["dataset_download_location","ingested_data_dir"] )

DataValidationConfig = namedtuple("DataValidationConfig",["schema_file_path", "report_file_path"])

DataTransformationConfig = namedtuple('DataTransformationConfig', ['transformed_file_dir'])

ModelTrainerConfig = namedtuple('ModelTrainerConfig', ['trained_model_file_path', "silhouette_score", "model_config_file_path"])

ClusterSaverConfig = namedtuple('ClusterSaverConfig', ['cluster_file_path'])

TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"])

