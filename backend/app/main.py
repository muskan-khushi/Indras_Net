from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.database import db
from app.routers import simulation, graph

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP LOGIC ---
    print("🚀 Initializing Indra's Net Architecture...")
    
    # Enforce Schema Constraints 
    constraints = [
        "CREATE CONSTRAINT IF NOT EXISTS FOR (c:Company) REQUIRE c.ticker IS UNIQUE",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (m:Macro) REQUIRE m.id IS UNIQUE",
        "CREATE INDEX IF NOT EXISTS FOR (c:Company) ON (c.sector)"
    ]
    with db.get_session() as session:
        for q in constraints:
            session.run(q)
            print(f"   ⚙️ Schema Constraint Enforced: {q[:40]}...")
            
    yield
    # --- SHUTDOWN LOGIC ---
    db.close()
    print("🛑 System Shutdown.")

app = FastAPI(title="Indra's Net API", lifespan=lifespan)

# Allow React Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(simulation.router, prefix="/api/sim", tags=["Simulation"])
app.include_router(graph.router, prefix="/api/graph", tags=["Graph"])

@app.get("/")
def health_check():
    return {"status": "operational", "system": "Indra's Net Causal Twin"}