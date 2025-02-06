# Standard Imports
import math
import time
from datetime import datetime, timezone, time as dtime
from typing import Optional
from functools import wraps
import statistics

# Local Imports
from app.models import Restaurant
from app.logger import CustomLogger

logger = CustomLogger.get_logger()


def is_open_now(restaurant: Restaurant, now: Optional[dtime] = None) -> bool:
    """
    Check if restaurant is currently within its delivery hours.
    Assumption: Open and Close times refer to the same day.
    """
    now = now or datetime.now(timezone.utc).time()
    
    # Set now to 1pm for local testing
    # now = datetime(2025, 2, 6, 13, 0, 0, tzinfo=timezone.utc).time()

    if restaurant.open_hour <= restaurant.close_hour:
        return restaurant.open_hour <= now <= restaurant.close_hour
    
    return False
    

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float):
    """Calculate the great circle distance (in km) between two points on Earth."""
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    return R * c


def get_bounding_box(lat: float, lon: float, radius_km: float):
    """
    Return bounding box (minx, miny, maxx, maxy) for a circle around (lat, lon)
    Note: we approximate 1 degree latitude ~111 km and adjust longitude by cos(latitude).
    """
    delta_lat = radius_km / 111  # rough conversion km to degrees latitude
    delta_lon = radius_km / (111 * math.cos(math.radians(lat)) + 1e-6)  # add small epsilon to avoid division by zero
    return (lon - delta_lon, lat - delta_lat, lon + delta_lon, lat + delta_lat)


def time_it(func):
    """Decorator to measure the execution time of a function in milliseconds, and log the result."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        elapsed_time = (end_time - start_time) * 1000
        logger.info(f"Execution finished: function={func.__name__} | duration={elapsed_time} ms")
        
        return result
    
    return wrapper


def get_statistics(times: list[float]):
    """
    Calculate the mean, median, mode, min, and max of a list of floats (usecase: execution time in milliseconds),
    and return a dictionary of the computed mean, median, mode, min, and max.
    """
    return {
        "mean": statistics.mean(times),
        "median": statistics.median(times),
        "mode": statistics.mode(times),
        "min": min(times),
        "max": max(times),
    }
