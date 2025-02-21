import re
import requests
from bs4 import BeautifulSoup
import json
import logging
from datapoint import UnProcessedDataPoint

def scrape_web(
        url: str, 
        logger: logging.Logger = None
        ) -> list[UnProcessedDataPoint]:
    
    try:
        # Log
        if logger is None:
            logger = logging.getLogger(__name__)

        # Do some scrapin'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tags = soup.find_all('script')

        # Retrieve 'Guidance' data
        guidance_data = None
        pattern = re.compile(
            r"chart\.addSeries\(\s*\{.*?name\s*:\s*['\"]Guidance['\"].*?data\s*:\s*(\[[^\]]*\])",
            re.DOTALL
        )

        for script in script_tags:
            if script.string and "chart.addSeries(" in script.string and "name:'Guidance'" in script.string:
                match = pattern.search(script.string)
                if match:
                    guidance_data = match.group(1)
                    break

        if guidance_data:
            def js_object_to_json(js_text):
                # This regex adds double quotes around object keys (assuming keys are alphanumeric and underscore)
                return re.sub(r"(\{|,)\s*([a-zA-Z0-9_]+)\s*:", r'\1 "\2":', js_text)

            json_compatible = js_object_to_json(guidance_data)
            
            # Remove trailing comma
            json_compatible = re.sub(r",\s*\]", "]", json_compatible)

            try:
                data_series = json.loads(json_compatible)
                
                # Package data into cute lil thangs
                dates = [date["x"] for date in data_series]
                stages = [stage["y"] for stage in data_series]
                data = [UnProcessedDataPoint(date, stage) for date, stage in zip(dates, stages, strict=True)]
                logging.info(f"{len(dates)} data points loaded successfully :0)")
                return data

            except json.JSONDecodeError as e:
                logging.error("Ruh Roh, error decoding JSON:", e)
                return
        else:
            logging.error("Oh nuts, Guidance data was not found :0(")
            return
    except Exception:
        logger.error("I wont lie, somethin real bad happened during web scraping...")
