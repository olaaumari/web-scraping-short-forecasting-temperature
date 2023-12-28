from tempForecast.constants import *
import os 
import pandas as pd
from pathlib import Path
from tempForecast.utils.common import read_yaml, create_directories
from tempForecast.entity.config_entity import ( DataIngestionConfig,
                                                PrepareBaseModelConfig,
                                                TrainingConfig,
                                                EvaluationConfig,
                                                PredictionConfig)



class ConfigurationManager:
    def __init__(
        self,
        config_filepath = CONFIG_FILE_PATH):
        #params_filepath = PARAMS_FILE_PATH):

        self.config = read_yaml(config_filepath)
        #self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])



    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            local_data_file=config.local_data_file,
            root_dir_train = config.root_dir_train,
            root_dir_test = config.root_dir_test
        )

        return data_ingestion_config
    

    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        config = self.config.prepare_base_model
        
        create_directories([config.root_dir])

        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path)
            
        )

        return prepare_base_model_config
    

    def get_training_config(self) -> TrainingConfig:
        training = self.config.training
        prepare_base_model = self.config.prepare_base_model
        #params = self.params
        training_data = self.config.data_ingestion.root_dir_train
        create_directories([
            Path(training.root_dir)
        ])

        training_config = TrainingConfig(
            root_dir=Path(training.root_dir),
            base_model_path=Path(training.base_model_path),
            root_dir_train=Path(training.root_dir_train),
            root_dir_test=Path(training.root_dir_test),
            trained_model_path=Path(training.trained_model_path),
            training_data=Path(training_data),
           
        )

        return training_config
    

    def get_validation_config(self) -> EvaluationConfig:
        eval_config = EvaluationConfig(
            path_of_model=Path("artifacts/training/model.txt"),
            training_data=Path("artifacts/data_ingestion/train"), # a modifer et mettre les données dans la db
            test_data=Path("artifacts/data_ingestion/test.csv")
        )
        return eval_config

    def get_prediction_config(self) -> PredictionConfig:
        training = self.config.training
        prediction = self.config.prediction
        prepare_base_model = self.config.prepare_base_model
        #params = self.params
        training_data = self.config.data_ingestion.root_dir_train
        create_directories([
            Path(training.root_dir)
        ])

        prediction_config = PredictionConfig(
            path_of_model=Path(training.base_model_path),
            training_data=Path(training.root_dir_train),
            test_data=Path(training.root_dir_test),
            trained_model_path=Path(training.trained_model_path),
           
        )
        return prediction_config