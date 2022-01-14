import tqdm
from elasticsearch import Elasticsearch, helpers
import re
es = Elasticsearch()

data_path = './static/new_all_exer.txt'
all_question = {}
with open(data_path, 'r') as freader:
    for line in freader:
        pid, question = [c for c in line.split('.', 1)]
        print(pid)
        question = re.sub('(<.*?>)', '', question)
        question = re.sub('（\w+）', ',', question)
        question = re.sub('_+| +', '', question)
        question = re.sub('（）', '', question)
        all_question[pid] = question
qids = list(all_question.keys())
questions = [all_question[qid] for qid in qids]
if not es.indices.exists(index='test'):
    try:
        es_index = {
            "mappings":{
                "properties": {
                    "question": {
                        "type": "text",
                        "analyzer": "ik_max-word",
                        "search_analyzer": "ik_smart"
                    }
                }
            }
        }
        es.indices.create(index='test', body=es_index, ignore=[400])
        chunk_size = 500
        print("Index data(you can stop it pressing crtl+c onec):")
        with tqdm.tqdm(total=len(qids)) as pbar:
            for start_idx in range(0, len(qids), chunk_size):
                end_idx = start_idx+chunk_size

                bulk_data = []
                # for qid, question in (qids[start_idx:end_idx], questions[start_idx:end_idx]):
                for i in range(start_idx, end_idx):
                    qid = qids[i]
                    question = questions[i]
                    bulk_data.append({
                        "_index": 'test',
                        "_id": qid,
                        "_source": {
                            'question': question
                        }
                    })
                helpers.bulk(es, bulk_data)
                pbar.update(chunk_size)
    except:
        print("during index an exception occured.")

