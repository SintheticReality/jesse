from collections import namedtuple

import numpy as np
from scipy.signal import argrelextrema

from jesse.helpers import get_config, np_ffill

EXTREMA = namedtuple('EXTREMA', ['min', 'max', 'last_min', 'last_max'])


def minmax(candles: np.ndarray, order: int = 3, sequential: bool = False) -> EXTREMA:
    """
    minmax - Get extrema

    :param candles: np.ndarray
    :param order: int - default = 3
    :param sequential: bool - default=False

    :return: EXTREMA(min, max, last_min, last_max)
    """
    warmup_candles_num = get_config('env.data.warmup_candles_num', 240)
    if not sequential and len(candles) > warmup_candles_num:
        candles = candles[-warmup_candles_num:]

    low = candles[:, 4]
    high = candles[:, 3]

    minimaIdxs = argrelextrema(low, np.less, order=order, axis=0)
    maximaIdxs = argrelextrema(high, np.greater, order=order, axis=0)

    min = np.full_like(low, np.nan)
    max = np.full_like(high, np.nan)

    # set the extremas with the matching price
    min[minimaIdxs] = low[minimaIdxs]
    max[maximaIdxs] = high[maximaIdxs]

    # forward fill Nan values to get the last extrema
    last_min = np_ffill(min)
    last_max = np_ffill(max)

    if sequential:
        return EXTREMA(min, max, last_min, last_max)
    else:
        return EXTREMA(min[-1], max[-1], last_min[-1], last_max[-1])

