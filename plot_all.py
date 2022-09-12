from random import random
import csv
import math
from matplotlib import pyplot as plt

ADJ_CLOSE_COLUMN_INDEX = 5


def get_adj_prices(csv_path):
    prices = []
    with open(csv_path) as file:
        reader = csv.reader(file)
        for row in reader:
            if reader.line_num > 1:
                prices.append(float(row[ADJ_CLOSE_COLUMN_INDEX]))
    return prices


stock_tickers = ("TSLA", "LMT", "GOOG", "JPM", "UNH", "XOM")
stock_histories = tuple(
    get_adj_prices(ticker + ".csv") for ticker in stock_tickers
)


def get_avg_and_sd(weights):
    p_returns = []
    p_value = 1
    stock_shares = tuple(
        weights[s_i] / stock_histories[s_i][0] for s_i in range(len(stock_tickers))
    )
    for i in range(1, len(stock_histories[0])):
        new_p_value = sum(stock_histories[s_i][i] *
                          stock_shares[s_i] for s_i in range(len(stock_tickers)))

        p_returns.append((new_p_value - p_value) / p_value)

        p_value = new_p_value

        stock_shares = tuple(p_value * (weights[s_i] /
                             stock_histories[s_i][i]) for s_i in range(len(stock_tickers)))

    return_avg = sum(p_returns) / len(p_returns)
    return_sd = math.sqrt(
        sum((r - return_avg)**2 for r in p_returns) / len(p_returns))
    return return_avg, return_sd


# Plotting
plot_x = []
plot_y = []

min_sd = float("inf")
min_sd_weights = None
min_sd_avg = None

NUM_RANDOM_PORTFOLIOS = 100000


for i in range(NUM_RANDOM_PORTFOLIOS):
    non_normalized_weights = tuple((random()*2)**2 for _ in stock_tickers)
    normalized_weights = tuple(w / sum(non_normalized_weights)
                               for w in non_normalized_weights)
    avg, sd = get_avg_and_sd(normalized_weights)

    plot_x.append(sd)
    plot_y.append(avg)
    if sd < min_sd:
        min_sd = sd
        min_sd_weights = normalized_weights
        min_sd_avg = avg

print("MVP standard deviation:", min_sd)
print("MVP expected returns", min_sd_avg)
print("MVP Weights:", " ".join(
    f"{stock_tickers[s_i]}: {min_sd_weights[s_i]}" for s_i in range(len(stock_tickers))))

plt.rcParams["figure.figsize"] = [7.00, 7.00]
plt.rcParams["figure.autolayout"] = True
plt.xlim(0, 0.3)
plt.ylim(0, 0.06)
plt.grid()
plt.plot(plot_x, plot_y, marker="o", markersize=1,
         markeredgecolor="red", markerfacecolor="None", linestyle="None")
plt.show()
