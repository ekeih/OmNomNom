import influxdb

from backend.backend import app
from celery.utils.log import get_task_logger
from os import environ

logger = get_task_logger(__name__)


host = environ.get('OMNOMNOM_INFLUXDB_HOST')
database = environ.get('OMNOMNOM_INFLUXDB_DATABASE')

if host and database:
    influxdb_client = influxdb.InfluxDBClient(host=host, database=database)
else:
    logger.warn('OMNOMNOM_INFLUXDB_(HOST|DATABASE) are not defined. Nothing will be logged to InfluxDB.')
    influxdb_client = None


@app.task(bind=True, default_retry_delay=30)
def log_to_influxdb(self, measurement, fields, tags={}):
    if influxdb_client:
        try:
            entry = {
                    'measurement': measurement,
                    'fields': fields,
                    'tags': tags
                    }
            influxdb_client.write_points([entry])
        except Exception as ex:
            raise self.retry(exc=ex)
