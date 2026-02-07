import logging
from app.core.database import db

# --- 1. THE GOLDEN LIST (Canonical Truth) ---
MACROS = [
    {"id": "CRUDE_OIL", "name": "Brent Crude Oil", "type": "Commodity", "unit": "USD/bbl"},
    {"id": "USD_INR", "name": "USD/INR Exchange Rate", "type": "Currency", "unit": "INR"},
    {"id": "REPO_RATE", "name": "RBI Repo Rate", "type": "Policy", "unit": "%"},
    {"id": "CPI_INFLATION", "name": "CPI Inflation", "type": "Economic", "unit": "%"},
    {"id": "GDP_GROWTH", "name": "India GDP Growth", "type": "Economic", "unit": "%"},
    {"id": "US_10Y", "name": "US 10Y Treasury Yield", "type": "Rates", "unit": "%"},
    {"id": "GEOPOLITICS", "name": "Geopolitical Stability Index", "type": "Risk", "unit": "Index"},
    {"id": "MONSOON", "name": "Monsoon Rainfall", "type": "Climate", "unit": "% of Normal"}
]

# A representative subset of Nifty 50 for the 'Big Bang' start
COMPANIES = [
    {"ticker": "RELIANCE.NS", "name": "Reliance Industries", "sector": "Energy"},
    {"ticker": "TCS.NS", "name": "Tata Consultancy Svcs", "sector": "IT"},
    {"ticker": "HDFCBANK.NS", "name": "HDFC Bank", "sector": "Financials"},
    {"ticker": "INFY.NS", "name": "Infosys", "sector": "IT"},
    {"ticker": "ICICIBANK.NS", "name": "ICICI Bank", "sector": "Financials"},
    {"ticker": "HINDUNILVR.NS", "name": "Hindustan Unilever", "sector": "Consumer Goods"},
    {"ticker": "ITC.NS", "name": "ITC Limited", "sector": "Consumer Goods"},
    {"ticker": "SBIN.NS", "name": "State Bank of India", "sector": "Financials"},
    {"ticker": "BHARTIARTL.NS", "name": "Bharti Airtel", "sector": "Telecom"},
    {"ticker": "LICI.NS", "name": "LIC India", "sector": "Financials"},
    {"ticker": "LT.NS", "name": "Larsen & Toubro", "sector": "Construction"},
    {"ticker": "BAJFINANCE.NS", "name": "Bajaj Finance", "sector": "Financials"},
    {"ticker": "MARUTI.NS", "name": "Maruti Suzuki", "sector": "Auto"},
    {"ticker": "ASIANPAINT.NS", "name": "Asian Paints", "sector": "Consumer Goods"},
    {"ticker": "AXISBANK.NS", "name": "Axis Bank", "sector": "Financials"},
    {"ticker": "TITAN.NS", "name": "Titan Company", "sector": "Consumer Goods"},
    {"ticker": "ULTRACEMCO.NS", "name": "UltraTech Cement", "sector": "Materials"},
    {"ticker": "SUNPHARMA.NS", "name": "Sun Pharma", "sector": "Healthcare"},
    {"ticker": "TATASTEEL.NS", "name": "Tata Steel", "sector": "Metals"},
    {"ticker": "NTPC.NS", "name": "NTPC", "sector": "Utilities"},
    {"ticker": "M&M.NS", "name": "Mahindra & Mahindra", "sector": "Auto"},
    {"ticker": "POWERGRID.NS", "name": "Power Grid Corp", "sector": "Utilities"},
    {"ticker": "TATAMOTORS.NS", "name": "Tata Motors", "sector": "Auto"},
    {"ticker": "ADANIENT.NS", "name": "Adani Enterprises", "sector": "Metals"},
    {"ticker": "JSWSTEEL.NS", "name": "JSW Steel", "sector": "Metals"},
    {"ticker": "COALINDIA.NS", "name": "Coal India", "sector": "Mining"},
    {"ticker": "HINDALCO.NS", "name": "Hindalco", "sector": "Metals"},
    {"ticker": "WIPRO.NS", "name": "Wipro", "sector": "IT"},
    {"ticker": "HCLTECH.NS", "name": "HCL Technologies", "sector": "IT"},
    {"ticker": "TECHM.NS", "name": "Tech Mahindra", "sector": "IT"},
    {"ticker": "NESTLEIND.NS", "name": "Nestle India", "sector": "Consumer Goods"},
    {"ticker": "BRITANNIA.NS", "name": "Britannia Industries", "sector": "Consumer Goods"}
]

# Real-world logical dependencies (Fact-grounded)
REAL_LINKS = [
    # Energy & Commodities
    ("RELIANCE.NS", "DEPENDS_ON", "CRUDE_OIL"), ("ASIANPAINT.NS", "DEPENDS_ON", "CRUDE_OIL"),
    ("ONGC.NS", "CORRELATED_WITH", "CRUDE_OIL"), ("BERGEPAINT.NS", "DEPENDS_ON", "CRUDE_OIL"),
    
    # Currency Sensitivity
    ("TCS.NS", "SENSITIVE_TO", "USD_INR"), ("INFY.NS", "SENSITIVE_TO", "USD_INR"),
    ("HCLTECH.NS", "SENSITIVE_TO", "USD_INR"), ("SUNPHARMA.NS", "SENSITIVE_TO", "USD_INR"),
    
    # Interest Rates (Banks & Auto)
    ("HDFCBANK.NS", "SENSITIVE_TO", "REPO_RATE"), ("SBIN.NS", "SENSITIVE_TO", "REPO_RATE"),
    ("BAJFINANCE.NS", "SENSITIVE_TO", "REPO_RATE"), ("MARUTI.NS", "SENSITIVE_TO", "REPO_RATE"),
    
    # Supply Chains
    ("MARUTI.NS", "DEPENDS_ON", "TATASTEEL.NS"), ("TATAMOTORS.NS", "DEPENDS_ON", "TATASTEEL.NS"),
    ("NTPC.NS", "DEPENDS_ON", "COALINDIA.NS"), ("JSWSTEEL.NS", "DEPENDS_ON", "COALINDIA.NS"),
    ("HINDALCO.NS", "DEPENDS_ON", "COALINDIA.NS"),
    
    # Inflation & Consumption
    ("HINDUNILVR.NS", "SENSITIVE_TO", "CPI_INFLATION"), ("NESTLEIND.NS", "SENSITIVE_TO", "CPI_INFLATION"),
    ("TITAN.NS", "SENSITIVE_TO", "GOLD"), # Gold price affects Titan jewelery margins
    
    # Climate
    ("ITC.NS", "DEPENDS_ON", "MONSOON"), ("M&M.NS", "DEPENDS_ON", "MONSOON"),
]

def run_seed():
    print("⚡ INITIATING INDRA'S NET PROTOCOL...")
    
    with db.get_session() as session:
        # 1. CLEAN SLATE (Development Only)
        session.run("MATCH (n) DETACH DELETE n")
        print("   🗑️  Database Wiped (Fresh Start).")

        # 2. INJECT MACROS
        print(f"   ✨ Injecting {len(MACROS)} Macro Factors...")
        for m in MACROS:
            session.run("""
                MERGE (m:Macro {id: $id}) 
                SET m.name = $name, m.type = $type, m.unit = $unit, m.group = 'Macro'
            """, **m)

        # 3. INJECT COMPANIES
        print(f"   🏭 Injecting {len(COMPANIES)} Nifty Constituents...")
        for c in COMPANIES:
            session.run("""
                MERGE (c:Company {ticker: $ticker})
                SET c.name = $name, c.sector = $sector, c.group = 'Company'
            """, **c)

        # 4. WEAVE CONNECTIONS
        print(f"   🔗 Weaving {len(REAL_LINKS)} Strategic Dependencies...")
        for src, rel, tgt in REAL_LINKS:
            # Cypher logic: Match both, create edge. 
            # Note: We check both 'ticker' and 'id' to match Company OR Macro
            session.run(f"""
                MATCH (a), (b)
                WHERE (a.ticker = $src OR a.id = $src) AND (b.ticker = $tgt OR b.id = $tgt)
                MERGE (a)-[r:{rel}]->(b)
                SET r.weight = 0.8
            """, src=src, tgt=tgt)
            
    print("✅ SYSTEM READY. Neural Lattice Hydrated.")

if __name__ == "__main__":
    run_seed()