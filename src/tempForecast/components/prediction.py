from tempForecast.entity.config_entity import PredictionConfig
from tempForecast.components.data_transformation import WeatherDatabase
from tempForecast.components.pipeline_transformation import pipe
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error

from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from tempForecast.utils.common import save_json

import matplotlib.pyplot as plt

class Prediction:
    def __init__(self, config: PredictionConfig):
        self.config = config
        self.model = joblib.load(self.config.trained_model_path)
        
        self.train, self.test = pd.read_csv("artifacts/data_ingestion/train.csv", index_col='datetime'), pd.read_csv("artifacts/data_ingestion/test.csv", index_col='datetime')
        self.data =  pd.read_csv("artifacts/data_ingestion/train.csv", index_col='datetime')
        self.data.index = pd.to_datetime(self.data.index)
        
        date_index = self.data.index[-144]
        # input data
        X_train = self.data[self.data.index < date_index]
        X_test = self.data[self.data.index >= pd.Timestamp(date_index) - pd.offsets.Hour(24)]
        
        # target
        y_train = self.data[self.data.index < date_index][["température"]]
        y_test = self.data[self.data.index >= pd.Timestamp(date_index) - pd.offsets.Hour(24)][[
            "température"
        ]]
        
        self.X_train_t = WeatherDatabase().fit_transform_pipe(X_train)
        
        self.X_test_t = WeatherDatabase().transform_pipe(X_test)


        y_train_t = y_train.loc[self.X_train_t.index]
        # The first hour of forecast.
        forecast_point = pd.Timestamp(date_index)

        # The forecasting horizon (24 hs ahead)
        forecast_end = forecast_point + pd.offsets.Hour(23)

        index = pd.date_range(
            start=forecast_point,
            end=forecast_end,
            freq="10T",
        )

        f_horizon = pd.DataFrame(columns=['température'], index=index)

        start_point = forecast_point - pd.offsets.Hour(24)


        input_data = X_test[(X_test.index >= start_point) & (X_test.index < forecast_point)]

        input_data.loc[forecast_point] = np.nan

        for i in range(200):
            try:
                # Re-slice the input data
                start_point = start_point + pd.offsets.Minute(10)
                forecast_point = forecast_point + pd.offsets.Minute(10)
                
                input_data = input_data[(input_data.index >= start_point)]
               
                input_data.loc[forecast_point] = np.nan
                # Obtain the prediction
                pred = self.model.predict(pipe.transform(pd.DataFrame(input_data[['température','vent', 'rafales']].dropna())))
                # Add prediction to horizon.
                f_horizon.loc[forecast_point, 'température'] = pred[0][0]
                input_data.loc[forecast_point, 'y_pred'] = pred[0][0]
            except:
                pass

     
        tmp = pd.DataFrame(f_horizon["température"]).join(
        X_test["température"], lsuffix="_left", rsuffix="_right")

        tmp.columns = ["predicted", "actual"]
        tmp['actual'].fillna(method='bfill', inplace=True)
        tmp.plot()

        plt.ylabel("temperature")
        plt.savefig('graphique.png')


        mae =  mean_absolute_error(tmp.dropna()['predicted'], tmp.dropna()['actual'])
        mape =  mean_absolute_percentage_error(tmp.dropna()['predicted'], tmp.dropna()['actual'])
        self.score = mae, mape
        

    def save_score(self):
        scores = {"MAE": self.score[0], "MAPE": self.score[1]}
        save_json(path=Path("scores.json"), data=scores)