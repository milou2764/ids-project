import numpy as np
import pandas as pd

from datetime import datetime

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler


def preprocess_data(data):
    data = pd.DataFrame(data)
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
    return features

def duration_from_dates(d1, d2):
    '''
    Used in the preprocessing
    '''
    model = "%Y-%m-%dT%H:%M:%S"
    date_d1 = datetime.strptime(d1, model)
    date_d2 = datetime.strptime(d2, model)

    delta = date_d1 - date_d2

    return delta.total_seconds()

def encode_tag(tag):
    '''
    Used in the preprocessing
    '''
    return 1 if tag == "Attack" else "0"
