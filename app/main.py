# Standard Imports
import threading
from datetime import datetime, timezone

# Third-Party Imports
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import uvicorn

# Local Imports
from app.models import Restaurant
from app.utils import is_open_now, haversine_distance
from app.csv_loader import CSVLoader


app = FastAPI(title="Restaurant Delivery API")

# Global Singleton Instance of CSVLoader
csv_loader_ins = CSVLoader()


@app.on_event("startup")
def startup_event():
    # Load CSV data at startup
    csv_loader_ins.load_csv_data()
    
    # Start background thread to reload CSV data periodically
    thread = threading.Thread(target=csv_loader_ins.csv_reload_daemon, daemon=True)
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
    candidate_ids = list(csv_loader_ins.spatial_index.intersection((longitude, latitude, longitude, latitude)))
    
    matching_ids = []

    for restaurant_id in candidate_ids:
        restaurant: Restaurant = csv_loader_ins.restaurants.get(restaurant_id)
        if restaurant is None:
            continue

        # Check distance
        distance = haversine_distance(latitude, longitude, restaurant.latitude, restaurant.longitude)
        
        if distance <= restaurant.availability_radius:
            # Check if open now.
            if is_open_now(restaurant):
                matching_ids.append(restaurant.id)

    return {"restaurant_ids": matching_ids}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
