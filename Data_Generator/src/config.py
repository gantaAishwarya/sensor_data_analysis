import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
DEFAULT_INFLUXDB_URL = 'http://localhost:8086'
DEFAULT_NUM_SENSORS = 20
DEFAULT_NUM_HOUSES = 8
DEFAULT_NUM_USERS = 4
TEMPERATURE_MIN = 20.0
TEMPERATURE_MAX = 30.0
DEFAULT_DATA_GENERATION_INTERVAL = 2  # seconds

# InfluxDB configuration
INFLUXDB_URL = os.getenv('INFLUXDB_URL', DEFAULT_INFLUXDB_URL)
INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN')
INFLUXDB_ORG = os.getenv('INFLUXDB_ORG')
INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET')

# Simulation configuration
try:
    NUM_SENSORS = int(os.getenv('NUM_SENSORS', DEFAULT_NUM_SENSORS))
    NUM_HOUSES = int(os.getenv('NUM_HOUSES', DEFAULT_NUM_HOUSES))
    NUM_USERS = int(os.getenv('NUM_USERS', DEFAULT_NUM_USERS))
    DATA_GENERATION_INTERVAL = int(os.getenv('DATA_GENERATION_INTERVAL', DEFAULT_DATA_GENERATION_INTERVAL))
    if NUM_SENSORS <= 0 or NUM_HOUSES <= 0:
        raise ValueError("NUM_SENSORS and NUM_HOUSES must be positive integers")
except ValueError as e:
    logger.error(f"Configuration error: {str(e)}")
    raise

# Validate required environment variables
if not all([INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET]):
    raise ValueError("Missing required environment variables. Please check INFLUXDB_TOKEN, INFLUXDB_ORG, and INFLUXDB_BUCKET") 