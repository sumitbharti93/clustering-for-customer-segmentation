from customer_segmentation.constant import *
from customer_segmentation.exception import cs_exception
from customer_segmentation.configuration.configuration import Configuration
from customer_segmentation.component.data_ingestion_st1 import DataIngestion
from customer_segmentation.logger import logging 
from customer_segmentation.pipeline.pipeline import Pipeline

def main():
    try:
        print(CONFIG_FILE_PATH)
        print(CURRENT_TIME_STAMP)
        pipeline = Pipeline()
        pipeline.start()
    except Exception as e:
        raise cs_exception(e,sys) from e

if __name__ =="__main__":
    main()