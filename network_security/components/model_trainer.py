import os, sys
import mlflow
import numpy as np

from network_security.logging.logger import logging
from network_security.entity.config_entity import ModelTrainerConfig
from network_security.utils.ml_utils.model.estimator import NetworkModel
from network_security.utils.main_utils.utils import load_numpy_array_data, evaluate_models
from network_security.exception.exception import NetworkSecurityException
from network_security.utils.main_utils.utils import save_object, load_object, load_numpy_array_data
from network_security.utils.ml_utils.metric.classification_metric import get_classification_score
from network_security.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
# from network_security.constant import training_pipeline


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
                AdaBoostClassifier, 
                GradientBoostingClassifier, 
                RandomForestClassifier
                )

# Copy this ccode from DagsHub
import dagshub
dagshub.init(   repo_owner = 'htetaunglynn94', 
                repo_name = 'E2E-Network-Security-ETL-Pipeline', 
                mlflow = True)


class ModelTrainer:
    def __init__(self, 
                data_transformation_artifact: DataTransformationArtifact,
                model_trainer_config: ModelTrainerConfig):
        try:
            self.model_trainer_conf = model_trainer_config
            self.dt_artifact = data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def track_mlflow(self, model, classification_metric):
        try:
            with mlflow.start_run():
                f1_score = classification_metric.f1_score
                precision_score = classification_metric.precision_score
                recall_score = classification_metric.recall_score

                mlflow.log_metric("f1_score", f1_score)
                mlflow.log_metric("precision_score", precision_score)
                mlflow.log_metric("recall_score", recall_score)
                mlflow.sklearn.log_model(model, name="best_model")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def train_model(self, x_train, y_train, x_test, y_test):
        """
        Hyperparameter tuning for multiple machine learning models using GridSearchCV:
        - select the best-performing model based on evaluation reports
        - computes classification metrics for both train and test sets
        - wraps the model with its data preprocessor and 
        - saves it as an artifact

        Args:
            x_train (np.ndarray): Training input features.
            y_train (np.ndarray): Training target labels.
            x_test (np.ndarray): Testing input features.
            y_test (np.ndarray): Testing target labels.

        Returns:
            ModelTrainerArtifact: Contains the file path of the trained network model 
                                  and the classification metric artifacts for train and test sets.
        """

        ## Multiple ML models
        models = {
                    "Random Forest": RandomForestClassifier(verbose=1, n_jobs=-1),
                    "Decision Tree": DecisionTreeClassifier(),
                    "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                    "Logistic Regression": LogisticRegression(verbose=1),
                    "AdaBoost": AdaBoostClassifier() 
                }

        ## Hyperparameters
        params = {  "Decision Tree": {  'criterion':['gini','entropy','log_loss'],
                                        'splitter': ['best','random'],
                                        'max_features': ['sqrt','log2']
                                     },
                    "Random Forest": {  'n_estimators': [8,16,32,64,128,256],
                                        # 'criterion': ['gini','entropy','log_loss'],
                                        'max_features': ['sqrt','log2',None],
                                     },
                    "Gradient Boosting": {
                                            'learning_rate': [.1,.01,.05,.001],
                                            'loss': ['log_loss', 'exponential'],
                                            # 'subsample': [0.6,0.7,0.8,0.85,0.9],
                                            # 'criterion': ['squared_error','friedman_mse'],
                                            # 'max_features': ['auto','sqrt','log2'],
                                            'n_estimators': [8,16,32,128,256]
                                         },
                    "Logistic Regression": {},
                    "AdaBoost": {   'learning_rate': [.1,.01,.05,.001],
                                    'n_estimators': [8,16,32,64,128,256]}
        }

        ## 1. Evaluate models with hyperparameter tuning
        model_report:dict = evaluate_models(x_train = x_train, 
                                            y_train = y_train, 
                                            x_test = x_test, 
                                            y_test = y_test,
                                            models = models,
                                            params = params)

        ## 2. Identify the best model based on performance scores
        best_model_name = max(model_report, key=model_report.get)
        best_model = models[best_model_name]

        ## 3. Generate predictions
        y_train_pred = best_model.predict(x_train)
        y_test_pred  = best_model.predict(x_test)

        ## 4. Calculate classification metric artifacts
        classfication_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)
        classification_test_metric = get_classification_score(y_true=y_test, y_pred=y_test_pred)

        ## 5. Implement MLflow tracking here if required
        self.track_mlflow(best_model, classfication_train_metric)
        self.track_mlflow(best_model, classification_test_metric)

        ## 6. Load preprocessor, wrap it with the best model, and save to disk
        preprocessor = load_object(file_path=self.dt_artifact.transformed_object_path)
        model_path = self.model_trainer_conf.trained_mdl_fp
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        network_model = NetworkModel(preprocessor=preprocessor, model=best_model)
        save_object(file_path=model_path, obj=network_model)

        ## Model pusher
        # save_object("final_model/ml_model.pkl", best_model)
        save_object(self.model_trainer_conf.mt_final_model, best_model)

        ## 7. Build and return the final model trainer artifact
        model_trainer_artifact = ModelTrainerArtifact(
                                    trained_model_path = model_path,
                                    train_metric_artifact = classfication_train_metric,
                                    test_metric_artifact = classification_test_metric)
                                    # final_model_path = self.model_trainer_conf.mt_final_model,
                                    # final_ml_model_name = self.model_trainer_conf.mt_final_model)

        logging.info("Model trainer artifact: %s" % model_trainer_artifact)
        return model_trainer_artifact
                      

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_fp = self.dt_artifact.transformed_train_path
            test_fp  = self.dt_artifact.transformed_test_path

            # Load training and testing array
            train_arr = load_numpy_array_data(train_fp)
            test_arr  = load_numpy_array_data(test_fp)

            x_train, y_train, x_test, y_test = (train_arr[:,:-1], 
                                                train_arr[:, -1], 
                                                test_arr[:, :-1], 
                                                test_arr[:,  -1])

            model_trainer_artifact = self.train_model(x_train, y_train, x_test, y_test)
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)