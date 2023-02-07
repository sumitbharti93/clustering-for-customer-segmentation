from customer_segmentation.logger import logging
from customer_segmentation.exception import cs_exception
from customer_segmentation.entity.config_entity import DataValidationConfig
from customer_segmentation.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, ClusterSaverArtifact
import os, sys
import pandas as pd
import yaml
import json
from customer_segmentation.util.util import read_yaml_file, write_yaml_file


class DataValidation:
    def __init__(self, data_validation_config:DataValidationConfig,
        data_ingestion_artifact: DataIngestionArtifact):
        try:
        
            logging.info(f"{'>>'*30}Data Validation log started .{'<<'*30} \n\n")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact

        except Exception as e:
            raise cs_exception(e,sys) from e

    def file_data_frame(self):
        try:
            file_data_frame = pd.read_excel(self.data_ingestion_artifact.data_file_path)
            return file_data_frame
        except Exception as e:
            raise cs_exception(e,sys) from e
    
    def validate_dataset_schema(self)->bool:
        try:
            validation_status = False 
            file_data_frame = self.file_data_frame()
            data_column_name = file_data_frame.columns
            validation_schema = read_yaml_file(self.data_validation_config.schema_file_path)
            column_from_schema = validation_schema['columns']
            flag=0
            if len(data_column_name)==len(column_from_schema):
                i = 0
                for key in column_from_schema.keys():
                    if key!=data_column_name[i]:
                        flag=1
                        break
                    i+=1
                k =0
                for values in column_from_schema.values():
                    if values!=file_data_frame.dtypes[k]:
                        flag=1
                        break
                    k+=1
            if flag==0:
                validation_status = True

            return validation_status

        except Exception as e:
            raise cs_exception(e,sys) from e


    def initiate_data_validation(self):
        try:
            if self.validate_dataset_schema():
                message = {'validation_message': "data has been succesfully validated and it is per the schema mentioned in the schema.yaml file "}
                write_yaml_file(self.data_validation_config.report_file_path, message)

                data_validation_artifact = DataValidationArtifact(
                    schema_file_path  = self.data_validation_config.schema_file_path,
                    report_file_path  = self.data_validation_config.report_file_path,
                    is_validated = True,
                    message = "Data Validation Performed Successfully"
                )
                logging.info(f'Data Validation artifact : {data_validation_artifact}')
            else:
                message = "Schema validation fail"
                raise Exception(message)
            return data_validation_artifact

        except Exception as e:
            raise cs_exception(e,sys) from e

        def __del__(self):
            logging.info(f"{'>>'*30}Data Validation log completed.{'<<'*30} \n\n")