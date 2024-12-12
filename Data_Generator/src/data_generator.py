import random
from datetime import datetime, timezone
from influxdb_client import Point
from . import config
from .database import InfluxDBManager
import logging

logger = logging.getLogger(__name__)

def generate_mock_data(db_manager: InfluxDBManager) -> None:
    """Generate random sensor data and store in InfluxDB."""
    try:
        current_time = datetime.now(timezone.utc)
        
        for sensor_id in range(1, config.NUM_SENSORS + 1):
            temperature = random.uniform(config.TEMPERATURE_MIN, config.TEMPERATURE_MAX)
            house_id = ((sensor_id - 1) % config.NUM_HOUSES) + 1
            user_id = ((house_id - 1) % config.NUM_USERS) + 1

            # come here to change precision
            point = Point("sensor_readings") \
                .tag("sensor_id", str(sensor_id)) \
                .tag("house_id", str(house_id)) \
                .tag("user_id", str(user_id)) \
                .field("temperature", round(temperature, 2)) \
                .time(current_time, write_precision='s')
                
            db_manager.write_point(point)
            logger.debug(
                f"Generated data: Sensor={sensor_id}, House={house_id}, "
                f"Temp={temperature:.2f}°C, Time={current_time.isoformat()}"
            )
    except Exception as e:
        logger.error(f"Error generating mock data: {str(e)}")
        raise 