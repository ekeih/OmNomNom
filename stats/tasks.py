import logging
from os import environ

import influxdb

logger = logging.getLogger(__name__)

host = environ.get('OMNOMNOM_INFLUXDB_HOST')
database = environ.get('OMNOMNOM_INFLUXDB_DATABASE')

if host and database:
    influxdb_client = influxdb.InfluxDBClient(host=host, database=database)
else:
    logger.warn('OMNOMNOM_INFLUXDB_(HOST|DATABASE) are not defined. Nothing will be logged to InfluxDB.')
    influxdb_client = None


def log_to_influxdb(measurement, fields, tags=None):
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
            raise ex
    else:
        logger.info('Would log to InfluxDB: %s' % entry)


def log_error(error_message, module_, type_):
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
