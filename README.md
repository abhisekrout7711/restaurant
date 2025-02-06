# Restaurant Delivery API

The Restaurant Delivery API allows users to find restaurants that can deliver to their specific location. It efficiently identifies nearby restaurants using a spatial index (R-tree) for fast proximity searches. The API considers a restaurant eligible for delivery if:

- The distance between the user's location and the restaurant is within a specified availability radius.
- The current time falls within the restaurant’s open/close hours.

Built with FastAPI, this high-performance API ensures quick responses and includes caching for frequently queried locations. It’s designed to provide real-time, accurate delivery options to users based on their current location.


## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Docker Setup](#docker-setup)
- [API Endpoints](#api-endpoints)
- [Design Choices](#design-choices)
- [Benchmark Resutls](#benchmark-results)

## Features

- **Efficient Restaurant Search:** Utilizes an R-tree spatial index for fast retrieval of restaurants within a given radius.
- **Real-time Availability:** Checks if a restaurant is open at the time of query based on its opening hours.
- **Caching:** Implements caching for frequently accessed locations to reduce latency.
- **Background Updates:** Periodically reloads restaurant data from a CSV file in the background to keep the information up-to-date.
- **Dockerized:** Easily deployable using Docker and docker-compose.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/abhisekrout7711/restaurant
   ```

2. Navigate to the project directory:
    ```bash
    cd restaurant
    ```

3. Set the python path to the base directory
    ```bash
    export PYTHONPATH=$PYTHONPATH:/Users/abhisekrout/Desktop/restaurant
    ```

4. Create a conda environment
    ```bash
    conda create --name restaurant_env python=3.12.8
    ```

5. Activate the conda environment
    ```bash
    conda activate restaurant_env
    ```

6. Install the dependencies
    ```bash
    pip install -r requirements.txt
    ```

## Usage
### Run Server

1. Execute `app/main.py`
    ```bash
    python app/main.py
    ```

OR

2. Using uvicorn
    ```bash
    uvicorn app.main:app --reload
    ```

### Run Tests
    
    ```bash
    pytest tests/test_api.py  
    ```

### Run Benchmarks

To run the benchmarks, execute the `benchmark.py` script. This script measures the time taken to fetch API responses for various numbers of requests and logs the statistics of the times taken to `app.log` file.
    ```bash
    python benchmark.py
    ```
- [Benchmark Results](#benchmark-results)

## Docker Setup

### Build and Start in Development Mode with Hot-Reload
To start the application in development mode with hot-reload, use the following command:
    ```bash
    docker-compose up restaurant-api
    ```
This will build and run the Docker container, allowing you to make changes and see them reflected immediately.

### Run Tests
To run tests within the Docker container, use the following command:
    ```bash
    docker-compose run --rm tests
    ```
This will execute the tests and remove the container once the tests are finished.

### Production Build (Without Hot-Reload)
For a production build, without hot-reload, you can build and run the Docker container with the following commands:
    ```bash
    docker build -t restaurant-api .
    ```
    ```bash
    docker run -d -p 8000:8000 restaurant-api
    ```
This will build the Docker image and start the application in a detached mode on port 8000.

### Stop Server
To stop the server
    ```bash
    docker stop 065d244716e0ff6848ce38fb2f1e20e67616384783b5a47a7d8fe151fceb5686
    ```
Replace `065d244716e0ff6848ce38fb2f1e20e67616384783b5a47a7d8fe151fceb5686` with your container-id


## API Endpoints

- **GET** `/`: Returns a message indicating the service is up and running
- **GET** `/restaurant`: Returns a list of restaurant IDs that can deliver to the user's location

## Design Choices

- **Spatial Indexing**: An R-tree is used for efficient nearest-neighbor searches, significantly improving the performance of restaurant lookups.

- **Caching**: Results for frequently accessed locations are cached using `lru_cache` to reduce latency.

- **Background Updates**: A background thread periodically reloads restaurant data from the CSV file to ensure the information is up-to-date.

- **Asynchronous Context**: The `lifespan` context manager is used to handle the initialization and cleanup of resources, such as loading the CSV data and starting the background thread.


## Benchmark Results

### API Performance
Below are the benchmark results for API request performance

#### 20,000 API Requests
- **Mean response time:** 3.68 ms  
- **Median response time:** 3.30 ms  
- **Mode response time:** 3.24 ms  
- **Min response time:** 2.01 ms  
- **Max response time:** 99.46 ms  

#### 50,000 API Requests
- **Mean response time:** 3.53 ms  
- **Median response time:** 3.08 ms  
- **Mode response time:** 2.95 ms  
- **Min response time:** 2.03 ms  
- **Max response time:** 80.18 ms  

#### 100,000 API Requests
- **Mean response time:** 3.71 ms  
- **Median response time:** 3.32 ms  
- **Mode response time:** 3.47 ms  
- **Min response time:** 1.99 ms  
- **Max response time:** 98.71 ms  


### CSV Load Performance
Below are the benchmark results for CSV loading performance

#### 100 Calls to `load_csv_data`
- **Mean CSV Load time:** 10,999.57 ms  
- **Median CSV Load time:** 8,380.38 ms  
- **Mode CSV Load time:** 8,601.17 ms  
- **Min CSV Load time:** 8,124.51 ms  
- **Max CSV Load time:** 24,030.62 ms  


#### Log Insights
You can refer to the app.log file for a detailed record of these benchmark results, which were tested on my local machine.
