from preprocessor import preprocess_data
from cross_validation import get_best_model
from utils import extract_ground_truth, element_to_dict, get_training_data

from checkResultFile import checkResultFile

from xml.etree.ElementTree import parse
from argparse import ArgumentParser
import json
from joblib import dump, load

import os

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

def model_path(app):
    return os.path.dirname(os.path.abspath(__file__))+'/../models/'+app+'.joblib'

def select_and_train(app,modelpath):
    '''
    Select with cross validation, train and saves a classifier
    '''
    print('cross validating models')
    X,y = get_training_data(app)
    model = get_best_model(X,y)

    print('training selected model')
    model.fit(X,y)
    dump(model,modelpath)
    
    return model

if __name__=='__main__':
    parser = ArgumentParser(
            prog='Challenge 1',
            description='Takes the two input xml files and return two prediction files',
            epilog='Authors: Martin Bazire and Émilien André')
    parser.add_argument('fp1',help='path of the xml file')
    parser.add_argument('fp2',help='path of the xml file')

    args=parser.parse_args()
    paths=[args.fp1,args.fp2]

    for p in paths:
        print('loading test data')
        test_flows = extract_flows(p)
        app=test_flows[0]['appName']
        print('appName',app)

        print('preprocessing test data')
        test_flows=preprocess_data(test_flows)

        modelpath = model_path(app)

        model = load(modelpath) if os.path.isfile(modelpath) else select_and_train(app,modelpath)

        X_test,_ = extract_ground_truth(test_flows)

        print('predicting test data')
        results = {'preds':[],'probs':[],'names':['Martin Bazire','Émilien André'],'method':str(model)[:-2],'appName':app,'version':1}
        results['probs'] = model.predict_proba(X_test).tolist()
        for prob in results['probs']:
            results['preds'].append('Normal' if prob[0] < 0.5 else 'Attack')

        # write output
        filepath='martin_emilien_'+app+'_1.res'
        result_file=open(filepath,'w')
        json.dump(results,result_file,ensure_ascii=False)
        result_file.close()

        #verify output
        checkResultFile(filepath)
