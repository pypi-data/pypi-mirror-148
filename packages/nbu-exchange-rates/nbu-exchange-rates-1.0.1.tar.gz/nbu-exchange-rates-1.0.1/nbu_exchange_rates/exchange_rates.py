import json
import csv

from datetime import datetime, timedelta

import requests
import matplotlib.pyplot as plt


BANK_API_URL = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date={date}&json'


def format_time(date_start, date_end):  # Get time in necessary format
    formatted_date_start = date_start.strftime("%Y%m%d")  # "20220419" (yearmonthday)
    formatted_date_end = date_end.strftime("%Y%m%d")  # "20220423" (yearmonthday)

    date_obj_start = datetime.strptime(formatted_date_start, "%Y%m%d")
    date_obj_end = datetime.strptime(formatted_date_end, "%Y%m%d")
    delta = (date_obj_end - date_obj_start).days

    return date_obj_start, delta


def get_exchange_rates(date_start: datetime, date_end: datetime, currency):

    """Get information about NBU exchange rates for the selected date range
    The first datatime is responsible for the beginning of the date range and the second for the end
           Example:
                >> get_exchange_rates(datetime(day=19, month=4, year=2022), datetime(day=23, month=4, year=2022),
                    currency='Євро'
           Args:
             date_start: The beginning of the period,
             date_end : The end of period
             currency : Selected currency from the list in readme.md
           Returns:
             Exchange rates in specific format(currency:rate).
       """

    date = format_time(date_start, date_end)
    date_obj_start = date[0]
    delta = date[1]
    dates = []
    for d in range(delta):  # Create a list of dates
        today = date_obj_start.date() + timedelta(days=d)
        dates.append(today.strftime("%Y%m%d"))
    data = []

    for dateIndex in range(len(dates)):  # Get the necessary data
        res = requests.get(BANK_API_URL.format(date=dates[dateIndex]))
        datas = [x for x in res.json() if x['txt'] == currency]
        data.append(datas)

    for dat in range(len(dates)):  # Get rates in specific format(currency:rate)
        message = f"{data[dat][0]['txt']}:{data[dat][0]['rate']} ({data[dat][0]['exchangedate']})"
        print(message)

    return data


def to_json(data):  # json data storage
    """
        Example:
            >> to_json(exchange_rates)
        Args:
            data : previously created function object(exchange_rates)
        Result: created json file
    """
    with open('exchange_rates.json', 'w') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)


def to_csv(data):  # csv data storage
    """
           Example:
               >> to_сsv(exchange_rates)
           Args:
               data : previously created function object(exchange_rates)
           Result: created сsv file
       """
    lst = []
    with open('exchange_rates.csv', 'w', newline='') as csv_file:
        for line in data:                                          # Get the right data structure for writing in csv
            lst.append(line[0])
        columns = set(i for d in line for i in d)                  # Delete duplicate currency
        writer = csv.DictWriter(csv_file, fieldnames=columns)
        writer.writeheader()
        for row in lst:
            writer.writerow(row)


def get_diagram(data):  # Plot how a certain currency changed in the selected period
    """
            Example:
                >> get_diagram(exchange_rates)
            Args:
                data : previously created function object(exchange_rates)
            Result: the chart window opens
    """
    lst_date = []
    lst_rate = []

    for line in data:                               # Create a list of dates
        lst_date.append(line[0]['exchangedate'])
    for line in data:                               # Create a list of rates
        lst_rate.append(line[0]['rate'])
    currency = data[0][0]['cc']
    x_list = lst_date                               # x-axis(date)
    y_list = lst_rate                               # y-axis(rate)
    plt.title(f'Exchange rates({currency})')
    plt.xlabel('date')
    plt.ylabel('rate, UAH')
    plt.plot(x_list, y_list, marker='o')
    plt.show()
