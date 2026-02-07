from fastapi import APIRouter
from pydantic import BaseModel
from app.services.engine import engine
from app.services.market_data import update_live_prices

router = APIRouter()

class ShockRequest(BaseModel):
    target_node: str 
    magnitude: float 

@router.post("/run")
async def run_simulation(shock: ShockRequest):
    impact_data = engine.run_shock_simulation(shock.target_node, shock.magnitude)
    
    # 🟢 API FIX: Always return the full structure
    return {
        "source": shock.target_node,
        "initial_shock": shock.magnitude,
        "affected_count": len(impact_data),
        "impacts": impact_data,
        "status": "success" if impact_data else "absorbed"
    }

@router.post("/sync-market")
async def sync_market():
    await update_live_prices()
    return {"status": "Market Data Synced"}