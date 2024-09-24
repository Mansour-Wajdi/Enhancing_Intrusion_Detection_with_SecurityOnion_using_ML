import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import urllib3
import logging


def connect_elasticsearch(elastic_host, username, password, logger):
    """
    Connects to Elasticsearch using the provided parameters.

    Parameters:
    - elastic_host (str): Host address for Elasticsearch.
    - username (str): Username for authentication.
    - password (str): Password for authentication.

    Returns:
    - tuple: (is_connected (bool), es (Elasticsearch instance or None))
    """
    
    try:
        es = Elasticsearch([elastic_host],
                           ca_certs=False, verify_certs=False, http_auth=(username, password))
        if not es.ping():
            logger.warning("Failed to connect to Elasticsearch!")
            return False, None

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        logger.info("Connected to Elasticsearch")
        return True, es

    except Exception as e:
        logger.error(f"Error occurred while connecting to Elasticsearch: {e}")
        return False, None
