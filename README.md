# 🕸️ Indra's Net: Causal Economic Twin

> **A High-Fidelity Digital Twin of the Indian Economy for Causal Inference & Stress Testing.**

**Indra's Net** is an advanced financial simulation platform that models the Indian economy (Nifty 50) as a directed graph. Unlike traditional correlation matrices, it uses **Causal Graph Theory** to simulate how macroeconomic shocks (e.g., Oil Price spikes, Currency Devaluation) propagate through supply chains and banking networks in real-time.

---

## 📉 Problem Statement

Modern financial risk models often fail to capture **second-order effects**.

* **The Linear Trap:** Traditional models assume relationships are linear and isolated (e.g., "If Oil goes up, Paints go down").
* **The Hidden Contagion:** They miss the ripple effects: *Oil up -> Inflation up -> Interest Rates up -> Banking Sector Stress -> Credit Crunch -> Auto Sector slowdown.*
* **Static Data:** Most dashboards show what *happened*, not what *will happen*.

**The Solution:** A **Living Graph Database** that maps the actual dependencies between Macro Factors (Oil, USD/INR, Yields) and Micro Assets (Companies), allowing for dynamic "What-If" stress testing.

---

## 🚀 Key Features

### 1. 🕷️ Causal Graph Engine (Backend)

* **Neo4j Graph Database:** Stores 100+ nodes (Companies, Macros, Risks) and 300+ dependency edges.
* **Physics-Based Propagation:** Uses a custom decay algorithm to simulate shockwaves. A 10% shock to Crude Oil doesn't just hit Asian Paints; it flows downstream to logistics, auto margins, and inflation indices.
* **Real-Time Data:** Integrated with **Yahoo Finance** (`yfinance`) to fetch live market prices for the Nifty 50.

### 2. 🖥️ Institutional-Grade Dashboard (Frontend)

* **"Bloomberg" Aesthetic:** Designed with a `Midnight` dark theme, razor-thin borders, and data-dense layouts for professional use.
* **3D Network Visualization:** Interactive force-directed graph (WebGL) to visualize cluster risks and "Ghost Links" between sectors.
* **Simulation War Room:** A dedicated interface to trigger hypothetical scenarios (e.g., *"What if the Rupee hits 90 vs USD?"*) and watch the red/green impact propagate instantly.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| --- | --- | --- |
| **Frontend** | React (Vite) | High-performance SPA with component-based architecture. |
| **Styling** | Tailwind CSS | Custom "Midnight" palette for financial data visualization. |
| **Charts** | Recharts | Professional time-series and area charts. |
| **Graph Viz** | React-Force-Graph | 3D WebGL rendering of the economic network. |
| **Backend** | Python (FastAPI) | Asynchronous REST API for high-concurrency simulation. |
| **Database** | Neo4j (AuraDB) | Native Graph Database for storing causal relationships. |
| **Inference** | NetworkX | Python library for graph algorithms (BFS/DFS traversal). |
| **Data Feed** | yfinance | Real-time market data pipeline. |

---

## ⚡ Quick Start

### Prerequisites

* Node.js (v18+)
* Python (v3.10+)
* Neo4j AuraDB Account (Free Tier is fine)

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

# Create a .env file with your credentials:
# NEO4J_URI=neo4j+s://...
# NEO4J_USERNAME=neo4j
# NEO4J_PASSWORD=...

# 1. Seed the Database (Build the City)
python -m app.services.seed

# 2. Start the Server (Power the Grid)
uvicorn app.main:app --reload

```

### 2. Frontend Setup

```bash
cd frontend
npm install

# Start the Interface
npm run dev

```

---

## 🎮 How to Use

1. **Overview Dashboard:** Check the "System Status" (Top Right). If Online, real-time Nifty 50 data is flowing.
2. **Network Analysis:** Navigate to the 3D Graph view to explore clusters. Zoom in to see how *Tata Steel* connects to *Auto Majors*.
3. **Simulation Engine (The Core):**
* Go to the **Simulation** tab.
* Select a Trigger (e.g., **Brent Crude Oil**).
* Set Magnitude to **+20%**.
* Click **RUN SCENARIO**.
* *Watch the feed:* See which sectors bleed red (Aviation, Paints) and which turn green (Upstream Oil).



---

## 🔮 Future Roadmap

* [ ] **AI Narrative Layer:** Integrate LLMs (Groq/Llama 3) to generate text explanations for *why* a shock happened.
* [ ] **Second-Order Decay:** Refine the physics engine to handle feedback loops (Inflation -> Rates -> Inflation).
* [ ] **Portfolio Upload:** Allow users to upload their own portfolio to stress-test specific holdings.

---

## 🤝 Contributing

This is an open-source research project. Pull requests for new sector logic or graph optimizations are welcome.

**Author:** [Your Name]
**License:** MIT