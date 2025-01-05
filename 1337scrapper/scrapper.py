import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, field_validator, ValidationError
import json

class _1337xparser():

    def search(self, r: requests.Request) -> str:
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            s = soup.find_all('tr')
            
            return self.parse_search_results(s)
        else:
            return 'KO'
        
    def parse_search_results(self, search_results) -> json:
        results = []
        for result in search_results:
            name = result.select_one('.name')
            if name.text != "name":
                torrent_name = name.select('a')[1].text
                seeds = result.select_one('td.seeds').text
                leechers = result.select_one('td.leeches').text
                size = result.select_one('td.size').text.replace(seeds, '')
                upload_date = result.select_one('td.coll-date').text
                uploaders = result.select_one('td.vip').text if result.select_one('td.vip') else "None"
                results.append({"name": torrent_name, "seeders": seeds, "leechers": leechers, "size": size, "upload_date": upload_date, "uploaders": uploaders})
        return results
