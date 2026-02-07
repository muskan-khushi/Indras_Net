from fastapi import APIRouter
from pydantic import BaseModel
from app.services.engine import engine
from app.services.market_data import update_live_prices
# 👇 THIS IMPORT IS CRITICAL
from app.services.oracle import generate_economic_briefing 

router = APIRouter()

class ShockRequest(BaseModel):
    target_node: str 
    magnitude: float 

@router.post("/run")
async def run_simulation(shock: ShockRequest):
    # 1. Run the Physics (The Math)
    impact_data = engine.run_shock_simulation(shock.target_node, shock.magnitude)
    
    # 2. Prepare the Result Dictionary
    results = {
        "source": shock.target_node,
        "initial_shock": shock.magnitude,
        "affected_count": len(impact_data),
        "impacts": impact_data
    }
    
    # 3. CALL THE AI (This is the step that was likely missing)
    # We pass the math results to the Oracle to get the text
    print("🧠 API: Calling Oracle...")
    ai_text = generate_economic_briefing(results)
    
    # 4. Attach the text to the response
    results["ai_analysis"] = ai_text  # <--- The Frontend looks for this Key!
    
    return results

@router.post("/sync-market")
async def sync_market():
    await update_live_prices()
    return {"status": "Market Data Synced"}