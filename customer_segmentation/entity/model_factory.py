from cmath import log
import importlib
from pyexpat import model
import numpy as np
import yaml
from customer_segmentation.exception import cs_exception
import os
import sys
from sklearn.metrics import silhouette_samples, silhouette_score
from collections import namedtuple
from typing import List
import matplotlib.pyplot as plt
from customer_segmentation.logger import logging
from sklearn.metrics import r2_score,mean_squared_error
GRID_SEARCH_KEY = 'grid_search'
MODULE_KEY = 'module'
CLASS_KEY = 'class'
PARAM_KEY = 'params'
MODEL_SELECTION_KEY = 'model_selection'
SEARCH_PARAM_GRID_KEY = "search_param_grid"

InitializedModelDetail = namedtuple("InitializedModelDetail",
                                    ["model_serial_number", "model", "param_grid_search", "model_name"])

GridSearchedBestModel = namedtuple("GridSearchedBestModel", ["model_serial_number",
                                                             "model",
                                                             "best_model",
                                                             "best_parameters",
                                                             "grid_search_cv"
                                                             ])

BestModel = namedtuple("BestModel", ["model",
                                     "slh_score"])


class ModelFactory:
    def __init__(self, model_config_path: str = None, ):
        try:
            self.config: dict = ModelFactory.read_params(model_config_path)

            self.grid_search_cv_module: str = self.config[GRID_SEARCH_KEY][MODULE_KEY]
            self.grid_search_class_name: str = self.config[GRID_SEARCH_KEY][CLASS_KEY]
            self.grid_search_property_data: dict = dict(self.config[GRID_SEARCH_KEY][PARAM_KEY])

            self.models_initialization_config: dict = dict(self.config[MODEL_SELECTION_KEY])

            self.initialized_model_list = None
            self.grid_searched_best_model_list = None

        except Exception as e:
            raise cs_exception(e, sys) from e

    @staticmethod
    def update_property_of_class(instance_ref:object, property_data: dict):
        try:
            if not isinstance(property_data, dict):
                raise Exception("property_data parameter should be dictionary")

            for key, value in property_data.items():
                logging.info(f"Executing:$ {str(instance_ref)}.{key}={value}")
                setattr(instance_ref, key, value)
            return instance_ref
        except Exception as e:
            raise cs_exception(e, sys) from e

    @staticmethod
    def read_params(config_path: str) -> dict:
        try:
            with open(config_path, 'r') as yaml_file:
                config:dict = yaml.safe_load(yaml_file)
            return config
        except Exception as e:
            raise cs_exception(e, sys) from e

    @staticmethod
    def class_for_name(module_name:str, class_name:str):
        try:
            # load the module, will raise ImportError if module cannot be loaded
            module = importlib.import_module(module_name)
            # get the class, will raise AttributeError if class cannot be found
            logging.info(f"Executing command: from {module} import {class_name}")
            class_ref = getattr(module, class_name)
            return class_ref
        except Exception as e:
            raise cs_exception(e, sys) from e

    def execute_grid_search_operation(self, initialized_model: InitializedModelDetail, transformed_data) -> GridSearchedBestModel:
        """
        excute_grid_search_operation(): function will perform paramter search operation and
        it will return you the best optimistic  model with best paramter:
        estimator: Model object
        param_grid: dictionary of paramter to perform search operation
        input_feature: your all input features
        output_feature: Target/Dependent features
        ================================================================================
        return: Function will return GridSearchOperation object
        """
        try:
            # instantiating GridSearchCV class
            
           
            grid_search_cv_ref = ModelFactory.class_for_name(module_name=self.grid_search_cv_module,
                                                             class_name=self.grid_search_class_name
                                                             )

            grid_search_cv = grid_search_cv_ref(estimator=initialized_model.model,
                                                param_grid=initialized_model.param_grid_search)
            grid_search_cv = ModelFactory.update_property_of_class(grid_search_cv,
                                                                   self.grid_search_property_data)

            
            message = f'{">>"* 30} f"Training {type(initialized_model.model).__name__} Started." {"<<"*30}'
            logging.info(message)





            grid_search_cv.fit(transformed_data)
            message = f'{">>"* 30} f"Training {type(initialized_model.model).__name__}" completed {"<<"*30}'
            logging.info(message)
            grid_searched_best_model = GridSearchedBestModel(model_serial_number=initialized_model.model_serial_number,
                                                             model=initialized_model.model,
                                                             best_model=grid_search_cv.best_estimator_,
                                                             best_parameters=grid_search_cv.best_params_,
                                                             grid_search_cv=grid_search_cv
                                                             )
            
            return grid_searched_best_model
        except Exception as e:
            raise cs_exception(e, sys) from e

    def get_initialized_model_list(self) -> List[InitializedModelDetail]:
        """
        This function will return a list of model details.
        return List[ModelDetail]
        """
        try:
            initialized_model_list = []
            for model_serial_number in self.models_initialization_config.keys():

                model_initialization_config = self.models_initialization_config[model_serial_number]
                model_obj_ref = ModelFactory.class_for_name(module_name=model_initialization_config[MODULE_KEY],
                                                            class_name=model_initialization_config[CLASS_KEY]
                                                            )
                model = model_obj_ref()
                
                if PARAM_KEY in model_initialization_config:
                    model_obj_property_data = dict(model_initialization_config[PARAM_KEY])
                    model = ModelFactory.update_property_of_class(instance_ref=model,
                                                                  property_data=model_obj_property_data)

                param_grid_search = model_initialization_config[SEARCH_PARAM_GRID_KEY]
                model_name = f"{model_initialization_config[MODULE_KEY]}.{model_initialization_config[CLASS_KEY]}"

                model_initialization_config = InitializedModelDetail(model_serial_number=model_serial_number,
                                                                     model=model,
                                                                     param_grid_search=param_grid_search,
                                                                     model_name=model_name
                                                                     )

                initialized_model_list.append(model_initialization_config)

            self.initialized_model_list = initialized_model_list
            return self.initialized_model_list
        except Exception as e:
            raise cs_exception(e, sys) from e

    def initiate_best_parameter_search_for_initialized_model(self, initialized_model: InitializedModelDetail,
                                                             transformed_data, slh_score) -> GridSearchedBestModel:
        """
        initiate_best_model_parameter_search(): function will perform paramter search operation and
        it will return you the best optimistic  model with best paramter:
        estimator: Model object
        param_grid: dictionary of paramter to perform search operation
        input_feature: your all input features
        output_feature: Target/Dependent features
        ================================================================================
        return: Function will return a GridSearchOperation
        """
        try:
            wcss = []
            for i in range(1,11):
                model = ModelFactory.update_property_of_class(instance_ref=initialized_model.model, 
                                                              property_data={"n_clusters" :i})
                model.fit(transformed_data)
                wcss.append(model.inertia_)
                
            plt.plot(range(1,11),wcss)
            plt.title("Elbow method")
            plt.xlabel('Number of clusters')
            plt.ylabel('WCSS')
            plt.show()

            percentage = []
            for i in range(len(wcss)-1):
                diff = wcss[i]-wcss[i+1]
                percentage.append((diff/(wcss[i]))*100)

            n_cluster = 0
            for i in range(len(percentage)-1):
                if percentage[i] >50 and percentage[i+1] < 40:
                    n_cluster = i+2
                    break
            print("n_cluster",n_cluster )
            model = ModelFactory.update_property_of_class(instance_ref=initialized_model.model, 
                                                              property_data={"n_clusters" :n_cluster})
            model.fit(transformed_data)
            cluster_value = model.predict(transformed_data)
            model_slh_score = silhouette_score(transformed_data, cluster_value)
            print(model_slh_score)
            if model_slh_score > slh_score:
                return BestModel(model=model, slh_score=model_slh_score)
            else:
                raise Exception 
        except Exception as e:
            raise cs_exception(e, sys) from e

    def initiate_best_parameter_search_for_initialized_models(self,
                                                              initialized_model_list: List[InitializedModelDetail],
                                                              transformed_data, slh_score) -> List[GridSearchedBestModel]:

        try:
            best_model = None 
            for initialized_model_list in initialized_model_list:
                    best_model = self.initiate_best_parameter_search_for_initialized_model(
                    initialized_model=initialized_model_list,
                    transformed_data = transformed_data,
                    slh_score =slh_score
                )
            if best_model is not None:
                return best_model
            else:
                raise Exception 
        except Exception as e:
            raise cs_exception(e, sys) from e

    @staticmethod
    def get_model_detail(model_details: List[InitializedModelDetail],
                         model_serial_number: str) -> InitializedModelDetail:
        """
        This function return ModelDetail
        """
        try:
            for model_data in model_details:
                if model_data.model_serial_number == model_serial_number:
                    return model_data
        except Exception as e:
            raise cs_exception(e, sys) from e

    @staticmethod
    def get_best_model_from_grid_searched_best_model_list(grid_searched_best_model_list: List[GridSearchedBestModel],
                                                          slh_score, transformed_data
                                                          ) -> BestModel:
        try:
            best_model = None
            for grid_searched_best_model in grid_searched_best_model_list:
                if slh_score < silhouette_score(transformed_data,grid_searched_best_model.best_model.predict(transformed_data)):
                    logging.info(f"Acceptable model found:{grid_searched_best_model}")
                    slh_score = silhouette_score(transformed_data,grid_searched_best_model.predict(transformed_data))
                    best_model = grid_searched_best_model
            if not best_model:
                raise Exception(f"None of Model has silhouette_score: {slh_score}")
            logging.info(f"Best model: {best_model}")
            return best_model
        except Exception as e:
            raise cs_exception(e, sys) from e

    def get_best_model(self, transformed_data,slh_score) -> BestModel:
        try:
            logging.info("Started Initializing model from config file")
            initialized_model_list = self.get_initialized_model_list()
            logging.info(f"Initialized model: {initialized_model_list}")
            best_model = self.initiate_best_parameter_search_for_initialized_models(
                initialized_model_list=initialized_model_list,
                transformed_data = transformed_data,
                slh_score = slh_score
            )
            print(best_model)
            return best_model
        except Exception as e:
            raise (e, sys)

