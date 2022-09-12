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


stock_a_prices = get_adj_prices("TSLA.csv")
stock_b_prices = get_adj_prices("LMT.csv")


def get_avg_and_sd(x):
    p_returns = []
    p_value = 1
    stock_b_shares = x / stock_b_prices[0]
    stock_a_shares = (1 - x) / stock_a_prices[0]

    for i in range(1, len(stock_a_prices)):
        new_p_value = stock_b_shares * \
            stock_b_prices[i] + stock_a_shares * stock_a_prices[i]
        p_returns.append((new_p_value - p_value) / p_value)

        p_value = new_p_value
        stock_b_shares = (p_value * x) * (1 / stock_b_prices[i])
        stock_a_shares = (p_value * (1 - x)) * (1 / stock_a_prices[i])

    return_avg = sum(p_returns) / len(p_returns)
    return_sd = math.sqrt(
        sum((r - return_avg)**2 for r in p_returns) / len(p_returns))
    return return_avg, return_sd


# Plotting
plot_x = []
plot_y = []

min_sd = float("inf")
min_sd_x = None
min_sd_avg = None

NUM_POINTS = 100

for i in range(1, NUM_POINTS):
    x = i / NUM_POINTS
    avg, sd = get_avg_and_sd(x)
    plot_x.append(sd)
    plot_y.append(avg)
    if sd < min_sd:
        min_sd = sd
        min_sd_x = x
        min_sd_avg = avg

print("MVP standard deviation:", min_sd)
print("MVP expected returns", min_sd_avg)
print("MVP split:", min_sd_x, "to", 1 - min_sd_x)

plt.rcParams["figure.figsize"] = [7.00, 7.00]
plt.rcParams["figure.autolayout"] = True
plt.xlim(0, 0.3)
plt.ylim(0, 0.06)
plt.grid()
plt.plot(plot_x, plot_y, marker="o", markersize=1,
         markeredgecolor="red", markerfacecolor="None", linestyle="None")
plt.show()
