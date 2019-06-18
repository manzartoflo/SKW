#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 13:16:00 2019

@author: manzar
"""

import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from urllib.parse import urljoin

wb = webdriver.FirefoxProfile()
wb.set_preference("javascript.enabled", True)
driver = webdriver.Firefox(wb)
urls = 'https://www.skw-cds.ch/'
#tag-list vertical
driver.get(urls)
html = driver.execute_script('return document.documentElement.outerHTML')
text = '/html/body/main/section[2]/div[1]/div[1]/div/div/form[2]/div[2]/div/button'
find = driver.find_element_by_xpath(text)
find.click()
html = driver.execute_script('return document.documentElement.outerHTML')
soup = BeautifulSoup(html, 'lxml')
links = soup.findAll('div', {'class': 'tag-list vertical'})
li = links[0].findAll('li')
url = []
for link in li:
    url.append(urljoin(urls, link.a.attrs['href']))

header = 'Company Name, email, telephone, Website\n'
file = open('assignment.csv', 'w')
file.write(header)
for hyper in url:
    req = requests.get(hyper)
    soup = BeautifulSoup(req.text, 'lxml')
    p = soup.findAll('div', {'class': 'description'})
    name = soup.findAll('h4')
    name = name[0].text
    tel = []
    for i in p[0].p.contents:
        if('\n' in i):
            if( not any(c.isalpha() for c in i.split('\n')[1].replace(' ', ''))):
                tel.append(i.split('\n')[1].replace(' ', ''))
        if('@' in i):
            email = i
        if('www' in i):
            web = i
    print(name, tel, email, web)
    file.write(name.replace(',', '').replace('\n', '').replace(' ', '') + ', ' + email.replace('\n', '').replace(' ', '') + ', ')
    count = 0
    for t in tel:
        if(count == len(tel) - 1):
            file.write(t)
        else:
            file.write(t + ' | ')
        count += 1
    file.write(', ' + web.replace('\n', '').replace(' ', '') + '\n')
file.close()
file = pd.read_csv('assignment.csv') 