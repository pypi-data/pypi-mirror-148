from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import requests
import pandas as pd
from pylab import rcParams


rcParams['figure.figsize'] = 12, 6

# https://minfin.com.ua/ua/currency/banks/eur/2022-03-11/
MINFIN_URL = 'https://minfin.com.ua/ua/currency/banks/{curr}/{date}/'

# you can add more banks from url "MINFIN_URL"
BANKS = ["Приватбанк", "Ощадбанк"]


def get_exchange_rates(date, curr):
    """Get information on cash exchange rates on the selected date.

        Example:
             >>> get_exchange_rates(datetime(day=21, month=4, year=2022), "USD")

        Args:
          date: Selected date exchange rates,
          curr: currency string (eg: "USD", "EUR")

        Returns:
          Exchange rates list.
    """
    formatted_date = date.strftime("%Y-%m-%d")  # "2022-04-20" (year-month-day)
    rr = requests.get(MINFIN_URL.format(curr=curr, date=formatted_date))
    table = pd.read_html(rr.text)
    df = table[-1]  # we need last table on the page

    # rename columns
    df.columns = ['BankName', 'purchase', ' ', 'sale', "", "", "", "", ""]

    res_list = {}
    # print(df)
    for bank in BANKS:
        try:
            purch = df[df["BankName"] == bank]["purchase"].values[0]
            sale = df[df["BankName"] == bank]["sale"].values[0]
            res_list[bank] = [purch, sale]
        except IndexError:
            print(f"No data for bank {bank} on date {date}")
            res_list[bank] = [-99, -99]
    return res_list


def prepare_df(dt, y):
    df_save = pd.DataFrame()
    df_save["date"] = dt
    for bank in BANKS:
        purch = [x[bank][0] for x in y]
        sale = [x[bank][1] for x in y]
        df_save[bank + "_purchase"] = purch
        df_save[bank + "_sale"] = sale
    return  df_save


def get_curr_rates_on_time_interval(curr, date_start, date_end, step_d, save_to=None, plot=False):
    """
    Example:
        >>> date_st = datetime(day=10, month=1, year=2022)
        >>> date_e = datetime(day=22, month=4, year=2022)
        >>> stepd = 10
        >>> get_curr_rates_on_time_interval("USD", date_st, date_e, stepd, save_to="csv", plot=True)
    Args:
        curr: currency string (eg: "USD", "EUR")
        date_start: start date exchange rates,
        date_end: end date exchange rates,
        step_d: step for date exchange rates in DAYS,
        save_to: csv | json  Save to file
        plot: Plot image for each bank from BANKS variable

    Returns:
        date_rates_dict: dict
    """
    date = date_start
    date_rates_dict = {}

    while date <= date_end:
        # print(date, date_end, date <= date_end)
        date_rates_dict[date] = get_exchange_rates(date, curr)
        date = date + timedelta(days=step_d)

    dt, y = zip(*date_rates_dict.items())

    if save_to == "csv":
        df_save = prepare_df(dt, y)
        df_save.to_csv(f'{curr}.csv', index=False)

    if save_to == "json":
        df_save = prepare_df(dt, y)
        with open(f"{curr}.json", "w", encoding='utf-8') as fs:
            df_save.to_json(fs, orient="records", date_format="iso", lines=True, force_ascii=False)

    if plot:
        plt.figure(figsize=(12, 6))
        for bank in BANKS:
            purch = [x[bank][0] for x in y]
            sale = [x[bank][1] for x in y]
            plt.clf()
            plt.title(bank + " " + curr)
            plt.xlabel("date")
            plt.ylabel("course amount")
            plt.plot(dt, purch, "k-", label='purchase')
            plt.plot(dt, sale, "b--", label='sale')
            plt.legend()
            plt.show()

    return date_rates_dict


# if __name__ == "__main__":
#     start_date = datetime(day=20, month=4, year=2022)
#     end_date = datetime(day=24, month=4, year=2022)
#     step = 1
#     drl = get_curr_rates_on_time_interval("USD", start_date, end_date, step, plot=False, save_to="json")
#     print(drl)
