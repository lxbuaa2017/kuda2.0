from py2neo import Graph,Node,Relationship
import json
graph = Graph("bolt://123.57.203.185:7687/db/data/", username="neo4j", password="kuda")
theCypherQuery= '''MERGE (j:%s {name: $subject})
MERGE (m:%s {name: $_object})
MERGE (j)-[r:%s]->(m)
'''
def insert(thisCypherQuery,subject_type,subject,object_type,_object,predicate):
    query = thisCypherQuery % (subject_type,object_type,predicate)
    graph.run(query,parameters = {'subject':subject,'_object':_object}).data()

with open('./neo4j_data.json','r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            try:
                line = json.loads(line)
            except:
                continue
            for spo in line['spo_list']:
                insert(theCypherQuery, spo['subject_type'], spo['subject'], spo['object_type'], spo['object'], spo['predicate'])