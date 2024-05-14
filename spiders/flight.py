import scrapy
import json
from scrapy.crawler import CrawlerProcess
from time import sleep

class FlightSpider(scrapy.Spider):
    name = "flight"
        
    def start_requests(self):
        # start_urls = "https://www.flightradar24.com/data/airports"
        countries_url = "https://www.flightradar24.com/airports/country-list"
        yield scrapy.Request(url=countries_url, callback=self.parse_country)
    

    # def parse(self, response):
        # country_names = response.xpath('//td//a/text()').extract()
        # country_urls = response.xpath('//td//a/@href').extract()
        # country_urls = set(country_urls)
        # country_urls = sorted(list(country_urls))[1:]
        # country_count = len(country_names)
        # country_pair = [f"{c,u}" for c,u in zip(country_names, country_urls)]
        # for url in country_urls:
        #     sleep(1)
        #     yield response.follow(url=url, callback= self.parse_country)
        

                
    def parse_country(self,response):
        """Parsing Countries into JSON File"""
        # country = response.url.split('/')[-1]
        # airports = response.xpath('//td//a/text()').extract()
        # airports = [airport for airport in airports if airport !=' ']
        # airport_urls =  response.xpath('//td//a/@href[1]').extract()
        # airport_urls = [url for url in airport_urls if url !='#']
        # airport_iata = response.xpath('//td//a/@data-iata').extract()
        # airport_lat = response.xpath('//td//a/@data-lat').extract()
        # airport_lon = response.xpath('//td//a/@data-lon').extract()
        # airport_code = response.xpath('//small/text()').extract()[1:]      
        # yield {
        #     "country": country,
        #     "airports": airports,
        #     "airport_codes": airport_code,
        #     "airport_lon": airport_lon,
        #     "airport_lat": airport_lat
        #     }
        

        # country = { "country":{
        #     "name": country.capitalize(),
        #     "code": airport_iata,
        #     "location":{
        #         "lat": airport_lat,
        #         "lon": airport_lon,
        #                 }
        # }}
        country_details = json.loads(response.body)
        country_code = country_details.keys()
        codes = [country for country in country_code]
        countries = []
        for num, country in enumerate(country_details.values()):
            country["url"] = "https://www.flightradar24.com/data/airports/" + country["url"]
            country["code"] = codes[num]
            countries.append(country)
        country_data = {"countries": countries}
        with open("countries.json",'w') as f:
            json.dump(country_data,f, indent=2)
    
        airport_url = "https://www.flightradar24.com/airports/list"
        yield scrapy.Request(url=airport_url, callback= self.parse_airport)
       
        
    def parse_airport(self,response):
        """Parsing Airport into JSON File"""
        airport_details = json.loads(response.body)
        keys = ["icao", "iata", "name", "lat", "lon", "url","num_x","city", "code"]
        airports = []
        for airport in airport_details.values():
            airports.append({key:value for key,value in zip(keys,airport)})
        
        airports_data = {"airports": airports}
        
        with open("airports.json", 'w') as f:
            json.dump(airports_data, f, indent=2)
        airlines_url = "https://www.flightradar24.com/mobile/airlines"
        yield scrapy.Request(url=airlines_url, callback=self.parse_airline)
        
    def parse_airline(self,response):
        """Parsing Airlines into JSON File"""
        airline_details = json.loads(response.body)
        airlines = airline_details["rows"]
        airlines = {"airlines": airlines}
        with open("airlines.json", 'w') as f:
            json.dump(airlines, f, indent=2)


        

# https://www.flightradar24.com/webapi/v1/airport-disruptions?continent=0&period=live&type=both&indices=false
# https://data-live.flightradar24.com/clickhandler/?version=1.5&flight=352b26f8
# https://data-live.flightradar24.com/clickhandler/?version=1.5&flight=352b1036
# https://www.flightradar24.com/airports/list?version=0
# https://www.flightradar24.com/airports/traffic-stats/?airport=kms
# https://www.flightradar24.com/airports/traffic-stats/?airport=tkd

# pinned flights
# https://www.flightradar24.com/flights/pinned?limit
# country list
# https://www.flightradar24.com/airports/country-list
# airlines 
# https://www.flightradar24.com/mobile/airlines?format=2&version=0