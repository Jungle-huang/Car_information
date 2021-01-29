import os
import requests
from bs4 import BeautifulSoup
import json
import urllib.request
import argparse
import difflib
import datetime

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

def write_log_to_file(text,filename):
    f = open(path+filename +'.txt', 'a', encoding="utf-8")
    f.write(text + '\n')    
    
print("-----Creat File-----")
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

#compare
print("\n-----Compare File-----")
file_couont = 0
file_array = []
for i in os.listdir(path):
    htm_txt = i.find('html')
    if (htm_txt==-1):
        file_couont+=1
        date_txt = i.replace('.txt',"")
        file_array.append(datetime.datetime.strptime(date_txt,'%Y-%m-%d').date().strftime("%Y-%#m-%#d"))
        
if (file_couont>=2):
    #get near two files
    for i in range(file_couont-1):
        for j in range(file_couont-i-1):
            if file_array[j]>file_array[j+1]:
                temp = file_array[j]
                file_array[j] = file_array[j+1]
                file_array[j+1] = temp

    a = file_array[file_couont-1]
    b = file_array[file_couont-2]
    
    print("File#1 %s \nFile#2 %s" % (a,b))
    compare_file = a + "_" + b +'.html'
    if not os.path.isfile(path+compare_file):
        file1 = str(path+str(a) + '.txt')
        file2 = str(path+str(b) + '.txt')
        f1 = open(file1, encoding="utf-8")
        f2 = open(file2, encoding="utf-8")
        diff = difflib.HtmlDiff()
        result = diff.make_file(f1, f2)
        
        compare_file = a + "_" + b +'.html'
        with open(path + compare_file, 'w', encoding="utf-8") as result_file:
            result_file.write(result)

        print("Creat compare file" + compare_file )
    else:
        print("Compare file exist.")
else:
    print("Just a file, Can't compare file.")



