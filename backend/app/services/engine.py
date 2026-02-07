from app.core.database import db

class SimulationEngine:
    def __init__(self, decay_factor=0.2):
        self.decay = decay_factor 

    def run_shock_simulation(self, source_id: str, shock_magnitude: float):
        print(f"🌪️ Simulating Shock: {source_id} -> {shock_magnitude*100}%")
        
        queue = [(source_id, shock_magnitude)]
        visited = {source_id: shock_magnitude}
        results = [] 

        with db.get_session() as session:
            while queue:
                current_node, current_impact = queue.pop(0)
                
                if abs(current_impact) < 0.01: 
                    continue

                # 🟢 LOGIC FIX: Look for INCOMING relationships (Upstream Propagation)
                # "Who depends on me?" -> (b)-[r]->(current_node)
                neighbors_query = """
                MATCH (b)-[r]->(a)
                WHERE (a.id = $id OR a.ticker = $id)
                RETURN 
                    COALESCE(b.ticker, b.id) as target, 
                    r.weight as weight, 
                    type(r) as type
                """
                
                result = session.run(neighbors_query, id=current_node)
                
                for record in result:
                    target = record["target"]
                    weight = record["weight"] or 0.5 
                    
                    # 🟢 PHYSICS FIX: If TCS is sensitive to USD, and USD moves,
                    # We simply transmit the shock. 
                    # (Refining this: If relation is 'SENSITIVE_TO' and USD goes UP, 
                    # does TCS go UP or DOWN? For now, we propagate raw magnitude).
                    transmission = current_impact * weight
                    next_impact = transmission * (1 - self.decay)
                    
                    if target not in visited:
                        visited[target] = next_impact
                        queue.append((target, next_impact))
                        
                        results.append({
                            "node": target,
                            "impact": round(next_impact, 4),
                            "source": current_node
                        })
                        print(f"   ⚡ {target} hit by {next_impact:.4f}")

        return results

engine = SimulationEngine()