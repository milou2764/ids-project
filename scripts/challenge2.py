from bigxml import Parser, xml_handle_element
from dataclasses import dataclass
from sklearn.preprocessing import LabelEncoder
from numpy import argmax
import json
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier

from checkResultFile import checkResultFile
from utils import get_project_dir

def convert_to_integer(value):
    multipliers = {'k': 1000, 'M': 1000000, 'G': 1000000000}  # Define multipliers for K, M, B, G
    suffix = value[-1]  # Get the last character to determine the multiplier
    
    if suffix.isdigit():  # If there's no letter suffix, return the integer value
        return int(float(value))
    
    multiplier = multipliers.get(suffix)  # Get the multiplier from the dictionary
    
    if multiplier:
        numeric_value = float(value.replace(suffix, ''))  # Extract numeric part
        return int(numeric_value * multiplier)
    else:
        return None

tags = {
            'attacker': 0,
            'normal': 1,
            'victim': 2}

@xml_handle_element('dataroot','FFlow')
@dataclass
class Flow():
    atts = {}
    tag: int = 0

    @xml_handle_element('Src_Pt')
    @xml_handle_element('Dst_Pt')
    @xml_handle_element('Packets')
    @xml_handle_element('Flows')
    @xml_handle_element('Tos')
    def handle_int(self, node):
        self.atts[node.name]=int(node.text.replace('.',''))

    @xml_handle_element('Bytes')
    def handle_bytes(self,node):
        self.atts[node.name]=convert_to_integer(node.text)

    @xml_handle_element('Duration')
    def handle_duration(self, node):
        self.atts[node.name]=float(node.text)

    @xml_handle_element('Protocol')
    @xml_handle_element('Flags')
    def handle_string(self, node):
        self.atts[node.name]=node.text

    @xml_handle_element('Tag')
    def handle_tag(self, node):
        self.tag = tags[node.text] if node.text in tags.keys() else 0

def parse_data(p):
    X = []
    y = []
    with open(p,'rb') as f:
        for flow in Parser(f).iter_from(Flow):
            y.append(flow.tag)
            X.append(flow.atts)
    return X,y

def preprocess_data(X):
    X = DataFrame(X)
    for k in ['Protocol','Flags']:
        X[k] = LabelEncoder().fit_transform(X[k])
    print(X)
    return X
    
def get_model(train_fp):
    # Get training data
    print('parsing training data')
    X,y = parse_data(train_fp)
    print('preprocessing training data')
    X = preprocess_data(X)

    # train a random forest classifier
    model = RandomForestClassifier()
    print('training model')
    model.fit(X,y)
    return model

def get_train_test_fp():
    project_path = get_project_dir()
    train_fp = project_path+'data/traffic_os_TRAIN.xml'
    test_fp = project_path+'data/traffic_os_TEST.xml'
    return train_fp,test_fp

if __name__=='__main__':
    train_fp,test_fp = get_train_test_fp()
    model = get_model(train_fp)
    
    # Test model
    print('parsing test data')
    X_test,_ = parse_data(test_fp)
    print('preprocessing test data')
    X_test = preprocess_data(X_test)
    print('predicting test data')
    res_probs = model.predict_proba(X_test).tolist()

    # write result file
    results = {'preds':[],'probs':res_probs,'names':['Martin Bazire','Émilien André'],'method':str(model)[:-2],'version':1}
    for probs in results['probs']:
        results['preds'].append(list(tags.keys())[argmax(probs)])
    filepath = 'martin_emilien_1.res'
    result_file=open(filepath,'w')
    json.dump(results,result_file,ensure_ascii=False)
    result_file.close()

    # verify result file
    checkResultFile(filepath)
