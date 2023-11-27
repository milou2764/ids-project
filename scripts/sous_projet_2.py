
import numpy as np
import pandas as pd
import api

import os
from datetime import datetime

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from sklearn.model_selection import cross_val_score, KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score


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
    return features


def duration_from_dates(d1, d2):
    model = "%Y-%m-%dT%H:%M:%S"
    date_d1 = datetime.strptime(d1, model)
    date_d2 = datetime.strptime(d2, model)

    delta = date_d1 - date_d2

    return delta.total_seconds()

def encode_tag(tag):
    return 1 if tag == "Attack" else "0"


def get_data(flow_code):
    ssh_flows=api.get_app_flows(flow_code)

    flows = []
    for i in range(len(ssh_flows)):
        try:
            flows += ssh_flows[i]['hits']['hits']
        except:
            pass

    for i in range(len(flows)):
        flows[i] = flows[i]["_source"]

    return pd.DataFrame(flows)


def split_data(data, n):
    res = []
    for d in np.array_split(data, n):
        res.append(pd.DataFrame(d))
    return res


def KNN(data):

    knn_classifier = KNeighborsClassifier(n_neighbors=3)  # You can adjust the number of neighbors (k) as needed
    breakpoint()
    #  specify the number of folds for cross-validation
    n_folds = 5

    #  define evaluation metrics
    scoring = {
    'accuracy': make_scorer(accuracy_score),
    'precision': make_scorer(precision_score),
    'recall': make_scorer(recall_score),
    'f1': make_scorer(f1_score)
    }

    #  create a KFold object
    kf = KFold(n_splits=n_folds, shuffle=True)

    #  perform cross-validation
    cv_results = cross_val_score(knn_classifier, X, y, cv=kf, scoring=scoring)

    #  print or log the cross-validation results
    for metric, values in cv_results.items():
        print(f'{metric.capitalize()} (mean): {values.mean()}')
        print(f'{metric.capitalize()} (std): {values.std()}')    



def main():
    
    print("example get shh flows")
    
    #  get data
    df_ssh_flows = get_data("SSH")
    breakpoint()

    #  preprocess data
    df_ssh_flows = preprocess_data(df_ssh_flows)

    #  split data
    df_list_ssh_flows = split_data(df_ssh_flows, 5)


    KNN(df_ssh_flows)
    breakpoint()


if __name__ == "__main__":
    main()
