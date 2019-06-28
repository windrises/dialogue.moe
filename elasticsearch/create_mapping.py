from elasticsearch import Elasticsearch

es = Elasticsearch('***', timeout=60)

index_name = 'sub'
mapping = {
    'mappings': {
        'sub': {
            'properties': {
                'subject_id': {'type': 'keyword'},
                'sub_id': {'type': 'keyword'},
                'sub_title': {'type': 'text', 'analyzer' : 'ik_max_word', 'search_analyzer': 'ik_max_word'},
                'sub_url': {'type': 'keyword', 'index' : False},
                'up_data': {'type': 'date', 'format': 'yyyy-MM-dd', 'index' : False},
                'dl_cnt': {'type': 'integer', 'index' : False},
                'dl_url': {'type': 'keyword', 'index' : False}
            }
        },
        'file': {
            'properties': {
                'file_id': {'type': 'keyword'},
                'file_name': {'type': 'text', 'analyzer' : 'ik_max_word', 'search_analyzer': 'ik_max_word'}
            }
        },
        'dialogue': {
            'properties': {
                'dialogue_id': {'type': 'keyword'},
                'start': {'type': 'date', 'format': 'HH:mm:ss:SSS', 'index' : False},
                'end': {'type': 'date', 'format': 'HH:mm:ss:SSS', 'index' : False},
                'text': {'type': 'text', 'analyzer' : 'ik_smart', 'search_analyzer': 'ik_smart'}
            }
        }
    }
}
es.indices.create(index=index_name, body=mapping)

index_name = 'subject'
type_name = 'anime'
mapping = {
    'mappings': {
        type_name: {
            'properties': {
                'id': {'type': 'keyword', 'index' : False},
                'namechs': {'type': 'text', 'analyzer' : 'ik_max_word', 'search_analyzer': 'ik_max_word'},
                'namejp': {'type': 'text', 'analyzer' : 'ik_max_word', 'search_analyzer': 'ik_max_word'},
                'cat': {'type': 'keyword', 'index' : False},
                'eps': {'type': 'keyword', 'index' : False},
                'date': {'type': 'keyword', 'index' : False},
                'img': {'type': 'keyword', 'index' : False},
                'sub_ids': {'type': 'keyword', 'index' : False}
            }
        }
    }
}
es.indices.create(index=index_name, body=mapping)
