from tempForecast.config.configuration import ConfigurationManager
from tempForecast.components.data_ingestion import weather_scraping
from tempForecast.components.data_transformation import WeatherDatabase

import pandas as pd
import matplotlib.pyplot as plt

STAGE_NAME = "Data Ingestion stage"





class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        # Configuration
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()

        # load data already in the database
        data = weather_scraping().load_data()
        # we instantiate the class with the database already loaded so as not to rescrap everything
        data_ingestion = weather_scraping(last_df=data)
        # scraping 
        data = data_ingestion.web_scraping()
        # we add data to the database
        data_ingestion.load_data(df=data)

        # small transformation
        data = WeatherDatabase().load_data_and_transform()
        data.datetime = pd.to_datetime(data.datetime)

       
        # data cleaning
        data['température'].fillna(method='bfill', inplace=True)
        data['vent'].fillna(method='bfill', inplace=True)
        data['rafales'].fillna(0, inplace=True)
        data['vent_direction'].fillna(0, inplace=True)
        data['pt_de_rosee'].fillna(0, inplace=True)
        data['humidite'].fillna(0, inplace=True)
        data.drop(columns=['bio_meteo','radiation_solaire', 'id', 'datetime'], inplace=True)
        data.index = pd.to_datetime(data.index)

        # Data splitting
        date_index = data.index[-144]
        train = data[data.index < date_index]
        test = data[data.index >= pd.Timestamp(date_index) - pd.offsets.Hour(24)]
        
        
        # Note verifer que toutes les dates sont présentes
        # cad tout les jours ou voire toutes les heures de tout les jours sont présent dans le dataset
       
        # Exportation
        train.to_csv(data_ingestion_config.root_dir_train)
        test.to_csv(data_ingestion_config.root_dir_test)
        data.to_csv(data_ingestion_config.local_data_file, index=False)

        # Data visualisation
        plt.plot(data['température'])
        plt.savefig('data.jpg')
        
        return data
    

if __name__ == '__main__':
    obj = DataIngestionTrainingPipeline()
    data = obj.main()









