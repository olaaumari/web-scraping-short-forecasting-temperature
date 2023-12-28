from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    root_dir_train: Path
    root_dir_test: Path
    local_data_file: Path
   


@dataclass(frozen=True)
class PrepareBaseModelConfig:
    root_dir: Path
    base_model_path: Path
    # ajout de paramètres 



@dataclass(frozen=True)
class TrainingConfig:
    root_dir: Path
    base_model_path : Path
    trained_model_path: Path
    root_dir_train: Path
    root_dir_test: Path
    training_data: Path

    # Paramètres



@dataclass(frozen=True)
class EvaluationConfig:
    path_of_model: Path
    training_data: Path
    test_data: Path
    

@dataclass(frozen=True)
class PredictionConfig:
    path_of_model: Path
    training_data: Path
    test_data: Path
    trained_model_path : Path
    