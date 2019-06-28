from django.http import JsonResponse
import json
from elasticsearch import Elasticsearch
import time
from datetime import datetime
import Levenshtein
import re
from dialogue.settings import ES_URL
from dialogue.settings import SUB_INDEX
from dialogue.settings import SUBJECT_INDEX

es = Elasticsearch(ES_URL, timeout=60)
sub_index = SUB_INDEX
subject_index = SUBJECT_INDEX


# Create your views here.
def search(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get('text')
        bangumi_id = data.get('bangumi_id')
        duplicate = data.get('duplicate')
        sort_values = data.get('sort_values')
        history = data.get('history')
        if text is None:
            return JsonResponse({'error': 'error'})
        if bangumi_id is None:
            bangumi_id = ''
        if duplicate is None:
            duplicate = False
        if sort_values is None:
            sort_values = ''
        if history is None:
            history = []

        subject = {}
        subject_id = ''
        sub_ids = []
        if bangumi_id != '':
            try:
                subject_id = bangumi_id
                subject = es.get_source(index=subject_index, doc_type='anime', id=bangumi_id,
                                        _source_include=['namechs', 'namejp', 'eps', 'sub_ids'])
                sub_ids = subject['sub_ids']
            except:
                return JsonResponse({'error': 'Bangumi ID Error'})

        size = 12
        body = {
            'query': {
                'match': {
                    'text': text
                }
            },
            '_source': {
                'includes': ['start', 'end', 'text'],
            },
            'highlight': {
                'fields': {
                    'text': {}
                }
            },
            'size': size,
            'sort': [
                {'_score': 'desc'},
                {'dialogue_id': 'asc'}
            ]
        }
        if bangumi_id != '':
            reg = ''
            for sub_id in sub_ids:
                reg += sub_id + '_.*|'
            reg = reg[:-1]
            body['query'] = {
                        'bool': {
                            'must': [
                                {
                                    'regexp': {
                                        'dialogue_id': reg
                                    }
                                },
                                {
                                    'match': {
                                        'text': text
                                    }
                                }
                            ]
                        }
                    }
        if sort_values != '':
            body['search_after'] = sort_values
        if duplicate:
            body['size'] = size * 2
        dialogues = es.search(index=sub_index, doc_type='dialogue', body=body)

        total = dialogues['hits']['total']
        time_cost = dialogues['took']
        result = {'total': total, 'time_cost': time_cost, 'dialogues': []}
        time_start = time.time()
        dialogue_dict = {}
        if duplicate:
            for dialogue in history:
                try:
                    start = dialogue['time_current']
                    start = datetime.strptime(start, '%H:%M:%S')
                    text = dialogue['text_current']
                    subject_id = dialogue['subject_id']
                    if subject_id not in dialogue_dict:
                        dialogue_dict[subject_id] = [(start, text)]
                    else:
                        dialogue_dict[subject_id].append((start, text))
                except:
                    continue
        for dialogue in dialogues['hits']['hits']:
            dialogue_current = dialogue['_source']
            dialogue_id = dialogue['_id']
            file_id = dialogue_id[:dialogue_id.rfind('_')]
            sub_id = file_id[:file_id.rfind('_')]
            file = {}
            sub = {}
            try:
                file = es.get_source(index=sub_index, doc_type='file', id=file_id,
                                     _source_include=['file_name'])
                sub = es.get_source(index=sub_index, doc_type='sub', id=sub_id,
                                    _source_include=['subject_id', 'sub_title'])
                if bangumi_id == '':
                    subject_id = sub['subject_id']
                    subject = es.get_source(index=subject_index, doc_type='anime', id=subject_id,
                                            _source_include=['namechs', 'namejp', 'eps'])
            except:
                continue
            if duplicate:
                try:
                    x_start = datetime.strptime(dialogue_current['start'][:-4], '%H:%M:%S')
                    x_text = dialogue_current['text']
                    if subject_id not in dialogue_dict:
                        dialogue_dict[subject_id] = [(x_start, x_text)]
                    else:
                        flag = False
                        time_eps = 3
                        text_eps = 5
                        for y_start, y_text in dialogue_dict[subject_id]:
                            if (x_start - y_start).seconds <= time_eps:
                                distance = Levenshtein.distance(x_text, y_text)
                                if distance < text_eps:
                                    flag = True
                                    break
                        dialogue_dict[subject_id].append((x_start, x_text))
                        if flag:
                            continue
                except:
                    pass

            subject_name = subject['namechs']
            if subject_name == '':
                subject_name = subject['namejp']
            dialogue_idx = int(dialogue_id[dialogue_id.rfind('_')+1:])
            dialogue_before = {'text': ''}
            dialogue_after = {'text': ''}
            try:
                if dialogue_idx > 1:
                    dialogue_before = es.get_source(index=sub_index, doc_type='dialogue',
                                                    id=file_id + '_' + str(dialogue_idx - 1),
                                                    _source_include=['text'])
                dialogue_after = es.get_source(index=sub_index, doc_type='dialogue',
                                               id=file_id + '_' + str(dialogue_idx + 1),
                                               _source_include=['text'])
            except:
                pass

            file_name = file['file_name'][:-4]
            eps = subject['eps']
            ep = ''
            if eps != '':
                try:
                    eps = int(eps)

                    pattern = re.compile(r'\d+')
                    ep_results = pattern.findall(file_name)
                    for ep_result in ep_results:
                        try:
                            if int(ep_result) <= eps:
                                ep = ep_result
                                break
                        except:
                            continue
                except:
                    pass

            result['dialogues'].append({
                'dialogues_id': dialogue_id,
                'subject_id': subject_id,
                'subject_name': subject_name,
                'ep': ep,
                'score': round(dialogue['_score'], 3),
                'sub_title': sub['sub_title'],
                'file_name': file_name,
                'text_before': dialogue_before['text'],
                'time_current': dialogue_current['start'][:-4],
                'text_current': dialogue_current['text'],
                'text_current_highlight': dialogue['highlight']['text'][0],
                'text_after': dialogue_after['text'],
                'sort_values': dialogue['sort']
            })
            if len(result['dialogues']) == size:
                break
        return JsonResponse(result)
    return JsonResponse({'error': 'error'})
