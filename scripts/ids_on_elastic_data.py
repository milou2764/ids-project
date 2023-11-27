"""

Load data from elastic database, and apply machine learning on it

"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler, StandardScaler

import api  # api for es

import os
import glob

from datetime import datetime

from elasticsearch import Elasticsearch


HOST="localhost"
PATH="/opt/data/TRAIN_ENSIBS/"


def get_data():
    #  get database
    data = api.get_all_data()
    final_data = []
    for i in range(len(data)):
        final_data += data[i]['hits']['hits']
    for i in range(len(final_data)):
        final_data[i] = final_data[i]['_source']
    return pd.DataFrame(final_data)

#  unused now
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

    #  Label encoding
    for v in ["appName", "protocolName", "sourcePort"]:
        data[v] = LabelEncoder().fit_transform(data[v])

    #  scale numerical variables
    scaler = MinMaxScaler()

    for v in ["totalSourceBytes", "totalDestinationBytes", "totalDestinationPackets", "duration", "Tag", "protocolName", "destinationPort", "sourcePort"]:
        data[v] = scaler.fit_transform(np.array(data[v]).reshape(-1, 1))

    features = data[["totalSourceBytes", "totalDestinationBytes", "totalDestinationPackets", "protocolName", "sourcePort", "destinationPort", "Tag", "duration"]]
    print("\n" * 30)
    print("features are stored in the features object")
    print("you can print the dataframe with print(features)")
    print("\n" * 5)
    breakpoint()
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
    
    dataset = get_data()

    df_data_preprocessed = preprocess_data(dataset)
    
    df_final = apply_ids(df_data_preprocessed)
        




if __name__ == "__main__":
    main()
