from collections import namedtuple


DataIngestionArtifact = namedtuple("DataIngestionArtifact",
["data_file_path", "is_ingested", "message"])

DataValidationArtifact = namedtuple('DataValidationArtifact', 
['schema_file_path', 'report_file_path','is_validated', 'message'])

DataTransformationArtifact = namedtuple('DataTransformationArtifact',
['is_transformed', 'message', 'transformed_data_file_path'])

ModelTrainerArtifact = namedtuple("ModelTrainerArtifact", ["is_trained", "message", "trained_model_file_path",
                                                           "silhouette_score"])
ClusterSaverArtifact = namedtuple("ClusterSaverArtifact", ["is_cluster_saved", "export_cluster_file_path"])
