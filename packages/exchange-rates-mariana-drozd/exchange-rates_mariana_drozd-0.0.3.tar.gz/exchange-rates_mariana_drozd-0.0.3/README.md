![PyPI - Python Version](https://img.shields.io/pypi/pyversions/exchange_rates_mariana_drozd?style=for-the-badge)

**Official Repo:** https://gtlb.jetsoftpro.com/mariana.drozd/exchange_rates_mariana_drozd

It uses the following libraries:

- [Requests](https://pypi.org/project/requests/) for requests to exchange rates
- [Pandas](https://pypi.org/project/pandas/) for working with tables
- [Matplotlib](https://pypi.org/project/matplotlib/) for plots

# Quick Install / Usage

```bash
pip install exchange_rates_mariana_drozd
```

```python
from datetime import datetime

from exchange_rates_mariana_drozd import get_exchange_rates_from_date_to_date


def main():
    exchange_rates_from_date_to_date = get_exchange_rates_from_date_to_date(
        datetime(day=15, month=4, year=2019),
        datetime(day=20, month=4, year=2019),
        currency="USD",
        save_to_csv_file=False,
        save_to_json_file=False,
        show_plot=False
    )

    print(exchange_rates_from_date_to_date)

 # Output:
 #    {
 # "15.04.2019": {
 #  "date": "15.04.2019",
 #  "bank": "PB",
 #  "baseCurrency": 980,
 #  "baseCurrencyLit": "UAH",
 #  "exchangeRate": [
 #   {
 #    "baseCurrency": "UAH",
 #    "currency": "UZS",
 #    "saleRateNB": 0.003243,
 #    "purchaseRateNB": 0.003243
 #   },
 #   {
 #    "baseCurrency": "UAH",
 #    "currency": "BYN",
 #    "saleRateNB": 12.64203,
 #    "purchaseRateNB": 12.64203
 #   },
 #   {
 #    "baseCurrency": "UAH",
 #    "currency": "TMT",
 #    "saleRateNB": 7.774029,
 #    "purchaseRateNB": 7.774029
 #   },
 #    ...
```
## Note:

### If you need to save data in CSV or/and JSON file, set needed parameter (```save_to_csv_file``` and/or ```save_to_json_file```) to "True".
### Also, if you want to see plot of selected currency, set ```show_plot``` to "True"

### Example of USD currency plot:
![](/home/mariana/Документи/exchange_rates_mariana_drozd/static/myplot.png)
