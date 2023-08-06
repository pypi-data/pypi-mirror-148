from datetime import datetime, timedelta

import requests

BANK_NBU_API_URL = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date={date}&json'
BANK_PB_API_URL = 'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}'


def get_current_date(start_date, end_date, bank_url):
    delta = end_date - start_date

    for day in range(delta.days + 1):
        current_day = start_date + timedelta(days=day)
        if bank_url == BANK_NBU_API_URL:
            yield current_day.strftime("%Y%m%d")
        elif bank_url == BANK_PB_API_URL:
            yield current_day.strftime("%d.%m.%Y")


def to_dict(exchange_rates: list):
    hist_data = {currency: sale_rate for (_, currency, sale_rate) in exchange_rates}
    result = {
        "date": exchange_rates[1][0],
        'rates': hist_data,
    }
    return result


def get_api_data(start_date, end_date):
    session = requests.Session()

    print('Exchange rates (sale) National Bank of Ukraine:')
    for date in get_current_date(start_date, end_date, BANK_NBU_API_URL):
        response = session.get(BANK_NBU_API_URL.format(date=date))
        exchange_rates_nbu = []

        for row in response.json():
            tmp = row["exchangedate"], row["cc"], row["rate"]
            exchange_rates_nbu.append(tmp)

        result = to_dict(exchange_rates_nbu)
        yield result

    print('\nExchange rates (sale) PrivatBank:')
    for date in get_current_date(start_date, end_date, BANK_PB_API_URL):
        response = session.get(BANK_PB_API_URL.format(date=date))
        exchange_rates_pb = []
        current_date = response.json()['date']

        for row in response.json()['exchangeRate'][1:]:
            if 'saleRate' in row:
                tmp = current_date, row["currency"], row["saleRate"]
                exchange_rates_pb.append(tmp)
            else:
                tmp = current_date, row["currency"], row["saleRateNB"]
                exchange_rates_pb.append(tmp)

        result = to_dict(exchange_rates_pb)
        yield result


def get_exchange_rates(start_date: datetime = datetime(2022, 4, 22),
                       end_date: datetime = datetime.now()):
    """Get information about NBU and PrivatBank exchange rates for the selected date range
           Example:
                >> get_exchange_rates(datetime(2022,4,22), datetime(2022,4,26))
           Args:
             start_date: Start of period
             end_date : The end of period
           Returns:
             Exchange rates
       """

    data = get_api_data(start_date, end_date)

    for row in data:
        print(row)
