import datetime
import logging
from datapoint import UnProcessedDataPoint, ProcessedDataPoint

def process_data(
        data: list[UnProcessedDataPoint],
          stage_threshold: float, 
          logger: logging.Logger = None
          ) -> list[ProcessedDataPoint]:
    # Log
    if logger is None:
        logger = logging.getLogger(__name__)
        
    try:
        # Convert time to freedom units
        processed_data = [
            ProcessedDataPoint(convert_dates_to_datetime(dp.date), dp.stage)
            for dp in data
        ]

        # Get flood points
        flood_points = find_flood_points(processed_data, stage_threshold)
        logger.info("Data processed, ez mode.")
        return flood_points
    except Exception:
        logger.error("Aw shucks, data processing didn't work.")

        
def convert_dates_to_datetime(date: int):
    # P sure these are in ms (like 50:50? hehe)
    return datetime.datetime.fromtimestamp(date / 1000) 

def find_flood_points(processed_data: list[ProcessedDataPoint], stage_threshold: float):
    # Just use a list comp bc theres not a ton of data and i dont wanna do it the right way
    return [point for point in processed_data if point.stage > stage_threshold]
