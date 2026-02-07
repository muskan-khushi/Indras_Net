import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Indra's Net"
    VERSION: str = "1.0.0"
    
    # Database
    NEO4J_URI: str = os.getenv("NEO4J_URI")
    NEO4J_USER: str = os.getenv("NEO4J_USERNAME", "neo4j")
    NEO4J_PASSWORD: str = os.getenv("NEO4J_PASSWORD")
    
    # AI Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")

settings = Settings()