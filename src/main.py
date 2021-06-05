import requests
import os
import sys
import argparse
import datetime
import json
import time
import threading

from sodapy import Socrata
from math import ceil
from datetime import datetime, date
from time import time

from config import mappings as es_mappings
from elastic_helper import (
    ElasticHelperException, 
    insert_doc,
    try_create_index,
)


DATASET_ID = os.environ.get("DATASET_ID")
APP_TOKEN = os.environ.get("APP_TOKEN") 
ES_HOST = os.environ.get("ES_HOST") 
ES_USERNAME = os.environ.get("ES_USERNAME")
ES_PASSWORD = os.environ.get("ES_PASSWORD")
DATA_URL = "data.cityofnewyork.us"


def call_api(id_, page_size, offset):
    s1 = time()
    resp = client.get(id_, limit=page_size, offset=offset)
    print(f"API CALL TIME: {time()-s1}")
    
    with open('output.txt', 'a+') as fh:
        for item in resp:
            fh.write(f"{str(item)}\n")


if __name__ == '__main__':
    client = Socrata (DATA_URL, APP_TOKEN)
    results = client.get(DATASET_ID, select='COUNT(*)') 
    total = int(results[0]['COUNT'])
    parser = argparse.ArgumentParser()
    parser.add_argument('--page_size', type=int, help='how many rows to get per page', required=True)
    parser.add_argument('--num_pages',type=int, help='how many pages to get in total', required=False)
    args = parser.parse_args()
    page_size = args.page_size
    num_pages = args.num_pages
    
    
    s0 = time()
    threads = []
    for i in range(num_pages):
        t = threading.Thread(
            target=call_api,
            args=(DATASET_ID, page_size, i*page_size, ),
        )
        threads.append(t)
        t.start()
    # wait for all to finish
    for th in threads:
        th.join()
    print(f"DONE {time()-s0}")
    
    
    try:
        try_create_index(
            "nyc",
            ES_HOST,
            mappings=es_mappings,
            es_user=ES_USERNAME,
            es_pw=ES_PASSWORD,
        )
    except ElasticHelperException as e:
        print("Index already exists! skipping")
        print(f"{e}")
        
    rows = client.get(DATASET_ID, limit=page_size, offset=num_pages, order=":id")
    
    for row in rows:
        try:
            row['summons_number'] = float(row['summons_number'])
            row['fine_amount'] = float(row['fine_amount'])
            row['penalty_amount'] = float(row['penalty_amount'])
            row['interest_amount'] = float(row['interest_amount'])
            row['reduction_amount'] = float(row['reduction_amount'])
            row['payment_amount'] = float(row['payment_amount'])
            row['amount_due'] = float(row['amount_due'])
            row['issue_date'] = str(datetime.strptime(row['issue_date'], "%m/%d/%Y").date())
            
        except Exception as e:
            print("SKIPPING! Failed to transform row: {row}. Reason: {e}")
            continue
        try:
            ret = insert_doc(
                "nyc", 
                ES_HOST,
                data=row,
                es_user=ES_USERNAME,
                es_pw=ES_PASSWORD,
            )
            print(ret)
        except ElasticHelperException as e:
            print(e)
  