from customer_segmentation.exception import cs_exception
import sys,os
import pandas as pd
from customer_segmentation.logger import logging
from customer_segmentation.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, DataIngestionArtifact, ClusterSaverArtifact
from customer_segmentation.entity.config_entity import ClusterSaverConfig
from customer_segmentation.util.util import save_object,load_object
from customer_segmentation.entity.model_factory import ModelFactory
from customer_segmentation.util.util import save_data


class ClusterSaver:
    try:
        def __init__(self,cluster_saver_config, data_ingestion_artifact, data_transformation_artifact, model_trainer_artifact):
            self.cluster_saver_config = cluster_saver_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
    except Exception as e:
        raise cs_exception(e, sys) from e 

    def initiate_cluster_formation(self,)-> ClusterSaverArtifact:
        try:
            # cluster file path 
            cluster_file_path = self.cluster_saver_config.cluster_file_path
            os.makedirs(cluster_file_path, exist_ok=True)

            # Loading original data 
            file_path = self.data_ingestion_artifact.data_file_path
            ingested_data = pd.read_excel(file_path)
            
            # Loading Transformed data 
            transformed_file_path = self.data_transformation_artifact.transformed_data_file_path
            transformed_data  = pd.read_csv(transformed_file_path, index_col="CustomerID")

            # loading trained model object 
            model_file_path = self.model_trainer_artifact.trained_model_file_path

            model = load_object(file_path=model_file_path)

            cluster_value = model.predict(transformed_data)

            ## saving Transformed data cluster 

            for i in range(model.n_clusters):
                file_name = f"transformed_data_cluster{i+1}.csv"
                tranformed_cluster_file_path = os.path.join(cluster_file_path, file_name)
                transformed_clustered_data = transformed_data[cluster_value==i]
                save_data(tranformed_cluster_file_path, transformed_clustered_data)
            
            ## saving cluster from the ingested / original data
            for i in range(model.n_clusters):
                file_name = f"ingested_data_cluster{i+1}.csv"
                ingested_cluster_file_path = os.path.join(cluster_file_path, file_name)
                ingested_clustered_data = pd.DataFrame(columns=ingested_data.columns)
                for i in transformed_data[cluster_value==i].index:
                    print(i)
                    new_df = ingested_data[ingested_data.CustomerID==i]
                    frames = [ingested_clustered_data, new_df]
                    ingested_clustered_data= pd.concat(frames, axis =0)
                save_data(ingested_cluster_file_path, ingested_clustered_data)

            cluster_saver_artifact = ClusterSaverArtifact(is_cluster_saved=True, export_cluster_file_path= cluster_file_path)

            logging.info(f" Cluster for both transformed and ingested data has been successfully saved ")

            return cluster_saver_artifact

        except Exception as e:
            raise cs_exception(e, sys) from e 