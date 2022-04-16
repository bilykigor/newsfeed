import re
import traceback
import logging
import sys

from mysql.connector import DataError

from app import config
from app.utils.db.misc import create_mysql_connector

logging.getLogger().setLevel(logging.NOTSET)
console = logging.StreamHandler(sys.stdout)
console.setLevel(logging.INFO)
formater = logging.Formatter('%(name)-13s: %(levelname)-8s %(message)s')
console.setFormatter(formater)
logging.getLogger().addHandler(console)

def insert_records_to_table(table_name, records, primary_key=None, connector=None):
    """
    Extracts emails count statistics, required for creating final report.

    Parameters
    ----------
    table_name : str
        Which table insert to
    records : list or dict
        List of dictionaries where keys are column names and values are column values
    primary_key : str, default None
        Set primary key name to perform ON DUPLICATE KEY UPDATE operation by it.
        By default updating operation if any of column values differs.
    connector : mysql connection

    Returns
    -------
    None
    """
    logging.info(f"Writing to {table_name}")

    if not connector:
        connector = create_mysql_connector(config.db_news)
        connector.__dict__['_temp'] = True

    cursor = connector.cursor()

    records = [records] if isinstance(records, dict) else records
    
    columns = list(records[0].keys())
    batch_size = 100
    for iter_ in range(0, len(records), batch_size):
        sub_records = records[iter_: iter_ + batch_size]
        query = "INSERT INTO {table_name} {columns}\nVALUES\n\t{values}\nON DUPLICATE KEY UPDATE\n\t{dubl_values}". \
            format(table_name=table_name,
                   columns=tuple(columns).__str__().replace("'", ''),
                   values=",\n\t".join(
                       list(map(lambda x: str(tuple([x.get(i) for i in columns])), sub_records))
                   ),
                   dubl_values=",\n\t".join(
                       [f"{column} = VALUES({column})" for column in columns if column != primary_key])
                   )
        query = re.sub(r"(\W)(null|none|nan|nat)(\W)", '\\1NULL\\3', query, flags=re.I)
        query = re.sub(r"(\W)'(null|none|nan|nat)'(\W)", '\\1NULL\\3', query, flags=re.I)
        
        try:
            cursor.execute(query)
            connector.commit()
        except (ValueError, TypeError, DataError):
            logging.error(f"Couldn`t insert records to db:\n {query}")
            logging.error(f'Traceback:\n {traceback.format_exc()}')
            continue
    cursor.close()

    if connector.__dict__.get('_temp'):
        connector.close()


if __name__ == '__main__':
    conn = create_mysql_connector
    insert_records_to_table("timed_text",{},conn)
