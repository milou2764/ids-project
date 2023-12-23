from elasticsearch import Elasticsearch

es = Elasticsearch('http://localhost:9200')
index='iscx'

###########
# GENERAL #
###########

def get_documents(field: str, value: str) -> list:
    '''
    Returns all the documents having the specific field and value couple
    '''
    flows=[]
    query = {'term':{field:value}} 
    initial_results=es.search(index=index,query=query,scroll='1m')
    scroll_id=initial_results['_scroll_id'] 
    while True:
        next_results=es.scroll(scroll_id=scroll_id,scroll='1m')
    
        if len(next_results['hits']['hits'])==0:
            break
    
        scroll_id = next_results['_scroll_id']
        next_results=next_results['hits']['hits']
        flows+=[e['_source'] for e in next_results]
    return flows

def get_values(field: str) -> list:
    '''
    Returns all the distinct values in a specific field in all documents
    '''
    values = []
    aggregation_query = {'unique_values':{'terms':{'field':field,'size':1000000}}}
    result = es.search(index=index, aggs=aggregation_query)
    values += [bucket["key"] for bucket in result["aggregations"]["unique_values"]["buckets"]]
    return values

def get_documents_count(field: str, value: str) -> int:
    '''
    Returns the number of documents having the specific field and value couple
    '''
    search_query = {'match': {field: value}}
    return es.count(index=index, query=search_query)['count']

def get_totals(field: str, srcField: str, dstField: str) -> dict:
    '''
    Returns the totals of srcField and dstField sorted with the values of field
    '''
    values = get_values(field)
    totals = {}
    for value in values:
        totals[value] = {'source': 0, 'destination': 0}
        query = {
                'term': {
                    field: value
                    }
                }
        aggregation_query = {
                'total_sum_source': {
                    'sum': {
                        'field': srcField
                        }
                    },
                'total_sum_destination': {
                    'sum': {
                        'field': dstField
                        }
                    }
                }
        result = es.search(index=index, query=query, aggs=aggregation_query)
        totals[value]['source']=result['aggregations']['total_sum_source']['value']
        totals[value]['destination']=result['aggregations']['total_sum_destination']['value']
    return totals

def get_documents_counts(field: str) -> dict:
    '''
    Returns the documents counts sorted with field values
    '''
    values = get_values(field)
    counts = {}
    for value in values:
        counts[value] = get_documents_count(field,value)
    return counts

#############
# PROTOCOLS #
#############

def get_protocols() -> list:
    """
    Returns the list of all the (distinct) protocols contained in the XML files
    """
    return get_values('protocolName')

def get_protocol_flows(protocol: str) -> list:
    '''
    Returns the list of flows for a given protocol
    '''
    return get_documents('protocolName',protocol) 

def get_protocols_flows_count() -> dict:
    '''
    Returns the number of flows for each protocols
    '''
    return get_documents_counts('protocolName')

def get_protocols_total_bytes() -> dict:
    '''
    Returns the total source/destination Bytes for each protocol
    '''
    return get_totals('protocolName','totalSourceBytes','totalDestinationBytes')

def get_protocols_total_packets() -> dict:
    '''
    Returns the total source/destination Bytes for each protocol
    '''
    return get_totals('protocolName','totalSourcePackets','totalDestinationPackets')

################
# APPLICATIONS #
################

def get_apps() -> list:
    """
    Returns the list of all the (distinct) apps contained in the XML files
    """
    return get_values('appName')

def get_app_flows(app: str) -> list:
    '''
    Returns the list of flows for a given app
    '''
    return get_documents('appName',app)

def get_apps_flows_count() -> dict:
    '''
    Returns the number of flows for each apps
    '''
    return get_documents_counts('appName')

def get_apps_total_bytes() -> dict:
    '''
    Returns the total source/destination Bytes for each app
    '''
    return get_totals('appName','totalSourceBytes','totalDestinationBytes')

def get_apps_total_packets() -> dict:
    '''
    Returns the total source/destination packets for each app
    '''
    return get_totals('appName','totalSourcePackets','totalDestinationPackets')


