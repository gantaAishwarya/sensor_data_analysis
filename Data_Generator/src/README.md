InfluxDB Time-Series Data Service
This guide provides instructions on setting up and running the application with InfluxDB using Docker, configuring the .env file, and testing the service with a sample API call.

Setup Instructions
1. Start InfluxDB Using Docker
To start InfluxDB using Docker, follow these steps:

make start-build inside teh data-generator folder

Access the InfluxDB web interface by opening your browser and navigating to:

http://localhost:8086/

Sign up on the InfluxDB web interface. Once you're logged in, create an API token and make sure to save it for use in the next steps.

2. Configure .env File
Fill in the .env file with the appropriate values:

ini
Copy code
INFLUXDB_URL=http://localhost:8086
INFLUXDB_TOKEN=your_influxdb_token_here
INFLUXDB_ORG=your_influxdb_org_here
INFLUXDB_BUCKET=your_influxdb_bucket_here
Replace the placeholders (your_influxdb_token_here, your_influxdb_org_here, and your_influxdb_bucket_here) with the correct values you obtained after signing up for InfluxDB.

3. Run the Application
Once you’ve configured the .env file, you can run the application by executing the following command:

oprn new terminla and execute:
python -m src.app
This will start the Flask application, which will listen for requests on http://localhost:5000.

4. Test the API
You can test the API using a GET request to retrieve measurements within a specified time range.

Here is an example curl command:

bash
Copy code
curl -X GET "http://localhost:5000/measurements?start_time=1733766220&end_time=1733766230" -H "Content-Type: application/json"
start_time and end_time are Unix timestamps that specify the time range for the data you want to retrieve.
Replace these timestamps with actual values relevant to your use case.
Sample Response
The API should return the measurements within the given time range in JSON format:

json
Copy code
{
    "data": [
        {
            "timestamp": 1733766220,
            "sensor_id": 1,
            "temperature": 22.5
        },
        {
            "timestamp": 1733766225,
            "sensor_id": 1,
            "temperature": 23.0
        }
    ]
}
