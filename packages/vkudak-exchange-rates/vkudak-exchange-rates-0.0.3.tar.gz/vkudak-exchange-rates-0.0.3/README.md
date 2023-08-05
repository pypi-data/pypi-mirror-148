![PyPI - Python Version](https://img.shields.io/pypi/pyversions/privat_exchange_rates?style=for-the-badge)

**Official Repo:** https://gtlb.jetsoftpro.com/vkudak/vkudak-exchange-rates

It uses the following libraries:

- [Requests](https://pypi.org/project/requests/) for requests to exchange rates
- [Pandas](https://pypi.org/project/pandas/) for greate html to table parse
- [Matplotlib](https://pypi.org/project/matplotlib/) for plots
# Quick Install / Usage

```bash
pip install vkudak-exchange-rates
```

```python
from datetime import datetime

from vkudak_exchange_rates import get_exchange_rates, get_curr_rates_on_time_interval


def main():
    curr = "USD" 
    my_date = datetime(day=21, month=4, year=2022)
    exchange_rates = get_exchange_rates(my_date, curr)

    print(exchange_rates)
    # Output:
    # {
    # datetime.datetime(2022, 4, 20, 0, 0): 
    #   {
    #   'Приватбанк': [29.255, 32.18], <-- purchase, sale
    #   'Ощадбанк': [29.5, 32.18]
    #   }
    # }
    
    start_date = datetime(day=20, month=4, year=2022)
    end_date = datetime(day=24, month=4, year=2022)
    step = 1
    res = get_curr_rates_on_time_interval(curr, start_date, end_date, step, save_to="csv", plot=True)
    
    print(res)
    # Output:
    # {
    #     datetime.datetime(2022, 4, 20, 0, 0): {'Приватбанк': [29.255, 32.18], 'Ощадбанк': [29.5, 32.18]}, 
    #     datetime.datetime(2022, 4, 21, 0, 0): {'Приватбанк': [29.255, 32.18], 'Ощадбанк': [29.5, 32.18]}, 
    #     datetime.datetime(2022, 4, 22, 0, 0): {'Приватбанк': [29.255, 32.18], 'Ощадбанк': [29.8, 32.18]}, 
    #     datetime.datetime(2022, 4, 23, 0, 0): {'Приватбанк': [29.255, 32.18], 'Ощадбанк': [29.8, 32.18]}, 
    #     datetime.datetime(2022, 4, 24, 0, 0): {'Приватбанк': [29.255, 32.18], 'Ощадбанк': [29.8, 32.18]}
    # }


```