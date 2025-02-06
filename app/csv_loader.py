# Standard Imports
import csv
import io
import time

# Third-Party Imports
import requests
from rtree import index
from fastapi import HTTPException

# Local Imports
from app.config import CSV_URL, CSV_UPDATE_INTERVAL_SECONDS
from app.models import Restaurant
from app.utils import get_bounding_box
from app.logger import CustomLogger

logger = CustomLogger.get_logger()

class CSVLoader:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            # Initialize instance variables
            cls.__instance.restaurants = {}
            cls.__instance.spatial_index = index.Index()
        
        return cls.__instance

    def load_csv_data(self):
        """Load the CSV file from the URL and update the restaurants and spatial_index instance variables."""
        try:
            response = requests.get(CSV_URL)
            response.raise_for_status()
            content = response.content.decode("utf-8")
            csv_reader = csv.DictReader(io.StringIO(content))
        
        except Exception as e:
            error_msg = f"Error fetching CSV from {CSV_URL}: {e}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)

        new_restaurants = {}
        # Create a new spatial index (we cannot easily remove all items from an rtree)
        new_spatial_index = index.Index()

        for idx, row in enumerate(csv_reader):
            try:
                restaurant = Restaurant.from_csv_row(row)
                new_restaurants[restaurant.id] = restaurant

                # Compute bounding box for the restaurant based on its delivery radius.
                bbox = get_bounding_box(restaurant.latitude, restaurant.longitude, restaurant.availability_radius)
                new_spatial_index.insert(restaurant.id, bbox)

            except Exception as e:
                logger.warning(f"Error parsing row {idx}: {e}")
                continue
        
        # Update the instance variables
        self.restaurants = new_restaurants
        self.spatial_index = new_spatial_index

        logger.info(f"Loaded {len(self.restaurants)} restaurants.")

    def csv_reload_daemon(self):
        """Thread that reloads the CSV file periodically."""
        while True:
            time.sleep(CSV_UPDATE_INTERVAL_SECONDS)
            self.load_csv_data()
