from tempForecast.entity.config_entity import TrainingConfig
from pathlib import Path
import lightgbm as lgb
import pandas as pd
from tempForecast.components.data_transformation import WeatherDatabase
import joblib


class Training:
    def __init__(self, config: TrainingConfig):
        self.config = config
        self.train, self.test = WeatherDatabase().split_train_test(pd.read_csv("artifacts\data_ingestion\data.csv", index_col='datetime'))

    def get_base_model(self):
        print("Chemin du modèle à charger:", self.config.base_model_path)
        #self.model = lgb.Booster(model_file=str(self.config.base_model_path))
        self.model = lgb.LGBMRegressor()

    @staticmethod
    def save_model(path: Path, model):
        # Vérifier le type du modèle (LightGBM ou autre)
        if isinstance(model, lgb.LGBMRegressor):
            # Sauvegarder le modèle LightGBM
            model.save_model(str(path))
        else:
            # Sauvegarder un modèle TensorFlow (ou autre)
            model.save(path)

    def train_model(self):
        

        self.model.fit(
            self.train.drop(columns='température'),
            self.train['température']
            
        )
        
        joblib.dump(self.model, self.config.trained_model_path)