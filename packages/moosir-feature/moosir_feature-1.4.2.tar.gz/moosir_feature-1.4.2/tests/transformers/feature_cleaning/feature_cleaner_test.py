import numpy as np
import pandas as pd
from pandas.util.testing import assert_frame_equal

from moosir_feature.transformers.feature_cleaning.feature_cleaner import *

import pytest


def test_normalize_should_scale_cols_separately():
    # arrange
    n_samples = 15
    min_value_f1 = -10
    max_value_f1 = -5

    min_value_f2 = 60000
    max_value_f2 = 70000

    data = {
        "feature_1": np.random.randint(low=min_value_f1, high=max_value_f1, size=n_samples),
        "feature_2": np.random.randint(low=min_value_f2, high=max_value_f2, size=n_samples)
    }

    data = pd.DataFrame(data=data)

    # act
    transformed, scaler = normalize(data=data)

    # assert
    dec_points = 5
    assert round(transformed["feature_1"].max(), dec_points) == 1
    assert round(transformed["feature_1"].min(), dec_points) == 0

    assert round(transformed["feature_2"].max(), dec_points) == 1
    assert round(transformed["feature_2"].min(), dec_points) == 0


def test_timestamp_ohlc_resample_should_work():
    # assrange
    open = [10, 20, 30, 40]
    high = [100, 200, 300, 400]
    low = [1, 2, 3, 4]
    close = [50, 60, 70, 80]
    inds = pd.date_range(start="2022/04/01", periods=4, freq="T")

    ohlc = pd.DataFrame({"Open": open, "High": high, "Low": low, "Close": close}, index=inds)
    ohlc.index.name = "Timestamp"

    # act
    result = timestamp_ohlc_resample(ohlc=ohlc, resample_freq="2T")

    # assert
    exp_inds = pd.date_range(start="2022/04/01", periods=2, freq="2T")
    expected = pd.DataFrame(data={"Open": [10, 30], "High": [200, 400], "Low": [1, 3], "Close": [60, 80]},
                            index=exp_inds)
    expected.index.name = "Timestamp"

    assert_frame_equal(result, expected)


def test_timestamp_ohlc_resample_should_consider_uneven_highs_lows():
    # assrange
    open = [10, 20, 30, 40]
    high = [200, 100, 300, 400]
    low = [2, 1, 3, 4]
    close = [50, 60, 70, 80]
    inds = pd.date_range(start="2022/04/01", periods=4, freq="T")

    ohlc = pd.DataFrame({"Open": open, "High": high, "Low": low, "Close": close}, index=inds)
    ohlc.index.name = "Timestamp"

    # act
    result = timestamp_ohlc_resample(ohlc=ohlc, resample_freq="2T")

    # assert
    exp_inds = pd.date_range(start="2022/04/01", periods=2, freq="2T")
    expected = pd.DataFrame(data={"Open": [10, 30], "High": [200, 400], "Low": [1, 3], "Close": [60, 80]},
                            index=exp_inds)
    expected.index.name = "Timestamp"

    assert_frame_equal(result, expected)


def test_timestamp_ohlc_resample_should_return_input_when_freq_bigger():
    # assrange
    sample_n = 5
    open = np.random.randint(0, 2, size=sample_n)
    high = np.random.randint(0, 2, size=sample_n)
    low = np.random.randint(0, 2, size=sample_n)
    close = np.random.randint(0, 2, size=sample_n)

    inds = pd.date_range(start="2022/04/01", periods=sample_n, freq="H")

    ohlc = pd.DataFrame({"Open": open, "High": high, "Low": low, "Close": close}, index=inds)
    ohlc.index.name = "Timestamp"

    # act
    result = timestamp_ohlc_resample(ohlc=ohlc, resample_freq="10T")

    # assert

    assert_frame_equal(result, ohlc)
