from elasticsearch import Elasticsearch

es = Elasticsearch('http://localhost:9200')
index='iscx'

def get_indices() -> list:
    """
    Returns the list of all current indices in the elasticsearch database
    """
    return list(es.indices.get_alias(index="*").keys())

def get_protocols() -> list:
    """
    Returns the list of all the (distinct) protocols contained in the XML files
    """
    field = 'protocolName'
    protocols = []
    aggregation_query = {'unique_values':{'terms':{'field':field}}}
    result = es.search(index=index, aggs=aggregation_query)
    protocols += [bucket["key"] for bucket in result["aggregations"]["unique_values"]["buckets"]]
    return protocols

def get_protocol_flows(protocol: str) -> list:
    '''
    Returns the list of flows for a given protocol
    '''
    results = []
    search_query = {
            "match": {
                'protocolName': protocol
                }
            }
    result = es.search(index=index, query=search_query)
    results.append(result)

    return results

def get_protocols_flows_count() -> dict:
    '''
    Returns the number of flows for each protocols
    '''
    protocols = get_protocols()
    counts = {}
    for protocol in protocols:
        counts[protocol] = 0
        search_query = {
                'match': {
                    'protocolName': protocol
                    }
                }
        result = es.count(index=index, query=search_query)
        counts[protocol] += result['count']
    return counts

def get_protocols_total_bytes() -> dict:
    '''
    Returns  the total source/destination Bytes for each protocol
    '''
    protocols = get_protocols()
    total_bytes = {}
    indices = get_indices()
    for protocol in protocols:
        total_bytes[protocol] = {'source': 0, 'destination': 0}
        query = {
                'term': {
                    'protocolName': protocol
                    }
                }
        aggregation_query = {
                'total_sum_source': {
                    'sum': {
                        'field': 'totalSourceBytes'
                        }
                    },
                'total_sum_destination': {
                    'sum': {
                        'field': 'totalDestinationBytes'
                        }
                    }
                }
        result = es.search(index=index, query=query, aggs=aggregation_query)
        total_bytes[protocol]['source'] += result['aggregations']['total_sum_source']['value']
        total_bytes[protocol]['destination'] += result['aggregations']['total_sum_destination']['value']
    return total_bytes


def get_protocols_total_packets() -> dict:
    '''
    Returns  the total source/destination Bytes for each protocol
    '''
    protocols = get_protocols()
    total_bytes = {}
    for protocol in protocols:
        total_packets[protocol] = {'source': 0, 'destination': 0}
        query = {
                'term': {
                    'protocolName': protocol
                    }
                }
        aggregation_query = {
                'total_sum_source': {
                    'sum': {
                        'field': 'totalSourceBytes'
                        }
                    },
                'total_sum_destination': {
                    'sum': {
                        'field': 'totalDestinationBytes'
                        }
                    }
                }
        result = es.search(index=index, query=query, aggs=aggregation_query)
        total_packets[protocol]['source'] += result['aggregations']['total_sum_source']['value']
        total_packets[protocol]['destination'] += result['aggregations']['total_sum_destination']['value']
    return total_packets

def get_apps() -> list:
    """
    Returns the list of all the (distinct) apps contained in the XML files
    """
    apps = []
    aggregation_query = {'unique_values':{'terms':{'field':'appName','size':1000000}}}
    result = es.search(index='iscx', aggs=aggregation_query)
    apps += [bucket["key"] for bucket in result["aggregations"]["unique_values"]["buckets"]]
    return apps

def get_app_flows_count(app: str) -> int:
    '''
    Returns the number of flows for a single app
    '''
    search_query = {'match': {'appName': app}}
    return es.count(index=index, query=search_query)['count']

def get_app_flows(app: str) -> list:
    '''
    Returns the list of flows for a given app
    '''
    flows=[]
    query = {'term':{'appName':app}} 
    initial_results=es.search(index='iscx',query=query,scroll='1m')
    scroll_id=initial_results['_scroll_id'] 
    while True:
        next_results=es.scroll(scroll_id=scroll_id,scroll='1m')
    
        if len(next_results['hits']['hits'])==0:
            break
    
        scroll_id = next_results['_scroll_id']
        next_results=next_results['hits']['hits']
        flows+=[e['_source'] for e in next_results]

    return flows


def get_all_data() -> dict:
    apps = get_apps()
    indices = get_indices()
    results = []
    for app in apps:
        for index in indices:
            search_query = {
                "match": {
                    'appName': app
                }
            }
            result = es.search(index=index, query=search_query)
            results.append(result)
    return results


def get_apps_flows_count() -> dict:
    '''
    Returns the number of flows for each apps
    '''
    apps = get_apps()
    counts = {}
    for app in apps:
        counts[app] = 0
        search_query = {'match': {'appName': app}}
        result = es.count(index=index, query=search_query)
        counts[app] += result['count']
    return counts

def get_apps_total_bytes() -> dict:
    '''
    Returns  the total source/destination Bytes for each app
    '''
    apps = get_apps()
    total_bytes = {}
    indices = get_indices()
    for app in apps:
        total_bytes[app] = {'source': 0, 'destination': 0}
        for index in indices:
            query = {
                'term': {
                    'appName': app
                }
            }
            aggregation_query = {
                'total_sum_source': {
                    'sum': {
                        'field': 'totalSourceBytes'
                    }
                },
                'total_sum_destination': {
                    'sum': {
                        'field': 'totalDestinationBytes'
                    }
                }
            }
            result = es.search(index=index, query=query, aggs=aggregation_query)
            total_bytes[app]['source'] += result['aggregations']['total_sum_source']['value']
            total_bytes[app]['destination'] += result['aggregations']['total_sum_destination']['value']
    return total_bytes


def get_apps_total_packets() -> dict:
    '''
    Returns  the total source/destination Bytes for each app
    '''
    apps = get_apps()
    total_bytes = {}
    indices = get_indices()
    for app in apps:
        total_packets[app] = {'source': 0, 'destination': 0}
        for index in indices:
            query = {
                'term': {
                    'appName': app
                }
            }
            aggregation_query = {
                'total_sum_source': {
                    'sum': {
                        'field': 'totalSourceBytes'
                    }
                },
                'total_sum_destination': {
                    'sum': {
                        'field': 'totalDestinationBytes'
                    }
                }
            }
            result = es.search(index=index, query=query, aggs=aggregation_query)
            total_packets[app]['source'] += result['aggregations']['total_sum_source']['value']
            total_packets[app]['destination'] += result['aggregations']['total_sum_destination']['value']
    return total_packets


