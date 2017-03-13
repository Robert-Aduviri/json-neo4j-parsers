from neo4j.v1 import GraphDatabase, basic_auth
import json

driver = GraphDatabase.driver("bolt://localhost:7687",
auth=basic_auth("neo4j", "admin"))

data_file = open('course_h.json', encoding='utf-8')
data = json.load(data_file)

session = driver.session()

session.run("MATCH (n) DETACH DELETE (n)")

for curso in data['cursos']:
    session.run(("CREATE (c:Curso {{id: '{0}', name: '{1}'}})").format(curso['id'], curso['name']))
    print(curso['name'])

for tema in data['temas']:
    session.run(("MATCH (c:Curso {{id: '{0}'}}) \n"
                 "CREATE (t:Tema {{id: '{1}', name: '{2}'}}) \n"
                 "CREATE (t)-[:PERTENENCE]->(c)").format(tema['tema_id'], tema['id'], tema['name']))

for subtema in data['subtemas']:
    session.run(("MATCH (t:Tema {{id: '{0}'}}) \n"
                 "CREATE (st:Subtema {{id: '{1}', name: '{2}'}}) \n"
                 "CREATE (st)-[:PERTENENCE]->(t)").format(subtema['course_id'], subtema['id'], subtema['name']))

session.close()
