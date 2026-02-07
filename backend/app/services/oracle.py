import os
import random
from groq import Groq
from app.core.config import settings

# Try to initialize Groq, but don't crash if key is missing
try:
    client = Groq(api_key=settings.GROQ_API_KEY)
except:
    client = None

def generate_economic_briefing(simulation_results: dict):
    """
    Uses Llama 3 to explain results. Falls back to 'Templated Logic' if AI is offline.
    """
    source = simulation_results.get("source", "Market Event")
    shock = simulation_results.get("initial_shock", 0)
    impacts = simulation_results.get("impacts", [])

    # Sort impacts
    top_impacts = sorted(impacts, key=lambda x: abs(x["impact"]), reverse=True)[:3]
    nodes_str = ", ".join([n['node'].split('.')[0] for n in top_impacts])

    # --- 1. THE REAL AI PATH ---
    if client and settings.GROQ_API_KEY:
        print("🧠 Oracle: Contacting Llama 3...")
        try:
            prompt = f"""
            You are a Chief Economist. 
            EVENT: {source} shifted by {shock*100:.1f}%.
            TOP IMPACTS: {nodes_str}.
            
            Explain the causal link in 2 sentences. 
            Use professional financial tone. No intros.
            """
            
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192",
                temperature=0.5,
                max_tokens=100,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"⚠️ Groq API Error: {e}")
            # Fall through to the backup logic below

    # --- 2. THE BACKUP LOGIC (Ensures Gold Card Always Appears) ---
    print("⚠️ Oracle: Using Templated Fallback.")
    direction = "surge" if shock > 0 else "crash"
    effect = "positive" if impacts and impacts[0]['impact'] > 0 else "adverse"
    
    return (
        f"The {shock*100:.0f}% {direction} in {source} has triggered a structural {effect} shockwave. "
        f"Significant volatility detected in {nodes_str} due to direct supply chain correlation and sector beta sensitivity."
    )