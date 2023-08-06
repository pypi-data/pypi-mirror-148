import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta
import pandas as pd

import requests

BANK_API_URL = 'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'

dates = []
response = {}
currencies = []
purchase_rate, sale_rate, purchase_rate_NB, sale_rate_NB = [], [], [], []


def get_exchange_rates_from_date_to_date(date1: datetime,
                                         date2: datetime,
                                         currency: str,
                                         save_to_json_file=False,
                                         save_to_csv_file=False,
                                         show_plot=False) -> dict:
    """
    Get information on cash exchange rates of PrivatBank and the NBU on the selected range of dates.

             Example:
                  >>> get_exchange_rates_from_date_to_date(
                  datetime(day=15, month=4, year=2022),
                  datetime(day=18, month=4, year=2022),
                  currency="USD"
                  save_to_json_file=True,
                  save_to_csv_file=True,
                  show_plot=False)

             Args:
               date1: Start date of date range
               date2: End date of date range
               currency: Enter currency lit you want to show in plot
               save_to_json_file: True | False Save data to JSON file
               save_to_csv_file: True | False Save data into CSV file
               show_plot: True | False Show plot information about selected currency


             Returns:
               Exchange rates for every day in selected range of dates.
        """

    for n in range(int((date2 - date1).days) + 1):
        my_date = date1 + timedelta(n)
        dates.append(my_date.strftime("%d.%m.%Y"))

    for date in dates:
        res = requests.get(BANK_API_URL.format(date=date)).json()
        response[date] = res

    if save_to_json_file:
        save_to_json()

    if save_to_csv_file:
        save_to_csv()

    if show_plot:
        show_plot_info(currency)

    return response


def save_to_json(filename="data.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False, indent=1)

    print(f"Data is saved to file '{filename}'.")
    return filename


def save_to_csv(filename="data.csv"):
    for key, value in response.items():
        f = pd.json_normalize(response[key]["exchangeRate"])
        dataframe = pd.DataFrame(f)
        dataframe.insert(0, "date", key)
        dataframe.to_csv(filename, mode="a", index=False)

    print(f"Data is saved to file '{filename}'.")

    return filename


def prepare_data_to_plot(currency):
    for key, value in response.items():
        dataframe = pd.DataFrame(pd.json_normalize(response[key]["exchangeRate"]).fillna(0))
        search_curr_data = dataframe.loc[dataframe["currency"] == currency]
        sale_rate.append(float(search_curr_data["saleRate"]))
        purchase_rate.append(float(search_curr_data["purchaseRate"]))
        sale_rate_NB.append(float(search_curr_data["saleRateNB"]))
        purchase_rate_NB.append(float(search_curr_data["purchaseRateNB"]))


def show_plot_info(currency):
    prepare_data_to_plot(currency)
    plt.plot(dates, sale_rate, color='c', label='Sale PrivatBank')
    plt.plot(dates, purchase_rate, color='y', label='Purchase PrivatBank')
    plt.plot(dates, sale_rate_NB, color='g', label='Sale NBU')
    plt.plot(dates, purchase_rate_NB, color='r', label='Purchase NBU')
    plt.title(f"{currency} Currency Rates")
    plt.legend()
    plt.show()
