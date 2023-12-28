from feature_engine.creation import CyclicalFeatures
from feature_engine.datetime import DatetimeFeatures
from feature_engine.imputation import DropMissingData
from feature_engine.selection import DropFeatures
from feature_engine.timeseries.forecasting import (
    LagFeatures,
    WindowFeatures,
    ExpandingWindowFeatures
    
)

from sklearn.pipeline import Pipeline


dtf = DatetimeFeatures(
    # the datetime variable
    variables="index",
    
    # the features we want to create
    features_to_extract=[
        "month",
        "week",
        "day_of_week",
        "day_of_month",
        "hour",
        "minute",
        "weekend",
    ],
)

# Lag features.

lagf = LagFeatures(
    variables=["température",'vent', 'rafales'],  # the input variables
    freq=["1H","2H"],  # move 1 hr and 24 hrs forward
    missing_values="ignore",
)

# Window features

winf = WindowFeatures(
    variables=["température"],  # the input variables
    window="3H",  # average of 3 previous hours
    freq="1H",  # move 1 hr forward
    missing_values="ignore",
)

# Periodic features

cyclicf = CyclicalFeatures(
    # The features we want to transform.
    variables=["month", "hour"],
    # Whether to drop the original features.
    drop_original=False,
)

# Drop original time series

drop_ts = DropFeatures(features_to_drop=["température",'vent','rafales'])

# Drop missing data
imputer = DropMissingData()

exp_w = ExpandingWindowFeatures(
    functions=["mean", "max", "std"],
    variables=['température'],
    

)

pipe = Pipeline(
    [
        ("datetime_features", dtf),
        ("lagf", lagf),
        #("window", exp_w),
        ("winf", winf),
        ("Periodic", cyclicf),
        ("drop_ts", drop_ts),
        ("dropna", imputer),

    ]
)