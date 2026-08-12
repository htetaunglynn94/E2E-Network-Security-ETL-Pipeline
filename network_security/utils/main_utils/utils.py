import numpy as np
import os, sys, yaml, dill, pickle

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, 'rb') as yf:
            return yaml.safe_load(yf)
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def write_yaml_file(file_path:str, content:object, replace:bool=False) -> None:
    try:
        if os.path.isdir(file_path):
            os.rmdir(file_path)
            
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as yf:
            yaml.dump(content, yf)

    except Exception as e:
        raise NetworkSecurityException(e, sys)

def save_numpy_array_data(file_path:str, array:np.array) -> None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)

    except Exception as e:
        raise NetworkSecurityException(e, sys)

def save_object(file_path:str, obj:object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")

    except Exception as e:
        raise NetworkSecurityException(e, sys)

def load_object(file_path:str) -> object:
    try:
        dir_name = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        if not os.path.exists(file_path):
            raise Exception(f"File name, {file_name} does not exist in this {dir_name}.")
        with open(file_path, "rb") as file:
            return pickle.load(file)

    except Exception as e:
        raise NetworkSecurityException(e, sys)

def load_numpy_array_data(file_path:str) -> np.array:
    try:
        dir_name = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        if not os.path.exists(file_path):
            raise Exception(f"File name, {file_name} does not exist in this {dir_name}.")
        with open(file_path, "rb") as file:
            return np.load(file)
    
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def evaluate_models(x_train,y_train,x_test,y_test,models,params):
    try:
        report = {}

        for name, model in models.items():
            para = params[name]

            gs = GridSearchCV(model, para, cv=3)
            gs.fit(x_train, y_train)
            model.set_params(**gs.best_params_)
            model.fit(x_train, y_train)
            y_train_pred = model.predict(x_train)
            y_test_pred  = model.predict(x_test)
            train_model_score = r2_score(y_test, y_test_pred)
            test_model_score  = r2_score(y_test, y_test_pred)
            report[name] = test_model_score
            
        return report
            

    except Exception as e:
        raise NetworkSecurityException(e, sys)