from pathlib import Path
from tempForecast.entity.config_entity import EvaluationConfig
from tempForecast.utils.common import save_json
import joblib
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error
import pandas as pd
from tempForecast.components.data_transformation import WeatherDatabase

class Evaluation:
    def __init__(self, config: EvaluationConfig):
        self.config = config


    @staticmethod
    def load_model(path: Path) -> lgb.LGBMRegressor:
        return joblib.load(path)
    

    def evaluation(self):
        model = self.load_model(self.config.path_of_model)
        self.train, self.test = WeatherDatabase().split_train_test(pd.read_csv("artifacts\data_ingestion\data.csv", index_col='datetime'))
        self.pred = model.predict(self.test.drop(columns='température'))
        self.score = mean_absolute_error(self.pred, self.test['température']), mean_absolute_percentage_error(self.pred, self.test['température']), mean_squared_error(self.pred, self.test['température'])
        
        

    def save_score(self):
        scores = {"MAE": self.score[0], "MAPE": self.score[1],"MSE": self.score[2]}
        save_json(path=Path("scores.json"), data=scores)