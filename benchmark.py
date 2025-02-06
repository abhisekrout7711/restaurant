# Standard Imports
import time

# Third-Party Imports
import requests

# Local Imports
from app.logger import CustomLogger
from app.csv_loader import CSVLoader
from app.utils import get_statistics


logger = CustomLogger.get_logger(name="benchmark")

API_URL = "http://0.0.0.0:8000/restaurants"


def api_response_benchmark(latitude: float, longitude: float, n: int = 100):
    """
    Benchmark the time taken to fetch the API response for the given coordinates.
    Make n requests to the API and log the statistics of the times taken.
    """
    times = []
    params = {"latitude": latitude, "longitude": longitude}

    requests.get(API_URL, params=params)
    for _ in range(n):
        start = time.perf_counter()
        response = requests.get(API_URL, params=params)
        end = time.perf_counter()
        elapsed = (end - start) * 1000
        times.append(elapsed)
        
        if response.status_code != 200:
            logger.error("Error in request:", response.status_code)

    # Log benchmark results
    stats = get_statistics(times)
    logger.info(f"Statistic for {n} api requests")
    logger.info(f"Mean response time: {stats["mean"]:.2f} ms")
    logger.info(f"Median response time: {stats["median"]:.2f} ms")
    logger.info(f"Mode response time: {stats["mode"]:.2f} ms")
    logger.info(f"Min response time: {stats["min"]:.2f} ms")
    logger.info(f"Max response time: {stats["max"]:.2f} ms")


def csv_loader_benchmark(n: int = 100):
    """
    Benchmark the time taken to load the CSV file and populate the restaurants and spatial index.
    Make n calls to load_csv_data and log the statistics of the times taken.
    """
    times = []
    for _ in range(n):
        start = time.perf_counter()
        csv_loader = CSVLoader()
        csv_loader.load_csv_data()
        end = time.perf_counter()
        elapsed = (end - start) * 1000
        times.append(elapsed)

    # Log benchmark results
    stats = get_statistics(times)
    logger.info(f"Statistics for {n} <function=load_csv_data> calls")
    logger.info(f"Mean CSV Load time: {stats["mean"]:.2f} ms")
    logger.info(f"Median CSV Load time: {stats["median"]:.2f} ms")
    logger.info(f"Mode CSV Load time: {stats["mode"]:.2f} ms")
    logger.info(f"Min CSV Load time: {stats["min"]:.2f} ms")
    logger.info(f"Max CSV Load time: {stats["max"]:.2f} ms")


if __name__ == "__main__":
    # Benchmark api response time with sample coordinates for syncronous requests
    api_response_benchmark(latitude=51.14, longitude=6.451, n=20000)
    print("\n")
    api_response_benchmark(latitude=51.145, longitude=6.45, n=50000)
    print("\n")
    api_response_benchmark(latitude=51.1461, longitude=6.4510, n=100000)

    # Benchmark CSV loader time
    csv_loader_benchmark(n=100)
