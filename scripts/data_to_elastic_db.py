from elasticsearch import Elasticsearch
from xml.etree.ElementTree import parse
from utils import element_to_dict
import os
import glob
import socket

from utils import get_project_dir

DATA_PATH = get_project_dir()+'/data/TRAIN_ENSIBS/'

def claim_datasets(path):
    
    paths = glob.glob(os.path.join(path, "*"))
    
    for p in paths:
        yield p, pd.read_xml(p)

ind = 'iscx'
    
def main():
    print('''
~~~~~~~~~~~~~~~~~~~~~~~
REMOVING EXISTING INDEX
~~~~~~~~~~~~~~~~~~~~~~~
''')
    es = Elasticsearch([{'host': 'localhost',
                         'port': 9200,
                         'scheme': "http"}])
 
    es.options(ignore_status=[400,404]).indices.delete(index='test-index')
    
    print('''
~~~~~~~~~~~~~~
CREATING INDEX
~~~~~~~~~~~~~~
''')
    
    payload='''{
    "mappings": {
        "properties": {
            "protocolName": {
                "type": "keyword"
            },
            "appName": {
                "type": "keyword"
            }
        }
    }
}'''

    headers = '''Content-Type: application/json
Content-Length: {}
'''.format(len(payload))

    req = '\n'.join(['PUT {}?pretty HTTP/1.1'.format(ind),
                         headers,
                         payload]).encode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 9200))
    sock.send(req)
    print(sock.recv(1024).decode())

    print('''
~~~~~~~~~~~~~~~~
SENDING THE DATA
~~~~~~~~~~~~~~~~
''')
    i=0
    bulk=''
    bulk_size=0
    max_bulk_size=1000
    bulk_data=[]
    paths = glob.glob(os.path.join(DATA_PATH, "*"))
    for p in paths:
        print(p)
        tree = parse(p)
        root = tree.getroot()
        for child in root:
            flow = element_to_dict(child)

            op_dict = {
                "index": {
                    "_index": ind,
                    "_id": i
                }
            }

            bulk_data.append(op_dict)
            bulk_data.append(flow)
            i+=1

            if len(bulk_data)>max_bulk_size:
                es.bulk(operations=bulk_data)
                bulk_data=[]
        es.bulk(operations=bulk_data)

if __name__ == "__main__":
    main()
