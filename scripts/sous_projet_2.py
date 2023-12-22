import glob
import numpy as np
import pandas as pd
import api

import os
from datetime import datetime

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

from sklearn.model_selection import cross_val_score, KFold, cross_validate
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
    flows=api.get_app_flows(flow_code)
    print('number of flows: ',len(flows))

    return pd.DataFrame(flows)

def fake_get_data(flow_code):
    pdlist = []
    for p in glob.glob(os.path.join("/home/user/Documents/cours/ids/TRAIN_ENSIBS", "*")):
        pdlist.append(pd.read_xml(p))
    df = pd.concat(pdlist)
    if flow_code != "na":
        df = df.loc[df["appName"] == flow_code]
    return df


def split_data(data, n):
    res = []
    for d in np.array_split(data, n):
        res.append(pd.DataFrame(d))
    return res


def split_train_test(data):
    X = data.drop("Tag", axis=1)
    y = data["Tag"]
    return X, y


def fit_models(X, y):
    """
    fit models with kfold = 5 on each model in the 'models' variable
    save results in var 'results' and return it
    """
    
    models = {
            "KNN": KNeighborsClassifier(n_neighbors=3),
            "GaussianNB": GaussianNB(),
            "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
            "MLP": MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, random_state=42)
    }

    results = {}

    for modelname, model in models.items():

        n_folds = 5

        #  evaluation metrics
        scoring = {
            'accuracy': make_scorer(accuracy_score),
            'precision': make_scorer(precision_score),
            'recall': make_scorer(recall_score),
            'f1': make_scorer(f1_score)
        }

        #  kfold using sklearn object
        kf = KFold(n_splits=n_folds, shuffle=True)

        #  perform cross-validation
        cv_results = cross_validate(model, X, y, cv=kf, scoring=scoring)

        #  store results
        results[modelname] = cv_results

        #  print or log the cross-validation results
        for metric, values in cv_results.items():
            print(f'{metric.capitalize()} (mean): {values.mean()}')
            print(f'{metric.capitalize()} (std): {values.std()}')    

    return results
    

def main():
    
    print("example get ssh flows")
    
    #  get data
    df_ssh_flows = get_data("SSH")
    
    #  preprocess data

    df_ssh_flows = preprocess_data(df_ssh_flows)

    X, y = split_train_test(df_ssh_flows)

    results = fit_models(X, y)
    breakpoint()


if __name__ == "__main__":
    main()
