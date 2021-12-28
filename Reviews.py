# %%
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import json

def download_url_content():
    html = urlopen(URL)
    time.sleep(5)                                                                 # waits 5sec until webpage loads java script
    return html.read().decode("UTF-8")                                            # UTF-8 > character map

URL = "https://play.google.com/store/apps/details?id=com.fluffyfairygames.idleminertycoon&gl=DE&showAllReviews=true"  # URL is a constant is a vriable on a module level that should never be changed by code
data = download_url_content()                                                     # assigning to variable keeps code clean and readable

def bs_parsing_data():
    soup = BeautifulSoup(data, "html.parser")  
    comment_soup=soup.find("script", string=re.compile("vaf_game"))               # Every comment seems to include a type of "vaf_game" so this should work longtime
    return str(comment_soup)

def cleanup():
    crop=bs_parsing_data().split('data:')[-1]
    crop_complete=crop.removesuffix(', sideChannel: {}});</script>')              # can only be used on strings!!
    comment_collection= json.loads(crop_complete)                                 # parsed to list
    del comment_collection[-1]                                                    # delete last entry in list cause it has nothing to do with comments themselves
    return comment_collection

comment_list= []

def create_list():
    for comment in cleanup()[0]:                                             # already accessing level 0 by default
        if isinstance(comment[7],list):                                               # check if that instance is a list or None, if None, write new list with 2 None instances, if list, return list valies
            reply_details = comment[7]
        else: 
            reply_details = [None,None] 
        row={
            'pk': comment[0],                                                         # primary_key == unique identifier for every single row, cannot be duplicate
            'Name': comment[1][0],
            'Stars': comment[2],
            'Player_Comment': comment[4],
            'Game_Version': comment[10],
            'Company': reply_details[0],
            'Company_Reply': reply_details[1]
        }
        comment_list.append(row)
    return comment_list

def data_frame():        
    df=pd.DataFrame(create_list())
    return df

print(data_frame())

# %% [markdown]
# import necessary libraries
# 
# Download URL and sleep 5sec to load whole page
# 
# Parsing data with bs + finding comment list + transform bs object to string
# 
# Crop beginning and end pieces + load in json to create a list
# 
# Extracting available features in a loop
#     Checking for None features
#     Extracting features
#     Create data frame

# %% [markdown]
# # test
# test


