from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.exceptions import InfluxDBError
from typing import Any, Optional
from datetime import datetime
from . import config
import logging

logger = logging.getLogger(__name__)

class InfluxDBManager:
    def __init__(self):
        self.client = InfluxDBClient(
            url=config.INFLUXDB_URL,
            token=config.INFLUXDB_TOKEN,
            org=config.INFLUXDB_ORG
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

    def reset_bucket(self) -> None:
        """Reset the InfluxDB bucket by deleting and recreating it."""
        try:
            buckets_api = self.client.buckets_api()
            
            bucket = buckets_api.find_bucket_by_name(config.INFLUXDB_BUCKET)
            if bucket:
                buckets_api.delete_bucket(bucket)
                logger.info(f"Deleted existing bucket: {config.INFLUXDB_BUCKET}")
            
            buckets_api.create_bucket(bucket_name=config.INFLUXDB_BUCKET, org=config.INFLUXDB_ORG)
            logger.info(f"Created new bucket: {config.INFLUXDB_BUCKET}")
            
        except InfluxDBError as e:
            logger.error(f"Error resetting InfluxDB: {str(e)}")
            raise

    def write_point(self, point: Point) -> None:
        """Write a single point to InfluxDB."""
        try:
            self.write_api.write(bucket=config.INFLUXDB_BUCKET, record=point)
        except Exception as e:
            logger.error(f"Error writing to InfluxDB: {str(e)}")
            raise

    def query_measurements(self, start_time: int, end_time: int) -> list[dict[str, Any]]:
        """Query measurements within a specified time range."""
        query = f'''
            from(bucket: "{config.INFLUXDB_BUCKET}")
                |> range(start: {start_time}, stop: {end_time})
                |> filter(fn: (r) => r["_measurement"] == "sensor_readings")
                |> pivot(
                    rowKey: ["_time", "sensor_id", "house_id", "user_id"],
                    columnKey: ["_field"],
                    valueColumn: "_value"
                )
        '''

        result = self.query_api.query(query=query, org=config.INFLUXDB_ORG)
        
        measurements = []
        for table in result:
            for record in table.records:
                measurements.append({
                    'time': int(record.get_time().timestamp()),
                    'sensor_id': record.values.get('sensor_id'),
                    'house_id': record.values.get('house_id'),
                    'user_id': record.values.get('user_id'),
                    'temperature': record.values.get('temperature')
                })
        
        return measurements

    def close(self) -> None:
        """Close the database connection."""
        self.client.close() 