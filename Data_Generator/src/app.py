from flask import Flask, request, jsonify
from typing import Any, Tuple
from .scheduler import SchedulerManager
from .database import InfluxDBManager
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)
db_manager = InfluxDBManager()
scheduler_manager = SchedulerManager()

@app.route('/')
def home() -> str:
    """Health check endpoint."""
    return 'Mock Data Generator is running!'

@app.route('/measurements')
def get_measurements() -> Tuple[Any, int]:
    """Fetch measurements within a specified time range."""
    try:
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')
        
        if not start_time or not end_time:
            return jsonify({
                'error': 'Missing parameters. Please provide start_time and end_time.'
            }), 400

        try:
            start_unix = int(start_time)
            end_unix = int(end_time)
        except ValueError:
            return jsonify({
                'error': 'Invalid timestamp format. Please provide UNIX timestamps in seconds.'
            }), 400
            
        measurements = db_manager.query_measurements(start_unix, end_unix)
        
        return jsonify({
            'measurements': measurements,
            'count': len(measurements)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching measurements: {str(e)}")
        return jsonify({
            'error': f'Error fetching measurements: {str(e)}'
        }), 500

def main() -> None:
    try:
        db_manager.reset_bucket()

        # Initialize the scheduler
        scheduler_manager.init_scheduler()
        
        # Run the Flask app
        app.run(debug=True, use_reloader=False)
    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}")
    finally:
        scheduler_manager.shutdown()

if __name__ == '__main__':
    main() 