# Standard Imports
import threading
from contextlib import asynccontextmanager
from functools import lru_cache

# Third-Party Imports
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import uvicorn

# Local Imports
from app.models import Restaurant
from app.utils import is_open_now, haversine_distance
from app.csv_loader import CSVLoader


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Global Singleton Instance of CSVLoader
    app.state.csv_loader_ins = CSVLoader()

    # Load CSV data to memory at startup and update restaurants and spatial_index in csv_loader_ins
    app.state.csv_loader_ins.load_csv_data()

    # Start background thread to reload CSV data periodically
    thread = threading.Thread(target=app.state.csv_loader_ins.csv_reload_daemon, daemon=True)
    thread.start()

    yield


# Initialize FastAPI with lifespan
app = FastAPI(title="Restaurant Delivery API", lifespan=lifespan)


@app.get("/")
def root() -> dict:
    """Returns a message indicating the service is up and running."""
    return {"message": "service up!"}


@lru_cache(maxsize=1000)
def get_cached_response(latitude: float, longitude: float) -> dict:
    """
    Returns a list of restaurant IDs that can deliver to the user's location.
    Implements caching to improve performance.
    """
    # For performance, query the spatial index to get candidate restaurants
    candidate_ids = list(app.state.csv_loader_ins.spatial_index.intersection((longitude, latitude, longitude, latitude)))
    
    matching_ids = []
    for restaurant_id in candidate_ids:
        restaurant: Restaurant = app.state.csv_loader_ins.restaurants.get(restaurant_id)
        if restaurant is None:
            continue

        # Check distance
        if haversine_distance(latitude, longitude, restaurant.latitude, restaurant.longitude) <= restaurant.availability_radius:
            # Check if open
            # if is_open_now(restaurant):
            matching_ids.append(restaurant.id)
                # break


    return {"restaurant_count": len(matching_ids), "restaurant_ids": matching_ids}


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

    return get_cached_response(latitude, longitude)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
