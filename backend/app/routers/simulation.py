from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.engine import engine
from app.services.market_data import update_live_prices

router = APIRouter()

class ShockRequest(BaseModel):
    target_node: str  # e.g., "CRUDE_OIL"
    magnitude: float  # e.g., 0.10 for 10%

@router.post("/run")
async def run_simulation(shock: ShockRequest):
    """
    Triggers a causal shockwave through the economy.
    """
    # 1. Calculate the Ripple Effect
    impact_data = engine.run_shock_simulation(shock.target_node, shock.magnitude)
    
    if not impact_data:
        return {"message": "Shock absorbed. No significant impact detected.", "impacts": []}

    # 2. Return the list of damaged nodes
    # The Frontend will use this to turn nodes RED
    return {
        "source": shock.target_node,
        "initial_shock": shock.magnitude,
        "affected_count": len(impact_data),
        "impacts": impact_data
    }

@router.post("/sync-market")
async def sync_market():
    """Manual trigger to fetch Yahoo Finance Data"""
    await update_live_prices()
    return {"status": "Market Data Synced"}