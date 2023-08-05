from krakentren import *
from pathlib import Path
import pandas as pd

pair = Coin("XXBTZEUR")


def read_csv_file(file_name):
    """Retreive pandas dataframe from csv file

    Args:
        file_name (str): name of the file

    Returns:
        pandas Dataframe: Pandas Dataframe from csv file
    """
    file_name = Path(__file__).parent / str(file_name + ".csv")
    data = pd.read_csv(file_name)
    return data


data = pair.get_ohlc_data("15")
# data = read_csv_file("ohlc_data")

add_ta(data,
       sma1={'indicator': 'sma', 'period': 3},
       sma2={'indicator': 'sma', 'period': 9},
       mfi={'indicator': 'mfi', 'period': 14},
       psl={'indicator': 'psl', 'period': 9},
       chop={'indicator': 'chop', 'period': 15},
       roc={'indicator': 'roc', 'period': 17},
       adl={'indicator': 'adl'},
       psar={'indicator': 'psar', 'af': 0.040, 'max_af': 0.40})

print(data)
