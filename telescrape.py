import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import os
import glob

def get_image_url(a_image):

    url_list = []
    for this_a_image in a_image:
        #get style string from the image anchor tag
        style_str = this_a_image.attrs['style']
        
        ## find url in style string
        regex_search = re.compile("url\(\'(.*)\'\)")
        matches = re.search(regex_search, style_str)
        matching_url = matches[1]
        url_list.append(matching_url)

    # return the image urls
    return url_list

def get_caption_text(div_caption):
    # find all text not within <>
    regex = re.compile(".*?\>(.*?)\<")
    result = re.findall(regex, str(div_caption))
    
    # concat all the resulting strings
    caption_text = ''.join(result)
    
    # return the resulting caption text
    return caption_text
  
def telescrape(url):
        
    # default to a blank row if we return nothing
    new_row = pd.DataFrame({'datetime': [],
                            'image_url': [],
                            'caption': []})
    
    # open url
    resp = requests.get(url)

    # if we get response code 200 we can proceed
    if resp.status_code == 200:

        # parse html
        soup = bs(resp.text,'html.parser')    
        
        try:
            # find message
            div_message = soup.find("div",{"class":"tgme_widget_message"})
            
            # find image anchor tag by class
            a_image = div_message.find_all("a",{"class":"tgme_widget_message_photo_wrap"})
            # get the url to this image
            url = get_image_url(a_image)
    
            # find text caption
            div_caption = div_message.find("div",{"class":"tgme_widget_message_text"})
            caption = get_caption_text(div_caption)
    
            # find the datetime of the post
            time = div_message.find("time", {"class":"time"})
            datetime = time.attrs['datetime']
    
            #print(url,caption,datetime)
        
            new_row = pd.DataFrame({'datetime': [datetime],
                                    'image_url': [url],
                                    'caption': [caption]})
        
        except AttributeError: # when we get a_image as None there's nothing to read
            pass

    else:
        print("Error", resp.status_code)
        
    return new_row
  
def telescrape_loop(telegram_username, n, n0=0, out_file=None, download_images=False, image_filepath_prefix=None):

    # create empty dataframe
    df = pd.DataFrame({'datetime': [],
                       'image_url': [],
                       'caption': [],
                       'url': []})

    # loop through posts to scrape
    for i in range(n0,n+1):
        # target url 
        url = f'https://t.me/s/{telegram_username}?before={i}'
        print('scraping ', url)
        # scrape new row
        new_row = telescrape(url)
        new_row['url'] = url
        # append to dataframe
        df = df.append(new_row, ignore_index = True)
        if download_images == True:
            try:
                datetime_string = new_row.datetime[0].replace(':','')[:-5]
                url_n = new_row.url[0].split('=')[-1]
                # check if images were already downloaded
                search_existing_images = glob.glob(f'{image_filepath_prefix}{datetime_string}_*.jpg')
                if len(search_existing_images) == 0:
                    for i, this_image_url in enumerate(new_row.image_url[0]):
                        filename = f'{image_filepath_prefix}{datetime_string}_{url_n}_{i}.jpg'
                        print('saving ', filename)
                        os.system(f'wget -O {filename} {new_row.image_url[0][i]}')
            except (KeyError, IndexError):
                pass
    
    # drop any duplicate rows    
    df.drop_duplicates(subset='datetime', inplace=True)
    df.reset_index(inplace=True)
    if out_file != None:
        # export result 
        print('saving to file', out_file)
        df.to_csv(out_file)
    
    return df
    
