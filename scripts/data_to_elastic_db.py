from lxml import etree
from elasticsearch import Elasticsearch, helpers
import os
import glob
import pandas as pd
import re, string
from math import isnan
import socket


DATA_PATH = "/opt/data/TRAIN_ENSIBS/"

def claim_datasets(path):
    
    paths = glob.glob(os.path.join(path, "*"))
    
    for p in paths:
        yield p, pd.read_xml(p)

        

def main():

    #  init elasticsearch obj
    es = Elasticsearch([{'host': 'localhost',
                         'port': 9200,
                         'scheme': "http"}])
    
    print('''
~~~~~~~~~~~~~~~~~~~~~~
REMOVING EXISTING DATA
~~~~~~~~~~~~~~~~~~~~~~
''')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("localhost", 9200))
    sock.send(b'DELETE _all?pretty HTTP/1.1\r\n\r\n')
    print(sock.recv(1024).decode())

    #  claim dataset in pandas format
    for p, dataset in claim_datasets(DATA_PATH):
        ind = p[len(p) - p[::-1].find("/") : - 4]
        ind = re.sub(r'\W+', '', ind).lower()

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
        print(req.decode())
        print(sock.recv(1024).decode())
        for index, row in dataset.iterrows():
            document = row.to_dict()
            for key in document:
                value=document[key]
                if type(value)==float and isnan(document[key]):
                    document[key]='NULL'
            es.index(index=ind, document=document,id=index)

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


