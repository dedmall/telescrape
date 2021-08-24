# telescrape
a simple telegram media scraper to dump image urls, caption text, and timestamps into a csv (and optionally wget images)

not efficient or elegant

## usage:

```python
import telescrape as ts

# pick a telegram username to scrape
telegram_username = 'SomeUser'

# grab everything and save to a csv file
df = ts.telescrape_loop(telegram_username, n, n0, out_file='SomeUser.csv', download_images=True, image_filepath_prefix='images/')
```

## requirements:
* requests
* bs4
* re
* pandas
* os
* glob
