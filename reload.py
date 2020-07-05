from py2neo import Graph, Node, Relationship
import json
import os
import requests
from pandas import DataFrame
from flask import Flask
from flask import request
app = Flask(__name__)


graph = Graph("bolt://123.57.203.185:7687/db/data/", username="neo4j", password="kuda")

theCypherQuery = '''MERGE (j:%s {name: $subject})
MERGE (m:%s {name: $_object})
MERGE (j)-[r:%s]->(m)
RETURN id(j),type(r),id(m)'''

nodeQuery = """
match (n) where n.name=$name return n
"""

relationQuery = """
match (a)-[r]->(b) where a.name=$a_name and b.name=$b_name return r
"""

id_file_path = "/home/lx/IdeaProject/gAnswer/data/pkubase/fragments/id_mappings/pkubase_entity_id.txt"
triple_file_path = "/home/lx/IdeaProject/gAnswer/data/pkubase/triple.txt"


def check_if_node_exist(name):
    res = graph.run(nodeQuery, parameters={'name': name}).data()
    if len(res) > 0:
        return True
    else:
        return False


def check_if_rel_exist(a_name, b_name):
    res = graph.run(relationQuery, parameters={'a_name': a_name, 'b_name': b_name}).data()
    if len(res) > 0:
        return True
    else:
        return False


def insert(thisCypherQuery, subject_type, subject, object_type, _object, predicate):
    query = thisCypherQuery % (subject_type, object_type, predicate)
    cypherResult = graph.run(query, parameters={'subject': subject, '_object': _object}).data()
    return cypherResult


def get_predicates():
    data = DataFrame(graph.run("match ()-[r]->() return distinct type(r)").data())
    predicates = []
    for index, row in data.iterrows():
        predicates.append(row.to_list()[0])
    return predicates


def get_labels():
    label_list = []
    labels = DataFrame(graph.run("call db.labels()").data())
    for index, row in labels.iterrows():
        # if index == 0:
        #     continue
        label_list.append(row.to_list()[0])
    return label_list




@app.route('/', methods=["POST"])
def rest():
    res = request.data.decode('UTF-8').replace("'",'"')
    spo_obj = json.loads(res)
    spo_list = spo_obj['spos']
    new_entity = ""
    for spo in spo_list:
        subject_exist = check_if_node_exist(spo['subject'])
        object_exist = check_if_node_exist(spo['object'])
        triple_exist = check_if_rel_exist(spo['subject'], spo['object'])

        res = insert(theCypherQuery, spo['subject_type'], spo['subject'], spo['object_type'], spo['object'],
                     spo['predicate'])
        data = DataFrame(res)

        for index, row in data.iterrows():

            if not subject_exist:
                new_entity += spo['subject'] + ","
                if spo['subject_type'] == 'Date' or spo['subject_type'] == 'Number' or spo['subject_type'] == 'Text':
                    triple_file.write(str(row['id(j)']) + ' ' + '48 -1\n')
                else:
                    triple_file.write(str(row['id(j)']) + ' ' + '48 ' + str(labels.index(spo['subject_type'])) + '\n')
                id_file.write('<' + spo['subject'] + '>\t' + str(row['id(j)']) + '\n')

            if not object_exist:
                new_entity += spo['object'] + ","
                id_file.write('<' + spo['object'] + '>\t' + str(row['id(m)']) + '\n')
                if spo['object_type'] == 'Date' or spo['object_type'] == 'Number' or spo['object_type'] == 'Text':
                    triple_file.write(str(row['id(m)']) + ' ' + '48 -1\n')
                else:
                    triple_file.write(str(row['id(m)']) + ' ' + '48 ' + str(labels.index(spo['object_type'])) + '\n')

            if not triple_exist:
                triple_file.write(
                    str(row['id(j)']) + ' ' + str(predicates.index(row['type(r)'])) + ' ' + str(row['id(m)']) + '\n')

    new_entity = new_entity[:-1]
    os.system("python /home/lx/PycharmProjects/kuda2.0/genrate_fragments/step5_get_entity_fragment.py")
    os.system("python /home/lx/PycharmProjects/kuda2.0/genrate_fragments/step6_get_type_fragment.py")
    os.system("python /home/lx/PycharmProjects/kuda2.0/genrate_fragments/step7_get_predicate_fragment.py")
    requests.post('http://localhost:8082/gReload/', data=new_entity.encode('utf-8'))
    return ""

if __name__ == '__main__':
    predicates = get_predicates()
    labels = get_labels()
    id_file = open(id_file_path, "a+")
    triple_file = open(triple_file_path, "a+")
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0", port=5000, debug=True)