from neo4j import GraphDatabase
from .config import settings

class Neo4jConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Neo4jConnection, cls).__new__(cls)
            try:
                cls._instance.driver = GraphDatabase.driver(
                    settings.NEO4J_URI, 
                    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
                )
                print("✅ Connected to Neo4j AuraDB")
            except Exception as e:
                print(f"❌ Failed to connect to Neo4j: {e}")
        return cls._instance

    def close(self):
        if self.driver:
            self.driver.close()

    def get_session(self):
        return self.driver.session()

# Global Instance
db = Neo4jConnection()