# -*- coding: utf-8 -*-
import scrapy
import re
import json
from datetime import date
today = date.today()
d1 = today.strftime("%d/%m/%Y")
url_end = '&offset={}'
i = 0

class HifiKlubbenSpider(scrapy.Spider):    
    name = 'hifiklubben'
    allowed_domains = ['www.hifiklubben.no','www.hifiklubben.se','www.hifiklubben.dk']

    def start_requests(self):        
        yield scrapy.Request(url='https://www.hifiklubben.no/api/v2/content/tv-surround/tv//facetsearch/?host=www.hifiklubben.no',cb_kwargs={"pg":"TV","cur":"NOK","offset":0}, callback=self.parse)
        yield scrapy.Request(url='https://www.hifiklubben.no/api/v2/content/tv-surround/projektor//facetsearch/?host=www.hifiklubben.no',cb_kwargs={"pg":"Projector","cur":"NOK","offset":0}, callback=self.parse)
        yield scrapy.Request(url='https://www.hifiklubben.se/api/v2/content/tv-hemmabio/tv//facetsearch/?host=www.hifiklubben.se',cb_kwargs={"pg":"TV","cur":"SEK","offset":0}, callback=self.parse)
        yield scrapy.Request(url='https://www.hifiklubben.se/api/v2/content/tv-hemmabio/projektor//facetsearch/?host=www.hifiklubben.se',cb_kwargs={"pg":"Projector","cur":"SEK","offset":0}, callback=self.parse)
        yield scrapy.Request(url='https://www.hifiklubben.dk/api/v2/content/tv-surround/tv//facetsearch/?host=www.hifiklubben.dk',cb_kwargs={"pg":"TV","cur":"DKK","offset":0}, callback=self.parse)
        yield scrapy.Request(url='https://www.hifiklubben.dk/api/v2/content/tv-surround/projektor//facetsearch/?host=www.hifiklubben.dk',cb_kwargs={"pg":"Projector","cur":"DKK","offset":0}, callback=self.parse)
        
    custom_settings = {
        'FEED_URI' : 'Hi-Fi Klubben.csv'
    }

    def parse(self, response, pg, cur, offset):
        data = json.loads(response.text)
        # itemcount = data['resultCount']        
        for item in data['filteredItems']:
            item = {
                'Description' : item['availableColors'][0]['productCode'],
                'ProductInformation' : item['modelType'],
                'Brand': item['brandName'],
                "MPN": item['modelName'],
                'ProductGroup' : pg,
                'Price': item['priceDetails']['price'],
                'Currency': cur,
                'DataURL': response.urljoin(item['url']),
                'Date': d1,
                'Dealer': 'Hi-Fi Klubben',
            }
            yield item        
            j = offset + 50
            if j <= int(json.loads(response.text)['resultCount']):       
                yield scrapy.Request(url=response.request.url + url_end.format(j), cb_kwargs={"pg":pg,"cur":cur,"offset":j}, callback=self.parse)