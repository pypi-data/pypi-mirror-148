![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vk_exchange_rates?style=for-the-badge)

![PyPI - Developer](https://img.shields.io/badge/Developer-VitoldKliain-red)

**Official Repo:** https://gtlb.jetsoftpro.com/vitoldkliain/vk-exchange-rates

The library allows you to collect exchange rates from two Ukrainian banks: PrivatBank and National Bank of Ukraine. What
can you do:

- Get the exchange rate of each currency for a certain period
- Save data in csv and json format
- Get a graph how a currency changed in the selected period

## Libraries

It uses the following libraries:

- [requests](https://pypi.org/project/requests/) for requests to exchange rates
- [numpy](https://pypi.org/project/numpy/) to calculation for better data visualization
- [matplotlib](https://pypi.org/project/matplotlib/) to draw a graph
- [pandas](https://pypi.org/project/pandas/) to set a DataFrame

# Quick Install / Usage

```bash
pip install vk-exchange-rates
```

```python
from datetime import datetime

from vk_exchange_rates import get_exchange_rates, show_graph, save_to_csv, save_to_json


def main():
    get_exchange_rates(datetime(2022, 4, 20), datetime(2022, 4, 27))
    # show_graph(currency='PLN')
    # save_to_json(datetime(2022, 4, 25))
    # save_to_csv(datetime(2022, 4, 20), datetime(2022, 4, 27), currency='USD')

    # Output:
    # Exchange rates (sale) National Bank of Ukraine:
    # {'date': '20.04.2022', 'rates': {'AUD': 21.5418, 'CAD': 23.1906, 'CNY': 4.5801, 'HRK': 4.176, 'CZK': 1.293, ... }
    # Exchange rates (sale) PrivatBank:
    # {'date': '20.04.2022', 'rates': {'AZN': 17.2433, 'BYN': 10.6335, 'CAD': 23.1906, 'CHF': 33.82, 'CNY': 4.5801, ... }
```

# Most popular currencies

- USD
- EUR
- PLN
- GBP
- CHF
- CZK
