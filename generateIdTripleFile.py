# match ()-[r]->() where type(r)='专业代码'  return r

from py2neo import Graph
from pandas import DataFrame

graph = Graph("bolt://localhost:7687/db/schemaKG/", username="neo4j", password="kuda")

def get_labels():
    label_list = []
    labels = DataFrame(graph.run("call db.labels()").data())
    for index, row in labels.iterrows():
        if index == 0:
            continue
        label_list.append(row.to_list()[0])
    return label_list

def get_predicates():
    data = DataFrame(graph.run("match ()-[r]->() return distinct type(r)").data())
    predicates = []
    for index, row in data.iterrows():
        predicates.append(row.to_list()[0])
    return predicates


predicates = get_predicates()
with open("./triple.txt", "w") as f:
    data = DataFrame(graph.run("match (a)-[r]->(b) return id(a),type(r),id(b)").data())
    for row in data.iterrows():
        obj = row[1].to_dict()
        f.write(str(obj['id(a)'])+' '+str(predicates.index(obj['type(r)']))+' '+str(obj['id(b)'])+'\n')
# match (a) where a.name='天龙八部'  return labels(a)
labels = get_labels()
with open("./triple.txt","a+") as f:
    data = DataFrame(graph.run("match (a) return id(a),labels(a)").data())
    for row in data.iterrows():
        obj = row[1].to_dict()
        each_labels = obj['labels(a)']
        for label in each_labels:
            if label=='Date' or label=='Number' or label=='Text':
                f.write(str(obj['id(a)']) + ' ' + '48 -1\n')
            else:
                f.write(str(obj['id(a)'])+' '+'48 '+str(labels.index(label))+'\n')