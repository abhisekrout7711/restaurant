# Standard Imports
import time
import statistics

# Third-Party Imports
import requests

# Local Imports
from app.logger import CustomLogger

logger = CustomLogger.get_logger(name="benchmark")

API_URL = "http://0.0.0.0:8080/restaurants"

def run_benchmark(latitude: float, longitude: float, n: int = 100):
    times = []
    params = {"latitude": latitude, "longitude": longitude}
    # Warm-up
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
    logger.info(f"Performed {n} requests.")
    logger.info(f"Mean response time: {statistics.mean(times):.2f} ms")
    logger.info(f"Median response time: {statistics.median(times):.2f} ms")
    logger.info(f"Mode response time: {statistics.mode(times):.2f} ms")
    logger.info(f"Min response time: {min(times):.2f} ms")
    logger.info(f"Max response time: {max(times):.2f} ms")


if __name__ == "__main__":
    # Benchmark with a sample location
    run_benchmark(latitude=51.14, longitude=6.451, n=1000)
    print("\n")
    run_benchmark(latitude=51.145, longitude=6.45, n=1000)
    print("\n")
    run_benchmark(latitude=51.1461, longitude=6.4510, n=1000)