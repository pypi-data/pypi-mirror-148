import csv
from datetime import datetime

from vk_exchange_rates.exchange_rates import get_api_data


def save_to_csv(start_date: datetime = datetime(2022, 4, 22),
                end_date: datetime = datetime.now(), currency: str = 'EUR'):
    """Save NBU and PrivatBank exchange rates for the selected date range to csv format
           Example:
                >> save_to_csv(datetime(2022,4,22), datetime(2022,4,26), currency='PLN')
           Args:
             start_date: Start of period
             end_date : The end of period
             currency : Selected currency
           Returns:
             Exchange rates
       """

    data = get_api_data(start_date, end_date)

    with open("vk_exchange_rates.csv", "w") as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerow(["Date", f"Sale ({currency})"])
        for row in data:
            hist_dict = {'date': row['date'], currency: row['rates'][currency]}
            print(hist_dict)
            writer.writerow([item[1] for item in hist_dict.items()])

    print("\nFile successfully created")
