import pandas as pd
import yfinance as yf
import time
import otherfunctions as of
import numpy as np


def tanh_normalization(unnormalized_data):
    m = np.mean(unnormalized_data, axis=0)
    std = np.std(unnormalized_data, axis=0)
    normalized_data = 0.5 * (np.tanh(0.01 * ((unnormalized_data - m) / std)) + 1)
    return normalized_data


def sigmoid_normalization(unnormalized_data):
    normalized_data = []
    for x in unnormalized_data:
        normalized_data.append(1 / (1 + np.exp(-x)))
    return normalized_data


def median_normalization(unnormalized_data):
    m = np.median(unnormalized_data, axis=0)
    normalized_data = unnormalized_data / m
    return normalized_data


def min_max_normalization(unnormalized_data):
    normalized_data = (unnormalized_data-min(unnormalized_data))/(max(unnormalized_data)-min(unnormalized_data))
    return normalized_data


def get_normalization_columns():
    pass


def normalize_dates():
    for date in dates:
        for column in normcol:
            df = pd.read_csv(f'./dates/{date}')
            unnormalized_data = df[f'{column}']
            normalized_data = tanh_normalization(unnormalized_data)
            df[f'{column}'] = normalized_data


if __name__ == '__main__':
    t1 = time.perf_counter()
    tickers = of.get_tickers()
    dates = of.get_dates()
    normcol = get_normalization_columns()
    normalize_dates()
    t2 = time.perf_counter()
    print(f'Finished in {t2 - t1} seconds')
