from lxml import html
import requests
import re
import pandas as pd


names = []
description = []

def scraper():
    for i in range(3):
        url = 'https://www.holidify.com/places/delhi/sightseeing-and-things-to-do.html?pageNum=' + str(i)
        resp = requests.get(url=url,
                            headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'})

        tree = html.fromstring(resp.text)

        # print(resp.text)

        locations = tree.xpath(
            "//div[@class='container']/div[contains(@class,'no')]/div[1]/div[4]/div[4]/div[@class='col-12 col-md-6 pr-md-3']")

        for location in locations:
            names.append(location.xpath('.//div/a/h3/text()')[0])
            description.append(location.xpath(".//div/div[@class='card-body']/p[@class='card-text']/text()")[0])


scraper()
d = {'Place_Name' : names, 'Description' : description}

places = pd.DataFrame(data=d)

places['Place_Name'] = places['Place_Name'].apply(lambda x: re.sub("[^A-Za-z']+"," ",x).strip())

#print(places)

places.to_csv('delhi_sightseeing.csv')
