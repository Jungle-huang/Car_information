import os
import requests
from bs4 import BeautifulSoup
import json
import urllib.request
import argparse

def write_log_to_file(text,filename):
    f = open(path+filename +'.txt', 'a', encoding="utf-8")
    f.write(text + '\n')    
    
url = "https://mama1978777.pixnet.net/blog/post/96336596"

r = requests.get(url, headers={'User-Agent': 'Custom'})
r_trans = r.text.encode('iso-8859-1').decode('utf-8')
soup_info = BeautifulSoup(r_trans, 'html.parser')

data_count = (soup_info.title.text).find("更新出售")
date = (soup_info.title.text[0:data_count]).replace('/', '-')
date_filename = date + '.txt'
for info in soup_info.findAll('div', {"class": "article-content-inner"}):
    count_start = (info.text).find("現有車輛資訊表")
    count_end = (info.text).find("新 進 車")
    car_status = info.text[count_start:count_end]
    
title_final = "Car_Information"
if not os.path.isdir(title_final):os.mkdir(title_final)
path = os.getcwd() + '\\' + str(title_final) + '\\'    

if not os.path.isfile(path+date_filename):
    write_log_to_file(car_status,date)
    print("Creat the file : " + date_filename)
else:
    print("Exists File " + date_filename)

