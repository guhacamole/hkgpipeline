from neo4j import GraphDatabase

class Neo4jConnection:
    
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response

emrconn = Neo4jConnection("bolt://localhost:7687","guhacamole","password")

emrconn.query("CREATE OR REPLACE DATABASE graphdb1")

query = '''
USING PERIODIC COMMIT 500
LOAD CSV WITH HEADERS FROM
"https://raw.githubusercontent.com/guhacamole/neo4jfiles/master/prelim_pipeline/data-5m.csv"
AS line FIELDTERMINATOR ','
MERGE (disease:Disease {name: line.sb})
MERGE (object:Object {name: line.ob})
MERGE (disease)-[r:reln {type: line.pr, wt: line.wt}]->(object)
'''
emrconn.query(query, db='graphdb1')