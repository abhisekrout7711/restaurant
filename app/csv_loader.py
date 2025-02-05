# Standard Imports
import csv
import io
import time
from datetime import datetime, timezone
from rtree import index

# Third-Party Imports
import requests

# Local Imports
from app.config import CSV_URL, CSV_UPDATE_INTERVAL_SECONDS
from app.models import Restaurant
from app.utils import get_bounding_box


restaurants = {}
spatial_index = index.Index()


def load_csv_data() -> tuple[dict[int, Restaurant], index.Index]:
    """Load the CSV file from the URL and update the global restaurants and spatial index."""
    
    try:
        response = requests.get(CSV_URL)
        response.raise_for_status()
        content = response.content.decode("utf-8")
        csv_reader = csv.DictReader(io.StringIO(content))
    
    except Exception as e:
        print(f"Error loading CSV from {CSV_URL}: {e}")
        return

    new_restaurants = {}
    # Create a new spatial index (we cannot easily remove all items from an rtree)
    new_index = index.Index()

    for idx, row in enumerate(csv_reader):
        try:
            restaurant = Restaurant.from_csv_row(row)
            new_restaurants[restaurant.id] = restaurant

            # Compute bounding box for the restaurant based on its delivery radius.
            bbox = get_bounding_box(restaurant.latitude, restaurant.longitude, restaurant.availability_radius)
            new_index.insert(restaurant.id, bbox)

        except Exception as e:
            print(f"Error parsing row {idx}: {e}")
            continue
    
    # restaurants = new_restaurants
    # spatial_index = new_index
    print(f"[{datetime.now(timezone.utc)}] Loaded {len(restaurants)} restaurants.")
    return new_restaurants, new_index


def csv_reload_daemon():
    """Thread that reloads the CSV file periodically."""
    while True:
        load_csv_data()
        time.sleep(CSV_UPDATE_INTERVAL_SECONDS)


if __name__ == "__main__":
    
    breakpoint()
    restaurants, spatial_index = load_csv_data()