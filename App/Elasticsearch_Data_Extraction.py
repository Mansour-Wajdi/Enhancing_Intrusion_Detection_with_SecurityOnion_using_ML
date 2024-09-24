import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import urllib3
import logging
#from handler import TextboxLoggerHandler
# Setup basic logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def connect_elasticsearch(elastic_host, username, password,logger2):
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
            logger2.warning("Failed to connect to Elasticsearch!")
            return False, None

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        return True, es

    except Exception as e:
        logging.error(f"Error occurred while connecting to Elasticsearch: {e}")
        return False, None
    

def retrieve_alerts(es,severity,logger2):
    """
    Retrieve alerts from Elasticsearch.

    Parameters:
    - es (Elasticsearch): Elasticsearch instance.

    Returns:
    - DataFrame: A DataFrame containing the retrieved alerts or None if retrieval failed.
    """
    search_context = Search(using=es, index='*:so-*', doc_type='doc') \
        .query('query_string', query='event.module:suricata') \
        .filter('terms', **{'rule.severity' : severity})

    response = search_context.execute()

    if not response.success():
        logger2.warning("Failed to retrieve alerts.")
        return None

    df = pd.DataFrame((d.to_dict() for d in search_context.scan()))
    logger2.info(f"Successfully retrieved {len(df)} alerts.")
    return df


def flatten_columns(df):
    """
    Flatten the columns of the DataFrame that contain dictionaries.

    Parameters:
    - df (DataFrame): The original DataFrame.

    Returns:
    - DataFrame: A DataFrame with flattened columns.
    """
    dict_cols = [col for col in df.columns if isinstance(df[col].iloc[0], dict)]
    for col in dict_cols:
        flattened = pd.json_normalize(df[col])
        flattened.columns = [f"{col}.{subcol}" for subcol in flattened.columns]
        df = df.drop(col, axis=1).join(flattened)
    return df


def extract_flow_info(df, version,logger2):
    """
    Extract specific columns based on the version.

    Parameters:
    - df (DataFrame): The original DataFrame.
    - version (str): Version type - either 'import' or 'standalone'.

    Returns:
    - DataFrame: A DataFrame with selected columns.
    """
    if version == 'import':
        columns = ['log.id.uid', 'destination.ip', 'destination.port', 'source.port', 'source.ip',
                   'network.transport', '@timestamp', 'host.name', 'import.id']
    elif version == 'standalone':
        columns = ['log.id.uid', 'destination.ip', 'destination.port', 'source.port', 'source.ip',
                   'network.transport', '@timestamp', 'host.name']
    else:
        logger2.error("version should be either import or standalone")
        return None

    return df[columns]


def extract_data_from_elasticsearch(elastic_host, username, password, version,severity,logger2, output_csv='./csv_files/flow_info.csv'):
    """
    Main execution function to extract data from Elasticsearch.

    Parameters:
    - elastic_host (str): Host address for Elasticsearch.
    - username (str): Username for authentication.
    - password (str): Password for authentication.
    - version (str): Version type - either 'import' or 'standalone'.
    - output_csv (str): Path for the output CSV file.
    """
    is_connected, es = connect_elasticsearch(elastic_host, username, password,logger2)
    if not is_connected:
        logger2.error("Exiting due to connection issues.")
        return

    alerts_df = retrieve_alerts(es,severity,logger2)
    if alerts_df is not None:
        alerts_df = flatten_columns(alerts_df)
        flow_info = extract_flow_info(alerts_df, version,logger2)
        if flow_info is not None:
            flow_info.to_csv(output_csv, index=False)


# Call the function
if __name__ == "__main__":
    elastic_host = input("Enter Elasticsearch host: ")
    username = input("Enter username: ")
    password = input("Enter password: ")
    version = input("Enter version (import/standalone): ")
    severity= ['1', '2', '3']
    
    extract_data_from_elasticsearch(elastic_host, username, password, version,severity)
