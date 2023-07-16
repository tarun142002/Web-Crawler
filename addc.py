
from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import csv

medicine_name  = input()
scraped_data = []

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # 1mg.com
url_netmeds = f'https://www.netmeds.com/catalogsearch/result/{medicine_name}/all'
response = requests.get(url_netmeds, headers=header).text
soup = BeautifulSoup(response, 'lxml')
# Extract images from 1mg.com
# images_netmed = soup.select('img[src^="https://www.netmeds.com/images/product-v1/150x150"]')
images_netmeds = soup.find_all("img")
# print(images_netmeds)
for i in range(len (images_netmeds)):
    image_url = images_netmeds[i]
    scraped_data.append({'website': 'netmeds', 'image_url': image_url})

print(scraped_data)
