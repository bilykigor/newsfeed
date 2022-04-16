import logging
from mysql.connector import connect as mysql_connect, Error
from app import config
from app.utils import Singleton

import pandas as pd
from time import sleep

class DBConnector(metaclass=Singleton):
    def __init__(self):
        self.connections={}
        self.engines={}

    def get_connection(self, credentials=config.db_news):
        key = '_'.join([credentials['host'],str(credentials['port']),credentials['database']])

        if key in self.connections:
            connection = self.connections[key]

            if connection is not None:
                if connection.is_connected():
                    logging.debug(f'Exists connection {key}')

                    return connection
        
        self.connections[key] = create_mysql_connector(credentials)

        return self.connections[key]

    def engine(self, credentials=config.db_news):
        key = '_'.join([credentials['host'],str(credentials['port']),credentials['database']])

        logging.info(key)

        if key in self.engines:
            engine = self.engines[key]

            if engine:
                if engine.open:
                    logging.info(f'Using existing engine {key}')

                    return engine
        
        logging.info(f'Creating engine {key}')
        self.engines[key] = create_mysql_engine(credentials)

        return self.engines[key]

def create_mysql_connector(credentials=config.db_news):
    """
    Creates mysql connector for micro-service database

    Returns
    -------
    con : mysql connector
    """
    try:
        logging.debug(f"DB: connecting to {credentials['host']}/{credentials['database']}")
        connection = mysql_connect(**credentials,buffered=True)
        
        if connection is not None:
            if connection.is_connected():
                logging.debug(f"DB: connected")
                return connection

        logging.warn(f"DB: failed to connect {credentials['host']}/{credentials['database']}")
        return None
    except Error as e:
        logging.error(f"Error while connecting to MySQL. Reason: {e}")
        return None
        
def create_mysql_engine(credentials=config.db_news):
    """
    Creates mysql engine for micro-service database

    Returns
    -------
    con : mysql engine
    """
    try:
        logging.info(f"Connecting to {credentials['host']}/{credentials['database']}")
        creds={}
        creds['host'] = credentials.get('host','0.0.0.0')
        creds['port'] = int(credentials.get('port',6033))
        creds['user'] = credentials.get('user','user')
        creds['passwd'] = credentials.get('password','user')
        creds['db'] = credentials.get('database','db')
        creds['cursorclass'] = pymysql.cursors.SSCursor
        
        engine  = pymysql.connect(**creds)
        
        return engine
    except Error as e:
        logging.error(f"Error while connecting to MySQL. Reason: {e}")
        return None

def read_sql(q, db_connector,**kwargs):
        passed = False
        logging.debug(q)
        data = pd.DataFrame()

        while db_connector is None:
            db_connector = DBConnector().get_connection()
            sleep(30)

        while not passed:
            try:   
                data = pd.read_sql(q, db_connector, **kwargs)               
                passed = True
            except ConnectionResetError as e:
                logging.error("ConnectionResetError")
                logging.error(e)
                sleep(30)
                db_connector = DBConnector().get_connection()
            except Exception as e:
                logging.error("Readsql Error")
                logging.error(e)
                passed = True
        
        return data

def delete_sql(q, db_connector):
    logging.debug(q)
    passed = False
    while not passed:
        try:   
            cursor = db_connector.cursor()
            cursor.execute(q)
            db_connector.commit()
            passed = True
        except ConnectionResetError as e:
            logging.error("ConnectionResetError ", e)
            sleep(30)
            db_connector = DBConnector().get_connection()
        except Exception as e:
            logging.error("Deletesql Error ")
            logging.info(q)
            logging.error(e)
            passed = True
            

if __name__ == '__main__':
    # print(type(create_mysql_connector()))
    con = create_mysql_connector()
    # cursor = con.cursor()
    # cursor.execute("SELECT mail_log_id, label FROM mail_label_relevance order by created_at DESC limit 1")
    # res = cursor.fetchall()
    # print(res)
