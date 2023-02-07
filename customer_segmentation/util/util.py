from customer_segmentation.exception import cs_exception
from customer_segmentation.logger import logging
import os,sys
import yaml
import dill


def read_yaml_file(file_path):

    '''
    except file path as a parameter and return dictionary as output 
    '''
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise cs_exception(e, sys)  from e


def write_yaml_file(file_path:str,data:dict = None):
    """
    Create yaml file 
    file_path: str
    data: dict
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"w") as yaml_file:
            if data is not None:
                yaml.dump(data,yaml_file)
    except Exception as e:
        raise cs_exception(e,sys)
    
def save_data(file_path, data = None):
    """ save dataframe to csv file """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path,"w") as file:
            if data is not None:
                data.to_csv(file)
    except Exception as e:
        raise cs_exception(e,sys)
    

def save_object(file_path:str,obj):
    """
    file_path: str
    obj: Any sort of object
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise cs_exception(e,sys) from e

def load_object(file_path:str):
    """
    file_path: str
    """
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise cs_exception(e,sys) from e