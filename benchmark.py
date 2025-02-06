# Standard Imports
import time

# Third-Party Imports
import requests

# Local Imports
from app.logger import CustomLogger
from app.utils import get_statistics

logger = CustomLogger.get_logger(name="benchmark")

API_URL = "http://0.0.0.0:8080/restaurants"

def run_benchmark(latitude: float, longitude: float, n: int = 100):
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
    logger.info(f"Performed {n} requests.")
    logger.info(f"Mean response time: {stats["mean"]:.2f} ms")
    logger.info(f"Median response time: {stats["median"]:.2f} ms")
    logger.info(f"Mode response time: {stats["mode"]:.2f} ms")
    logger.info(f"Min response time: {stats["min"]:.2f} ms")
    logger.info(f"Max response time: {stats["max"]:.2f} ms")


if __name__ == "__main__":
    # Benchmark with a sample location
    run_benchmark(latitude=51.14, longitude=6.451, n=1000)
    print("\n")
    run_benchmark(latitude=51.145, longitude=6.45, n=1000)
    print("\n")
    run_benchmark(latitude=51.1461, longitude=6.4510, n=1000)
