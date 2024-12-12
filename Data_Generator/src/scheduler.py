from flask_apscheduler import APScheduler
from .data_generator import generate_mock_data
from .database import InfluxDBManager
from . import config
import logging

logger = logging.getLogger(__name__)

class SchedulerManager:
    def __init__(self):
        self.scheduler = APScheduler()
        self.db_manager = InfluxDBManager()

    def init_scheduler(self) -> None:
        """Initialize the scheduler and add jobs."""
        try:
            self.scheduler.add_job(
                id='generate_data',
                func=lambda: generate_mock_data(self.db_manager),
                trigger='interval',
                seconds=config.DATA_GENERATION_INTERVAL
            )
            self.scheduler.start()
            logger.info("Scheduler initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing scheduler: {str(e)}")
            raise

    def shutdown(self) -> None:
        """Shutdown the scheduler."""
        try:
            self.scheduler.shutdown()
            self.db_manager.close()
            logger.info("Scheduler shutdown completed successfully")
        except Exception as e:
            logger.error(f"Error during scheduler shutdown: {str(e)}") 