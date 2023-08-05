![PyPI - Python Version](https://img.shields.io/pypi/pyversions/privat_exchange_rates?style=for-the-badge) 

![PyPI - Developer](https://img.shields.io/badge/Developer-LesDev-orange) [![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger) ![PyPI - License](https://img.shields.io/github/license/lesykbiceps/nbu-exchange-rates)

**Official Repo:** https://github.com/lesykbiceps/nbu-exchange-rates

Welcome! Using this library you can collect exchange rates and reproduce this information in various forms. You can do various manipulations with the obtained data:
- Save the data in json or csv format
- Get graphs of how the exchange rate of a particular currency has changed
- Get the selected exchange rate

> Those who have access to data 
> have great opportunities

## Libraries

It uses the following libraries:

| Library | Link |
| ------ | ------ |
| Requests | https://pypi.org/project/requests/ |
| Matplotlib | https://pypi.org/project/matplotlib/ |

Why you need them?
- [Requests](https://pypi.org/project/requests/) for requests to exchange rates
- [matplotlib](https://pypi.org/project/matplotlib/) to draw a graph

## Additional info

Also you should have *python3-tk* installed or any of the matplotlib supported GUI backends
For example on Linux:
```bash
    sudo apt-get install python3-tk
```

# Quick Install / Usage

```bash
pip install nbu_exchange_rates
```

```python
import json
import csv

from datetime import datetime

from privat_exchange_rates import get_exchange_rates,format_time,to_json,to_csv,get_diagram


def main():
    exchange_rates = get_exchange_rates(datetime(day=19, month=4, year=2022), datetime(day=23, month=4, year=2022),
               currency='Євро')
    to_json(exchange_rates)
    to_csv(exchange_rates)
    get_diagram(exchange_rates)

   
    # Output:
    # Євро:31.6216 (19.04.2022)
    # Євро:31.5792 (20.04.2022)    
    # Євро:31.6787 (21.04.2022)    
    # Євро:31.8264 (22.04.2022)
``` 
![](images/img-diagram.png)     


# Available currencies
- USD | Долар США
- EUR | Євро
- PLN | Злотий
- GBP | Фунт стерлінгів
- TRY | Турецька ліра
- CAD | Канадський долар
- for more currencies follow this link https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date=20220402&json

## License

Data are taken from the link: https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date=20220402&json
MIT

**Free Software, Hell Yeah!**

