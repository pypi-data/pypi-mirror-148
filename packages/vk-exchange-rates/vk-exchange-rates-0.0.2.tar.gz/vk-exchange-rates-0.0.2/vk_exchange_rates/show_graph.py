from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from vk_exchange_rates.exchange_rates import get_api_data


def show_graph(start_date: datetime = datetime(2022, 4, 22),
               end_date: datetime = datetime.now(), currency: str = 'EUR'):
    """Show a graph how a currency changed in the selected period
           Example:
                >> show_graph(datetime(2022,4,22), datetime(2022,4,26), currency='PLN')
           Args:
             start_date: Start of period
             end_date : The end of period
             currency : Selected currency
           Returns:
             Exchange rates
       """
    data = get_api_data(start_date, end_date)
    hist_data = []

    for row in data:
        hist_dict = {'date': row['date'], currency: row['rates'][currency]}
        hist_data.append(hist_dict)
        print(hist_dict)

    df = pd.DataFrame(hist_data)
    x1 = df['date'][:len(df) // 2]
    y1 = df[currency][:len(df) // 2]
    x2 = df['date'][len(df) // 2:]
    y2 = df[currency][len(df) // 2:]

    fig = plt.figure(figsize=(15, 6))

    plt.xticks(rotation=90)
    plt.xticks(np.arange(0, len(hist_data), 5))

    plt.title(f'Exchange rate {currency}')
    plt.xlabel('date', fontsize=12)
    plt.ylabel(f'rate', fontsize=12)

    plt.plot(x2, y2, color='g', label='PrivatBank')
    plt.plot(x1, y1, color='r', label='NBU')

    plt.legend()
    plt.show()
