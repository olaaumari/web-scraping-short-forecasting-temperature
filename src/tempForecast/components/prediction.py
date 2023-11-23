from tempForecast.entity.config_entity import PredictionConfig
from pathlib import Path
import lightgbm as lgb
import pandas as pd
import joblib
from tempForecast.utils.common import save_json

class Prediction:
    def __init__(self, config: PredictionConfig):
        self.config = config
        self.model = joblib.load(self.config.trained_model_path)

    def predict(self):
        pred = self.model.predict()
        self.prediction = {"Prediction": pred}
        save_json(path=Path("prediction.json", data=self.prediction))