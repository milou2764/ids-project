from api import get_app_flows
from preprocessor import preprocess_data
import os

def element_to_dict(child):
    flow={}
    for att in child:
        flow[att.tag]=att.text
    flow['totalSourceBytes']=int(flow['totalSourceBytes'])
    flow['totalDestinationBytes']=int(flow['totalDestinationBytes'])
    flow['totalDestinationPackets']=int(flow['totalDestinationPackets'])
    flow['totalSourcePackets']=int(flow['totalSourcePackets'])
    return flow

def extract_flows(p):
    '''
    p: path of the xml file containing the flows
    '''
    flows=[]
    tree=parse(p)
    root=tree.getroot()
    for child in root:
        flows.append(element_to_dict(child))
    return flows

def extract_ground_truth(data):
    '''
    Extract the ground truth from a pandas dataframe
    '''
    X = data.drop("Tag", axis=1)
    y = data["Tag"]
    return X, y

def get_training_data(app):
    flows = get_app_flows(app)
    flows = preprocess_data(flows)
    X, y = extract_ground_truth(flows)
    return X,y

def get_project_dir():
    return os.path.dirname(os.path.abspath(__file__))+'/../'
