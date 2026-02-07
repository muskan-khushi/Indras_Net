import yfinance as yf
from app.core.database import db

async def update_live_prices():
    """
    Fetches real-time data from Yahoo Finance and updates Neo4j.
    """
    print("📡 Fetching Real-Time Market Data...")
    
    # 1. Get all tickers from Neo4j
    query = "MATCH (c:Company) RETURN c.ticker as ticker"
    with db.get_session() as session:
        result = session.run(query)
        tickers = [record["ticker"] for record in result]
    
    if not tickers:
        print("⚠️ No tickers found in DB.")
        return

    # 2. Bulk Fetch from Yahoo Finance (Efficient)
    # yfinance allows downloading multiple tickers at once
    ticker_str = " ".join(tickers)
    data = yf.download(ticker_str, period="1d", interval="1m", progress=False)
    
    # 3. Update Neo4j with Real Prices
    # We take the latest 'Close' price
    latest_prices = data['Close'].iloc[-1]
    
    update_query = """
    MATCH (c:Company {ticker: $ticker})
    SET c.current_price = $price, 
        c.last_updated = datetime()
    """
    
    with db.get_session() as session:
        for ticker in tickers:
            try:
                price = float(latest_prices[ticker])
                session.run(update_query, ticker=ticker, price=price)
                print(f"   updated {ticker}: ₹{price:.2f}")
            except Exception as e:
                print(f"   ⚠️ Failed {ticker}: {e}")
                
    print("✅ Market Data Sync Complete.")