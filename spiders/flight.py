import scrapy
import json
from scrapy.crawler import CrawlerProcess
from time import sleep

class FlightSpider(scrapy.Spider):
    name = "flight"
        
    def start_requests(self):
        start_urls = "https://www.flightradar24.com/data/airports"
        yield scrapy.Request(url=start_urls, callback=self.parse)
    

    def parse(self, response):
        country_names = response.xpath('//td//a/text()').extract()
        country_urls = response.xpath('//td//a/@href').extract()
        country_urls = set(country_urls)
        country_urls = sorted(list(country_urls))[1:]
        country_count = len(country_names)
        # country_pair = [f"{c,u}" for c,u in zip(country_names, country_urls)]
        for url in country_urls:
            sleep(1)
            yield response.follow(url, callback= self.parse_country)
        

                
    def parse_country(self,response):
        country = response.url.split('/')[-1]
        airports = response.xpath('//td//a/text()').extract()
        airports = [airport for airport in airports if airport !=' ']
        airport_urls =  response.xpath('//td//a/@href[1]').extract()
        airport_urls = [url for url in airport_urls if url !='#']
        airport_iata = response.xpath('//td//a/@data-iata').extract()
        airport_lat = response.xpath('//td//a/@data-lat').extract()
        airport_lon = response.xpath('//td//a/@data-lon').extract()
        airport_code = response.xpath('//small/text()').extract()[1:]      
        # yield {
        #     "country": country,
        #     "airports": airports,
        #     "airport_codes": airport_code,
        #     "airport_lon": airport_lon,
        #     "airport_lat": airport_lat
        #     }
        
        yield {
            "country":{
                "name": country.capitalize(),
                "code": airport_iata,
                "location":{
                    "lat": airport_lat,
                    "lon": airport_lon,
                            }
            }
        }
       
        
    # def parse_airport(self,response):
    #     url = "https://www.flightradar24.com/airports/list?version=0"
    #     request = scrapy.Request(url)
    #     airport_details = json.loads(response.body)
    #     airport_code = airport_details.keys()
    #     with open("airports_details.json", 'w') as f:
    #         json.dump(airport_details, f, indent=2)
    #     yield response.body


        

# https://www.flightradar24.com/webapi/v1/airport-disruptions?continent=0&period=live&type=both&indices=false
# https://data-live.flightradar24.com/clickhandler/?version=1.5&flight=352b26f8
# https://data-live.flightradar24.com/clickhandler/?version=1.5&flight=352b1036
# https://www.flightradar24.com/airports/list?version=0
# https://www.flightradar24.com/airports/traffic-stats/?airport=kms
# https://www.flightradar24.com/airports/traffic-stats/?airport=tkd