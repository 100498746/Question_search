from elasticsearch import Elasticsearch, helpers

class ESphy(object):
    def __init__(self):
        self.es = Elasticsearch()

    def bm25search(self, query):
        Es_search = self.es
        result = []
        bm25 = Es_search.search(index="test", body={"query": {"match": {"question": query}}})
        for hit in bm25['hits']['hits'][0:5]:
            result.append([hit['_source']['question'], hit['_score'], hit['_id']])
        return result

# embed = ESphy()
# text = "关于摩擦起电，下列说法正确的是（ ）（A）只有正电荷从一个物体转移到另一个物体（B）只有电子从一个物体转移到另一个物体（C）正负电荷同时按相反方向方向转移（D）以上三种情况都有可能"
# print(text)
# ss = embed.bm25search(text)
# print(ss)
