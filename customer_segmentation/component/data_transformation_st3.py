from customer_segmentation.exception import cs_exception
from customer_segmentation.logger import logging
from customer_segmentation.entity.config_entity import DataTransformationConfig
from customer_segmentation.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, \
    DataTransformationArtifact

import sys,os
import numpy as np
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import pandas as pd
from customer_segmentation.constant import *
from customer_segmentation.util.util import save_data

class DataTransformation:

    def __init__(self,data_transformation_config:DataTransformationConfig,
                    data_ingestion_artifact:DataIngestionArtifact,
                    data_validation_artifact : DataValidationArtifact
                    ):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact

        except Exception as e:
            raise cs_exception(e,sys)


    def get_transformed_data(self):
        try:
            data_file_path = self.data_ingestion_artifact.data_file_path
            ## Loading data into dataframe 
            file_data_frame = pd.read_excel(data_file_path) 

            # dropping rows containing null values 
            file_data_frame.dropna(axis=0, inplace = True)

            # converting invoicedate type to str for further operation 
            file_data_frame.InvoiceDate = file_data_frame.InvoiceDate.astype(str)

            # generating anew column for invoice date to simplify the operation
            var = file_data_frame.InvoiceDate.str.split(' ').str[0].str.split("-")
            file_data_frame['invoice_date'] = var.str[0]+var.str[1]+var.str[2]

            # again changing the datetype of newly generated invoice date to int 
            file_data_frame.invoice_date = file_data_frame.invoice_date.astype(int)

            # dropping the old invoice date column
            file_data_frame.drop('InvoiceDate', axis=1, inplace = True)

            # there are some values which is negative for cancelled order , we need to remove that
            file_data_frame.drop(file_data_frame[(file_data_frame.Quantity<0)].index, inplace = True)

            # converting bins for invoice date for further operation 
            # file_data_frame["invoice_date_cat"] = pd.cut(file_data_frame["invoice_date"],
            #     bins =[20101200, 20101202,20101206],
            #     labels=[2,1])

            file_data_frame["invoice_date_cat"] = pd.cut(file_data_frame["invoice_date"],
                bins =[20101200, 20110100,20110200,20110300,20110400,20110500,20110600,20110700,20110800,20110900,20111000,20111100,np.inf],
                labels=[12,11,10,9,8,7,6,5,4,3,2,1])
            
            # multiplying unit price and quantity to get the final purchase value 
            file_data_frame['purchase_value'] = file_data_frame.Quantity*file_data_frame.UnitPrice

            # generating dataframe for unique customer id 
            d = file_data_frame.groupby('CustomerID')['CustomerID'].all().index
            customer_id_df = pd.DataFrame(d)
            
            # generating purchase value dataframe for each unique customer 

            purchase_value_df = pd.DataFrame(file_data_frame.groupby('CustomerID')['purchase_value'].sum().values, columns = ['purchase_value'])

            # generating no of transaction dataframe for each unique customer 

            no_of_transaction_df = pd.DataFrame(file_data_frame.groupby('CustomerID')['invoice_date_cat'].count().values, columns = ['no_of_transaction'])

            # generating recent transaction dataframe for each unique customer 

            recent_transaction_df = pd.DataFrame(file_data_frame.groupby('CustomerID')['invoice_date_cat'].max().values, columns = ['recent_transaction'])

            frames = [customer_id_df, purchase_value_df, no_of_transaction_df, recent_transaction_df]

            # generating final dataframe for each unique customer id, purchased value, no of transaction and recent transaction 

            final_df = pd.concat(frames,axis=1)
            
            # setting customerid as index value 

            final_df.set_index(final_df.CustomerID, inplace = True)
            final_df.drop('CustomerID', axis=1, inplace = True)
            print(final_df)
            return final_df

        except Exception as e:
            raise cs_exception(e,sys) from e   

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info(f"-------starting data tranformation------------")
            transformed_data = self.get_transformed_data()
            
            transformed_dir = self.data_transformation_config.transformed_file_dir

            transformed_file_name = "transformed_data.csv"

            transformed_data_file_path = os.path.join(transformed_dir, transformed_file_name)
    
            logging.info(f"Saving transformed data into the specified directory.")

            save_data(transformed_data_file_path, transformed_data)

            data_transformation_artifact = DataTransformationArtifact(is_transformed=True,
            message="Data transformation successfull.",
            transformed_data_file_path=transformed_data_file_path
            )
            logging.info(f"Data transformationa artifact: {data_transformation_artifact}")
            return data_transformation_artifact
            
        except Exception as e:
            raise cs_exception(e,sys) from e

    def __del__(self):
        logging.info(f"{'>>'*30}Data Transformation log completed.{'<<'*30} \n\n")