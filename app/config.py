# CSV URL and Update Interval
CSV_URL = "https://s3.amazonaws.com/test.jampp.com/dmarasca/takehome.csv"
CSV_UPDATE_INTERVAL_SECONDS = 6 * 60 * 60  # 6 hours


# Logger Configuration
import logging

LOGGER_INSTANCE_NAME = "app"
LOGGER_FILE_NAME = "app.log"

LOGGER_LEVEL = logging.DEBUG
LOGGER_LEVEL_CONSOLE = logging.DEBUG
LOGGER_LEVEL_FILE = logging.INFO

LOGGER_FORMATTER = logging.Formatter('%(asctime)s [%(levelname)s] : %(message)s', datefmt='%Y-%m-%d %H:%M:%S')