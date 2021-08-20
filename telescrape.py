import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

def get_image_url(a_image):

    #get style string from the image anchor tag
    style_str = a_image.attrs['style']
    
    # find url in style string
    regex_search = re.compile("url\(\'(.*)\'\)")
    matches = re.search(regex_search, style_str)
    matching_url = matches[1]

    # return the image url
    return matching_url

def get_caption_text(div_caption):
    # find all text not within <>
    regex = re.compile(".*?\>(.*?)\<")
    result = re.findall(regex, str(div_caption))
    
    # concat all the resulting strings
    caption_text = ''.join(result)
    
    # return the resulting caption text
    return caption_text
  
def telescrape(telegram_username):
    
    url = f'https://t.me/s/{telegram_username}'
    
    # default to a blank row if we return nothing
    new_row = pd.DataFrame({'datetime': [],
                                 'url': [],
                                 'caption': []})
    
    # open url
    resp = requests.get(url)

    # if we get response code 200 we can proceed
    if resp.status_code == 200:

        # parse html
        soup = bs(resp.text,'html.parser')    
        
        try:
            # find image anchor tag by class
            a_image = soup.find("a",{"class":"tgme_widget_message_photo_wrap"})
            # get the url to this image
            url = get_image_url(a_image)
    
            # find text caption
            div_caption = soup.find("div",{"class":"tgme_widget_message_text"})
            caption = get_caption_text(div_caption)
    
            # find the datetime of the post
            time = soup.find("time", {"class":"time"})
            datetime = time.attrs['datetime']
    
            #print(url,caption,datetime)
        
            new_row = df = pd.DataFrame({'datetime': [datetime],
                                         'url': [url],
                                         'caption': [caption]})
        
        except AttributeError: # when we get a_image as None there's nothing to read
            pass

    else:
        print("Error", resp.status_code)
        
    return new_row
  
def telescrape_loop(telegram_username, out_file):

    # create empty dataframe
    df = pd.DataFrame({'datetime': [],
                       'url': [],
                       'caption': []})

    # loop through posts to scrape
    for i in range(0,10000):
        # target url 
        url = f'https://t.me/s/{telegram_username}?before={i}'
        print('scraping ', url)
        # scrape new row
        new_row = pfscrape(url)
        # append to dataframe
        df = df.append(new_row, ignore_index = True)
    
    # drop any duplicate rows    
    df.drop_duplicates(subset='datetime', inplace=True)
    # export result    
    df.to_csv(out_file)
    
    return None
    
