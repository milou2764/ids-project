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
