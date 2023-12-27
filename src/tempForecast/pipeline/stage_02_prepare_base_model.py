from tempForecast.config.configuration import ConfigurationManager
from tempForecast.components.base_model import PrepareBaseModel
from tempForecast import logger

from sklearn.multioutput import MultiOutputRegressor
from sklearn.linear_model import Lasso



STAGE_NAME = "Prepare base model"


class PrepareBaseModelTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfigurationManager()
        prepare_base_model_config = config.get_prepare_base_model_config()
        prepare_base_model = PrepareBaseModel(config=prepare_base_model_config)

        lasso = MultiOutputRegressor(Lasso(random_state=0, alpha=1))

        prepare_base_model.get_base_model(lasso)





if __name__ == '__main__':
    try:
        logger.info(f"*******************")
        logger.info(f">>>>>> stage {STAGE_NAME} started <<<<<<")
        obj = PrepareBaseModelTrainingPipeline()
        obj.main()
        logger.info(f">>>>>> stage {STAGE_NAME} completed <<<<<<\n\nx==========x")
    except Exception as e:
        logger.exception(e)
        raise e