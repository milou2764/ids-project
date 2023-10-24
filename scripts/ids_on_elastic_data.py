"""

Load data from elastic database, and apply machine learning on it

"""

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler



import os
import glob

from datetime import datetime

from elasticsearch import Elasticsearch


HOST="localhost"
PATH="/opt/data/TRAIN_ENSIBS/"


def get_data(host):
    #  get database
    es = Elasticsearch([{'host': host, 'scheme' : 'http', 'port': 9200}])

    query = {
            "query": {
                "match": {
                    "database": "i"
                    }
                }
            }
    
    #  todo
    pass


def fake_get_data(path):
    for p in glob.glob(os.path.join(path, "*")):
        yield p, pd.read_xml(p)


def preprocess_data(data):
    print("columns : ", data.columns)
    
    #  put startDateTime and StopDateTime in a duration variable
    data["duration"] = data.apply(lambda x: duration_from_dates(x['stopDateTime'], x['startDateTime']), axis=1)
    data = data.drop(["stopDateTime", "startDateTime"], axis=1)

    #  encode tag
    data["Tag"] = data.apply(lambda x: encode_tag(x["Tag"]), axis=1)

    #  encode appName
    data["appName"] = LabelEncoder().fit_transform(data["appName"])

    #breakpoint()
    print("3 cols encoded : ")
    print("duration : ", data["duration"])
    print("tag : ", data["Tag"])
    print("appName : ", data["appName"])
    print("Others cols not encoded yet")
    breakpoint()

    #  encode 
    scaler = MinMaxScaler()
    data["totalSourceBytes"] = scaler.fit_transform(data["totalSourceBytes"])

    
    pass


def apply_ids(data):
    pass



"""

Preprocessing functions

"""

def duration_from_dates(d1, d2):
    model = "%Y-%m-%dT%H:%M:%S"
    date_d1 = datetime.strptime(d1, model)
    date_d2 = datetime.strptime(d2, model)
    
    delta = date_d1 - date_d2

    return delta.total_seconds()


def encode_tag(tag):
    return 1 if tag == "Attack" else "0"




"""

Main


"""


def main():
    
    """
    df_data = get_data(HOST)
    """

    #  just for the moment
    for p, dataset in fake_get_data(PATH):
        print("file : ", p)
        df_data_preprocessed = preprocess_data(dataset)
    
        df_final = apply_ids(df_data_preprocessed)
        
        breakpoint()




if __name__ == "__main__":
    main()
