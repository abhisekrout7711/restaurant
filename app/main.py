# Standard Imports
import threading
from datetime import datetime, timezone
from typing import Dict

# Third-Party Imports
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from rtree import index
import uvicorn

# Local Imports
from app.models import Restaurant
from app.utils import is_open_now, haversine_distance
from app.csv_loader import load_csv_data, csv_reload_daemon


# Global dictionaries: restaurant id -> Restaurant object.
restaurants: Dict[int, Restaurant] = {}

# Rtree spatial index. We index by a bounding box computed from the restaurant’s location and delivery radius.
spatial_index = index.Index()


app = FastAPI(title="Restaurant Delivery API")


@app.on_event("startup")
def startup_event():
    # Load CSV data at startup.
    global restaurants, spatial_index
    restaurants, spatial_index = load_csv_data()
    
    # Start background thread to reload CSV data periodically.
    thread = threading.Thread(target=csv_reload_daemon, daemon=True)
    thread.start()


@app.get("/")
def root():
    return {"message": "service up!"}


@app.get("/restaurants", response_class=JSONResponse)
def query_restaurants(
    latitude: float = Query(..., description="User's latitude"),
    longitude: float = Query(..., description="User's longitude")
):
    """
    Returns a list of restaurant IDs that can deliver to the user's location.
    A restaurant is considered if:
      - The distance between the user's location and the restaurant is <= availability_radius.
      - The current time is within the restaurant's open/close hours.
    """

    # For performance, query the spatial index to get candidate restaurants.
    candidate_ids = list(spatial_index.intersection((longitude, latitude, longitude, latitude)))
    
    matching_ids = []
    now = datetime.now(timezone.utc)

    for rest_id in candidate_ids:
        restaurant = restaurants.get(rest_id)
        if restaurant is None:
            continue

        # Check distance
        distance = haversine_distance(latitude, longitude, restaurant.latitude, restaurant.longitude)
        
        if distance <= restaurant.availability_radius:
            # Check if open now.
            if is_open_now(restaurant, now):
                matching_ids.append(restaurant.id)

    return {"restaurant_ids": matching_ids}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
