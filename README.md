# telescrape
a simple telegram media scraper to dump image urls, caption text, and timestamps into a csv

not efficient or elegant

## usage:

```python
import telescrape as ts

# pick a telegram username to scrape
telegram_username = 'SomeUser'

# grab just the most recent stuff as a single-row pandas df
df = ts.telescrape(telegram_username)

# try to grab everything and save to a csv file
ts.telescrape_loop(telegram_username, 'SomeUser.csv')
```

## requirements:
* requests
* bs4
* re
* pandas
