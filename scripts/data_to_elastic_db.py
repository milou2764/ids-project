from elasticsearch import Elasticsearch
import xml.etree.ElementTree as ET
import os
import glob
import socket


DATA_PATH = "/opt/data/TRAIN_ENSIBS/"

def claim_datasets(path):
    
    paths = glob.glob(os.path.join(path, "*"))
    
    for p in paths:
        yield p, pd.read_xml(p)

ind = 'iscx'
bulk=''
bulk_size=0
    
def send_bulk():
    global bulk
    global bulk_size
    headers = '''Content-Type: application/json
Content-Length: {}
'''.format(len(bulk))

    req = '\n'.join(['POST _bulk?pretty HTTP/1.1',
                                                headers,
                                                bulk]).encode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 9200))
    sock.send(req)
    #print(req.decode())
    print(sock.recv(1024).decode())
    bulk=''
    bulk_size=0

def main():
    global bulk
    global bulk_size

    print('''
~~~~~~~~~~~~~~~~~~~~~~
REMOVING EXISTING DATA
~~~~~~~~~~~~~~~~~~~~~~
''')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 9200))
    sock.send(b'DELETE _all?pretty HTTP/1.1\r\n\r\n')
    print(sock.recv(1024).decode())
    
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

    #  init elasticsearch obj
    es = Elasticsearch([{'host': 'localhost',
                         'port': 9200,
                         'scheme': "http"}])
   
    i=0
    max_bulk_size=1000
    bulk_data=[]
    paths = glob.glob(os.path.join(DATA_PATH, "*"))
    for p in paths:
        #dataset = pd.read_xml(p)
        print(p)
        tree = ET.parse(p)
        root = tree.getroot()
        #for index, row in dataset.iterrows():
        for child in root:
            #flow = row.to_dict()
            flow=child.attrib
            for att in child:
                flow[att.tag]=att.text
            
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

"""

BACKUP

"""

def etree_to_dict(t):
    d = {t.tag : map(etree_to_dict, t.iterchildren())}
    d.update(('@' + k, v) for k, v in t.attrib.iteritems())
    d['text'] = t.text
    return d


def get_big_dictionnary(i: int) -> dict:
    tree = etree.parse(datasets[i])
    root = tree.getroot()
    d = etree_to_dict(root)
    return d


