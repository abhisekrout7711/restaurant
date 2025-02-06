import time
from datetime import datetime, timezone, timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import Restaurant
from app.utils import get_bounding_box

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "service up!"}


def test_query_restaurants_no_results(monkeypatch):
    # Create a dummy CSV loader instance with empty restaurants and a dummy spatial_index.
    class DummyLoader:
        pass

    dummy_loader = DummyLoader()
    dummy_loader.restaurants = {}
    # Create a dummy spatial index whose intersection method always returns an empty list.
    dummy_loader.spatial_index = type(
        "DummyIndex", (), {"intersection": lambda self, bbox: []}
    )()

    # Use monkeypatch.setitem on app.state.__dict__ to inject our dummy_loader.
    monkeypatch.setitem(app.state.__dict__, "csv_loader_ins", dummy_loader)

    response = client.get("/restaurants?latitude=0&longitude=0")
    assert response.status_code == 200
    assert response.json() == {"restaurant_count": 0, "restaurant_ids": []}


def test_query_restaurants_with_result(monkeypatch):
    # Create a dummy CSV loader instance with empty restaurants and a dummy spatial_index.
    class DummyLoader:
        pass

    dummy_loader = DummyLoader()
    dummy_loader.restaurants = {}
    # Create a dummy spatial index whose intersection method returns a list with our dummy restaurant id.
    dummy_loader.spatial_index = type(
        "DummyIndex", (), {"intersection": lambda self, bbox: [999]}
    )()

    # Inject the dummy_loader into app.state using monkeypatch.setitem.
    monkeypatch.setitem(app.state.__dict__, "csv_loader_ins", dummy_loader)

    # Create a dummy restaurant near (10, 10) that is open now.
    now = datetime.now(timezone.utc)
    dummy = Restaurant(
        id=999,
        latitude=10.0,
        longitude=10.0,
        availability_radius=5.0,
        open_hour=(now - timedelta(hours=1)).time(),
        close_hour=(now + timedelta(hours=1)).time(),
        rating=4.5,
    )
    # Inject the dummy restaurant into our patched CSV loader instance.
    app.state.csv_loader_ins.restaurants[dummy.id] = dummy
    breakpoint()
    bbox = get_bounding_box(dummy.latitude, dummy.longitude, dummy.availability_radius)

    response = client.get("/restaurants?latitude=10&longitude=10")
    assert response.status_code == 200
    data = response.json()
    assert data["restaurant_count"] == 1
    assert dummy.id in data["restaurant_ids"]
