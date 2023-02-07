from customer_segmentation.exception import cs_exception
from customer_segmentation.entity.config_entity import DataIngestionConfig
from customer_segmentation.entity.artifact_entity import DataIngestionArtifact
from customer_segmentation.logger import logging 
from customer_segmentation.constant import *
from customer_segmentation.configuration.configuration import Configuration
import sys, os
import shutil 
from customer_segmentation.entity.config_entity import DataIngestionConfig
import pandas as pd 
import numpy as np

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig ):
            try:
                logging.info(f"{'=='*20}Data Ingestion log started.{'='*20} ")
                self.data_ingestion_config = data_ingestion_config

            except Exception as e:
                raise cs_exception(e,sys) from e

    def download_data(self,):
        try:
            download_location = self.data_ingestion_config.dataset_download_location

            #folder location to download file 
            ingested_data_dir = self.data_ingestion_config.ingested_data_dir
            if os.path.exists(ingested_data_dir):
                os.remove(ingested_data_dir)
            os.makedirs(ingested_data_dir,exist_ok=True)

            segmentation_data_file_name = os.path.basename(download_location)

            ingested_file_path = os.path.join(ingested_data_dir, segmentation_data_file_name)
            logging.info(f"Downloading file from :[{download_location}] into :[{ingested_file_path}]")

            shutil.copy(r'D:\Python Project\clustering-for-customer-segmentation\data\Online Retail.xlsx', ingested_file_path)

            logging.info(f"File :[{ingested_file_path}] has been downloaded successfully.")
            return ingested_file_path

        except Exception as e:
            raise cs_exception(e,sys) from e

    
    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            ingested_file_path =  self.download_data()
            data_ingestion_artifact = DataIngestionArtifact(data_file_path=ingested_file_path,
                                                            is_ingested=True,
                                                            message="Data has been succesfully downloaded to the specified folder")
            return data_ingestion_artifact
        except Exception as e:
            raise cs_exception(e,sys) from e

    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")

