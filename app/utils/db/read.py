import logging
import pandas as pd

from app.utils.db.misc import create_mysql_connector,delete_sql
from app.utils.db.misc import  read_sql, DBConnector#, query_data,
from app import config
from datetime import datetime
import dateutil.relativedelta


def select_news(last_id):
    db_connector = create_mysql_connector(config.db_news)
    
    if last_id is None:
        query = f"SELECT * FROM news order by id desc limit 10" 
    else:
        query = f"SELECT * FROM news where id>{last_id}"
    
    news = read_sql(query,db_connector)
    
    return news


def get_model_s3_index(model_type, biz_id=None, sort_by="date"):
    """
    Counts invoices applicable for training model and returns their total count for each biz

    Parameters
    ----------
    model_type : str
        model type in database table ``trained_models``, 'weeks_to_pay' or 'month_end_pay'
    biz_id : int, default None
        None means global model of all biz
    sort_by : str, default "date"
        choose model by "date" as latest model or "score" as best performed

    Returns
    -------
    id_, s3index : int, str
        model id in database, path to model in s3 bucket
    """
    biz_id = biz_id if biz_id else 0
    query = f""" 
             SELECT id, s3_index FROM trained_models WHERE model='{model_type}' AND biz_id={biz_id}
             """
    if sort_by == 'date':
        query += " ORDER BY updated_at DESC LIMIT 1"
    elif sort_by == 'score':
        if model_type == "weeks_to_pay":
            query += " ORDER BY RMSE_test DESC LIMIT 1"
        elif model_type == "month_end_pay":
            query += " ORDER BY f1_score_test DESC LIMIT 1"
        else:
            raise TypeError("model_type should be 'weeks_to_pay' or 'month_end_pay'")
    else:
        raise TypeError("sort_by should be 'date' or 'score'")
    db_connector = create_mysql_connector(config.db_ml)
    try:
        id_ = pd.read_sql_query(query, db_connector).values[0][0]
        s3index = pd.read_sql_query(query, db_connector).values[0][1]
    except IndexError:
        logging.warning(f"No pre-trained models was found in DB for model_type={model_type} and biz_id={biz_id}")
        id_, s3index = 0, ''
    return id_, s3index


if __name__ == '__main__':
    from time import time
    t1 = time()
    logging.info(get_invoice_count(404))
    logging.info(time()-t1)
    # logging.info(get_model_s3_index(model_type="month_end_pay", biz_id=902, sort_by="date"))
