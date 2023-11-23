import lightgbm as lgb
import joblib
from pathlib import Path
from tempForecast.entity.config_entity import PrepareBaseModelConfig


class PrepareBaseModel:
    def __init__(self, config: PrepareBaseModelConfig):
        self.config = config

    def get_base_model(self):
        self.model = lgb.LGBMRegressor()
        self.save_model(path=self.config.base_model_path, model=self.model)

    @staticmethod
    def save_model(path: Path, model):
        if isinstance(path, str):
            path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, path)