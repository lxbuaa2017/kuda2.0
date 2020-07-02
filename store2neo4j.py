from py2neo import Graph,Node,Relationship
import json
graph = Graph("bolt://localhost:7687/db/schemaKG/", username="neo4j", password="kuda")
graph.delete_all()
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
    #             创建节点
                subject_node = Node(spo['subject_type'],name=spo['subject'])
                object_node = Node(spo['object_type'],name=spo['object'])
                graph.create(subject_node)
                graph.create(object_node)
    #             创建关系
                relation = Relationship(subject_node,spo['predicate'],object_node)
                graph.create(relation)