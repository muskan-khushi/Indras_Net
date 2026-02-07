from fastapi import APIRouter
from app.core.database import db

router = APIRouter()

@router.get("/topology")
async def get_graph_topology():
    """
    Fetches the entire knowledge graph for 3D visualization.
    """
    query = """
    MATCH (n)-[r]->(m)
    RETURN n, r, m
    """
    
    nodes = {}
    links = []
    
    with db.get_session() as session:
        result = session.run(query)
        
        for record in result:
            source = record["n"]
            target = record["m"]
            rel = record["r"]
            
            # Process Source Node
            s_id = source.get("ticker") or source.get("id")
            if s_id not in nodes:
                nodes[s_id] = {
                    "id": s_id,
                    "label": source.get("name", s_id),
                    "group": source.get("group", "Unknown"),
                    # Visual sizing based on importance
                    "val": 20 if source.get("group") == "Macro" else 10 
                }
            
            # Process Target Node
            t_id = target.get("ticker") or target.get("id")
            if t_id not in nodes:
                nodes[t_id] = {
                    "id": t_id,
                    "label": target.get("name", t_id),
                    "group": target.get("group", "Unknown"),
                    "val": 10
                }
            
            # Process Link
            links.append({
                "source": s_id,
                "target": t_id,
                "type": rel.type,
                "weight": rel.get("weight", 0.5)
            })

    return {
        "nodes": list(nodes.values()),
        "links": links
    }