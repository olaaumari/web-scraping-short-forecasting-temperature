from tempForecast.entity.config_entity import TrainingConfig
from pathlib import Path
import lightgbm as lgb
import pandas as pd
from tempForecast.components.data_transformation import WeatherDatabase
import joblib
from tempForecast.components.pipeline_transformation import pipe
import numpy as np


class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.train, self.test = pd.read_csv("artifacts/data_ingestion/train.csv", index_col='datetime'), pd.read_csv("artifacts/data_ingestion/test.csv", index_col='datetime')

        self.data =  pd.read_csv("artifacts/data_ingestion/train.csv", index_col='datetime')
        self.train.index = pd.to_datetime(self.train.index) 
        self.test.index = pd.to_datetime(self.test.index) 

        X_train = self.train
        X_test = self.test
        y_train = self.train['température']
        y_test = self.test['température']
     

        self.X_train_t = WeatherDatabase().fit_transform_pipe(X_train)
        self.X_test_t = WeatherDatabase().transform_pipe(X_test)
       
        self.y_train_t = y_train.loc[self.X_train_t.index]


    def get_base_model(self, model):
        print("Chemin du modèle à charger:", self.config.base_model_path)
        self.model = model

    @staticmethod
    def save_model(path: Path, model):
        if isinstance(model, lgb.LGBMRegressor):
            model.save_model(str(path))
        else:
            model.save(path)

    def train_model(self):
        

        self.model.fit(
            self.X_train_t,
            np.reshape(self.y_train_t, (-1,1))
        )
        
        joblib.dump(self.model, self.config.trained_model_path)