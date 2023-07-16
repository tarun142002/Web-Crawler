from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import csv
import pymongo

myclient = pymongo.MongoClient("mongodb+srv://tushar:UcfsrFDx0RmfIQmq@cluster0.zc9dglx.mongodb.net/")
mydb = myclient["test"]
mycol = mydb["users"]
mydict = {"name": "John", "address": "Highway 37"}
x = mycol.insert_one(mydict)

app = Flask(__name__, template_folder='template', static_url_path='/static', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

def scrape_websites(medicine_name):
    scraped_data = []

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # pharmeasy.in
    url_pharmeasy = f'https://pharmeasy.in/search/all?name={medicine_name}'
    response = requests.get(url_pharmeasy, headers=header).content
    soup = BeautifulSoup(response, 'lxml')
    # Extract images from pharmeasy.in
    images_pharmeasy = soup.select('.ProductCard_medicineImgDefault__Q8XbJ')
    for j in range (len(images_pharmeasy)):
        image_url = images_pharmeasy[j]
        scraped_data.append({'website': 'pharmeasy', 'image_url': image_url})
    
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

    # 1mg.com
    url_1mg = f'https://www.1mg.com/search/all?name={medicine_name}'
    response = requests.get(url_1mg, headers=header).text
    soup = BeautifulSoup(response, 'lxml')
    # Extract images from 1mg.com
    images_1mg = soup.select('.style__product-image___3weAd')
    for i in range(len (images_1mg)):
        image_url = images_1mg[i]
        scraped_data.append({'website': '1mg', 'image_url': image_url})

    return scraped_data

def save_to_csv(scraped_data):
    fieldnames = ['website', 'image_url']
    filename = 'scraped_data.csv'
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write each row of data (website and image URL)
        writer.writerows(scraped_data)

@app.route('/get_data', methods=['POST'])
def get_data():
    medicine_name = request.form['medicine_name']

    # Web scraping and saving images
    scraped_data = scrape_websites(medicine_name)
    save_to_csv(scraped_data)
    return render_template('result.html', data=scraped_data)

if __name__ == '__main__':
    app.run(debug=True)
