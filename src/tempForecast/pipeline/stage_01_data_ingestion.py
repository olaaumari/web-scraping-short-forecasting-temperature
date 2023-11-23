from tempForecast.config.configuration import ConfigurationManager

from tempForecast.components.data_ingestion import weather_scraping
from tempForecast.components.data_transformation import WeatherDatabase
import pandas as pd

STAGE_NAME = "Data Ingestion stage"





class DataIngestionTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        # on charge les données déjà dans la base
        data = weather_scraping().load_data()
        # on instancie la classe avec la base de donnée déjà chargé pour ne pas rescrapé tout
        data_ingestion = weather_scraping(last_df=data)
        # scraping 
        data = data_ingestion.web_scraping()
        # il faut ajouter cette base à la db
        data_ingestion.load_data(df=data)
        data = WeatherDatabase().load_data_and_transform()
        # Note verifer que toutes les dates sont présentes
        # cad tout les jours ou voire toutes les heures de tout les jours sont présent dans le dataset
        train, test = WeatherDatabase().split_train_test(df=data)
        train.to_csv(data_ingestion_config.root_dir_train)
        test.to_csv(data_ingestion_config.root_dir_test)
        test.to_csv(data_ingestion_config.root_dir_test)
        #data.set_index('datetime', inplace=True)
        data.to_csv(data_ingestion_config.local_data_file, index=False)
        print(train)

        return data
    

if __name__ == '__main__':
    obj = DataIngestionTrainingPipeline()
    data = obj.main()