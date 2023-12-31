from tempForecast.config.configuration import ConfigurationManager
from tempForecast.components.training import Training
from tempForecast import logger

from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import Lasso

STAGE_NAME = "Training"


class ModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        training_config = config.get_training_config()
        training = Training(config=training_config)
        print("training", training)

        # Model
        lasso = MultiOutputRegressor(Lasso(random_state=0, alpha=1))

        training.get_base_model(lasso)
        training.train_model()
        


if __name__ == '__main__':
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = ModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e