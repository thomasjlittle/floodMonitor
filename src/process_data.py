import logging

from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from datapoint import UnProcessedDataPoint, ProcessedDataPoint

def process_data(
        data: list[UnProcessedDataPoint],
          low_stage_threshold: float, 
          high_stage_threshold: float, 
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
        low_flood_points, high_flood_points = find_flood_points(processed_data, low_stage_threshold, high_stage_threshold)
        logger.info("Data processed, ez mode.")
        return low_flood_points, high_flood_points
    
    except Exception as e:
        logger.error("Aw shucks, data processing didn't work.", exc_info=True)
        return []


def convert_dates_to_datetime(date: int) -> datetime:
    # Assuming the timestamp is in milliseconds.
    utc_time = datetime.fromtimestamp(date / 1000, tz=timezone.utc)
    pst_tz = ZoneInfo("America/Los_Angeles") # this is gross dont look at me
    pst_time = utc_time.astimezone(pst_tz)
    return pst_time


def find_flood_points(processed_data: list[ProcessedDataPoint], low_stage_threshold: float, high_stage_threshold: float) -> tuple[list[ProcessedDataPoint], list[ProcessedDataPoint]]:
    # Return any points that are above the thresholds AND are in the future
    current_time = datetime.now(tz=timezone.utc).astimezone(ZoneInfo("America/Los_Angeles"))
    low_flood_points = [point for point in processed_data if (high_stage_threshold > point.stage >= low_stage_threshold and point.date >= current_time)]
    high_flood_points = [point for point in processed_data if (point.stage >= high_stage_threshold and point.date >= current_time)]
    return low_flood_points, high_flood_points