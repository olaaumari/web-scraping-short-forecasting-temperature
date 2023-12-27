from tempForecast.components.prediction import Prediction
from tempForecast.config.configuration import ConfigurationManager


# Configuration
config = ConfigurationManager()
prediction_config = config.get_prediction_config()

# Prediction
pred = Prediction(config=prediction_config)

# Metric evaluation
pred.save_score()


