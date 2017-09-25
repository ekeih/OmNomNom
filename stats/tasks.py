from os import environ

import influxdb
from celery.utils.log import get_task_logger

from backend.backend import app

logger = get_task_logger(__name__)

host = environ.get('OMNOMNOM_INFLUXDB_HOST')
database = environ.get('OMNOMNOM_INFLUXDB_DATABASE')

if host and database:
    influxdb_client = influxdb.InfluxDBClient(host=host, database=database)
else:
    logger.warn('OMNOMNOM_INFLUXDB_(HOST|DATABASE) are not defined. Nothing will be logged to InfluxDB.')
    influxdb_client = None


@app.task(bind=True, default_retry_delay=30)
def log_to_influxdb(self, measurement, fields, tags=None):
    if tags is None:
        tags = {}
    entry = {
        'measurement': measurement,
        'fields': fields,
        'tags': tags
    }
    if influxdb_client:
        try:
            influxdb_client.write_points([entry])
        except Exception as ex:
            raise self.retry(exc=ex)
    else:
        logger.info('Would log to InfluxDB: %s' % entry)


@app.task(bind=True, default_retry_delay=30)
def log_error(_, error_message, module_, type_):
    fields = {
        'error': error_message,
        'module': module_,
        'type': type_
    }
    tags = {
        'module': module_,
        'type': type_
    }
    log_to_influxdb('errors', fields=fields, tags=tags)
