import json
from datetime import datetime

from vk_exchange_rates.exchange_rates import get_api_data


def save_to_json(start_date: datetime = datetime(2022, 4, 22),
                 end_date: datetime = datetime.now()):
    data = get_api_data(start_date, end_date)
    """Save NBU and PrivatBank exchange rates for the selected date range in json format
           Example:
                >> save_to_json(datetime(2022,4,22), datetime(2022,4,26))
           Args:
             start_date: Start of period
             end_date : The end of period
           Returns:
             Exchange rates
       """

    with open("vk_exchange_rates.json", "w") as file:
        for row in data:
            print(row)
            file.write(json.dumps(row, indent=4))

    print("\nFile successfully created")
