import pandas as pd
import time
import otherfunctions as of
import numpy as np

not_normalized = ["Open", "Close", "High", "Low", "Volume", "ma200", "ma50", "TRIX", "stochK", "stochD", "TRANGE",
                  "BBupperband", "BBmiddleband", "BBlowerband",
                  "ao", "cci", "coppock", "mom", "pgo", "alma", "dema", "wma", "fwma", "hma", "hwma", "jma", "kama",
                  "mcgd", "pwma", "sinwma", "swma", "t3", "tema", "trima", "vidya", "vwma", "zlma", "qstick", "vhf",
                  "atr", "massi", "pdist", "rvi", "ui", "ad", "adosc", "cmf", "efi", "obv", "pvt", "Market Cap", "DPC",
                  "Cumulative Return"]
normalized = ["ADX", "ADXR", "AROONOSC", "DX", "PPO", "ULTOSC", "MACD", "MACDSIG", "MACDHIS", "apo", "bias", "bop",
              "cfo", "cmo", "cti", "inertia", "psl", "roc", "rsi", "rsx", "willr", "chop", "increasing", "decreasing",
              "mfi", "pvr", "ebsw", "PriceUp", "PriceDown", "VIX", "VVIX", "VXN"]


def tanh_normalization(unnormalized_data):
    m = np.mean(unnormalized_data, axis=0)
    std = np.std(unnormalized_data, axis=0)
    normalized_data = 0.5 * (np.tanh(0.01 * ((unnormalized_data - m) / std)) + 1)
    return normalized_data


def normdist_normalization(unnormalized_data):
    m = np.mean(unnormalized_data, axis=0)
    std = np.std(unnormalized_data, axis=0)
    normalized_data = (unnormalized_data - m) / std
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
    normalized_data = (unnormalized_data - min(unnormalized_data)) / (max(unnormalized_data) - min(unnormalized_data))
    return normalized_data


def normalize_dates():
    for index, date in enumerate(dates):
        print(f"currently at {index + 1} out of {len(dates)}")
        df = pd.read_csv(f"./dates/{date}.csv")
        for column in not_normalized:
            unnormalized_data = df[f'{column}']
            normalized_data = normdist_normalization(unnormalized_data)
            df[f'{column}'] = normalized_data
        df.to_csv(f"./dates/{date}.csv")

if __name__ == '__main__':
    t1 = time.perf_counter()
    tickers = of.get_tickers()
    dates = of.get_dates(tickers)
    normalize_dates()
    t2 = time.perf_counter()
    print(f'Finished in {t2 - t1} seconds')
