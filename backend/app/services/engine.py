from app.core.database import db

class SimulationEngine:
    def __init__(self, decay_factor=0.2):
        self.decay = decay_factor # 20% dissipation per hop (The "Friction")

    def run_shock_simulation(self, source_id: str, shock_magnitude: float):
        """
        Propagates a shock from a source node through the network.
        source_id: e.g., 'CRUDE_OIL'
        shock_magnitude: e.g., 0.10 (10% increase)
        """
        print(f"🌪️ Simulating Shock: {source_id} -> {shock_magnitude*100}%")
        
        # We use a Breadth-First Search (BFS) approach to propagate
        # Queue stores: (node_id, current_impact_value)
        queue = [(source_id, shock_magnitude)]
        visited = {source_id: shock_magnitude}
        
        results = [] # List of nodes affected

        with db.get_session() as session:
            while queue:
                current_node, current_impact = queue.pop(0)
                
                # If impact is too small (negligible), stop propagating down this path
                if abs(current_impact) < 0.01: 
                    continue

                # Find neighbors
                # We look for OUTGOING relationships (Who depends on this node?)
                # We also grab the correlation/dependency weight
                neighbors_query = """
                MATCH (a {id: $id})-[r]->(b) 
                RETURN b.ticker as target, r.weight as weight, type(r) as type
                UNION
                MATCH (a {ticker: $id})-[r]->(b) 
                RETURN b.ticker as target, r.weight as weight, type(r) as type
                """
                
                result = session.run(neighbors_query, id=current_node)
                
                for record in result:
                    target = record["target"]
                    weight = record["weight"] or 0.5 # Default weight if missing
                    rel_type = record["type"]

                    # --- THE PHYSICS FORMULA ---
                    # 1. Base Transmission
                    transmission = current_impact * weight
                    
                    # 2. Logic Flip (If it's a "Sensitive To" negative correlation)
                    # e.g. If Oil UP, Paint DOWN. 
                    # Ideally, weights should be -1 to 1. For now, we assume positive weight 
                    # means dependency. We need to check if the relationship implies harm.
                    # For simplicity in this iteration: DEPENDS_ON propagates RISK.
                    
                    # 3. Apply Decay (Friction)
                    next_impact = transmission * (1 - self.decay)
                    
                    if target not in visited:
                        visited[target] = next_impact
                        queue.append((target, next_impact))
                        
                        results.append({
                            "node": target,
                            "impact": round(next_impact, 4),
                            "source": current_node
                        })
                        print(f"   ⚡ {target} hit by {next_impact:.4f} shock")

        return results

# Singleton
engine = SimulationEngine()