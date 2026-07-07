# Coralonge-Capstone

### 🔗 Project Links
- [🎬 Watch Video Demo (YouTube)](https://www.youtube.com/watch?v=mYvPeei4iPo)
- [🏆 Official Kaggle Submission Writeup](https://www.kaggle.com/competitions/vibecoding-agents-capstone-project/writeups/coralonge-ai-agent)

Coralonge-Capstone is an innovative Multi-Agent CLI system built with the Gemini API using the official `google-genai` SDK. It serves as an intelligent advisory system orchestrating specialized AI agents to analyze user skincare and supplement routines.

## Project Vision

The primary vision of Coralonge-Capstone is to ensure safety, efficacy, and brand loyalty in personalized health and beauty routines. By identifying biochemical contraindications (e.g., using Retinol and Vitamin C incorrectly) and highlighting missing safety components (e.g., lacking UV protection with Retinol), the system empowers users with structured, safe, and brand-aligned routines.

## Multi-Agent Architecture

The core of this system is powered by a collaborative Multi-Agent orchestration:

1. **Chemist Agent**
   - **Role:** Deep chemical and medical analysis.
   - **Function:** Queries local JSON databases (`product_db.json` and `chemical_db.json`) based on user input. It maps products to active ingredients, cross-references them against chemical data, and identifies any biochemical contraindications, synergies (e.g., Calcium + Vitamin D3), or missing safety components.

2. **Schedule Agent**
   - **Role:** Practical routine drafting and strict business logic enforcement.
   - **Function:** Consumes the Chemist Agent's report to dynamically generate a structured Morning/Night routine table in the terminal.
   - **Strict Business Logic:** If a user includes a Retinol product without a corresponding UV protection/sunscreen product, the Schedule Agent triggers a mandatory safety warning. It then proactively recommends a sunscreen specifically from the **same brand** as the user's input, preventing competitor leakage.

3. **Model Context Protocol (MCP) Server**
   - **Role:** Enforcing fact-based retrieval.
   - **Function:** Connects the agents safely to the verified local JSON databases, serving as an absolute Anti-Hallucination Lock by preventing agents from fabricating ingredient details.

## System Architecture

```mermaid
graph TD
    classDef user fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef security fill:#ffebee,stroke:#c62828,stroke-width:2px,stroke-dasharray: 5 5;
    classDef adk fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef agent fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px;
    classDef db fill:#fff8e1,stroke:#f9a825,stroke-width:2px;

    A[USER / TERMINAL CLI] :::user -->|Product Inputs| B(SECURITY LAYER <br> Transient API Key Verification) :::security
    B -->|Secure Session Trigger| C[MULTI-AGENT ORCHESTRATOR <br> ADK Powered by Gemini API] :::adk
    
    C -->|1. Request Analysis| D[CHEMIST AGENT] :::agent
    D -->|2. Factual Query| E[MCP SERVER <br> Anti-Hallucination Lock] :::security
    E -->|3. Read Local JSON| F[(LOCAL DATABASES <br> product_db / chemical_db)] :::db
    
    F -->|4. Verified Ingredients| D
    D -->|5. Send Chemical Report| C
    
    C -->|6. Staggering Routine Request| G[SCHEDULE AGENT] :::agent
    G -->|7. Enforce Business Rules <br> Brand Loyalty Lock| G
    G -->|8. Generate Tables| H[FINAL INTERACTIVE CLI OUTPUT <br> Routine Table & Critical Warnings] :::user
```

## Security

**API Keys are NEVER hardcoded.** 
To protect sensitive credentials, the Gemini API key is fetched strictly from the local environment using `os.environ.get("GEMINI_API_KEY")`.

## Setup and Installation

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your machine.

### 2. Install the Official SDK
The project uses the new `google-genai` SDK. Install it via pip:
```bash
pip install google-genai
```

### 3. Environment Variable Setup
You must configure your Gemini API Key as an environment variable before running the script.

**On Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your_gemini_api_key_here
```

**On Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_gemini_api_key_here"
```

**On macOS / Linux:**
```bash
export GEMINI_API_KEY="your_gemini_api_key_here"
```

### 4. Running the CLI Application
Navigate to the project root directory and run the main script:
```bash
python main.py
```

## Interactive Testing Scenarios (For Evaluation)
You can test the robustness and dynamic reasoning of the agents using these pre-configured product database combinations:

**Scenario A: Basic Longevity & Synergy Test**
- **Input:** `Coralvit Effervescent Calcium Multivitamin`
- **Agent Behavior:** The system will identify the core ingredients and praise the positive absorption synergy between Calcium and Vitamin D3, placing it safely in the Morning slot.

**Scenario B: Contraindication Staggering & Missing Sunscreen Alert**
- **Input:** `Coralcare Regenerist Series: Retinol, Coralvit Effervescent Calcium Multivitamin`
- **Agent Behavior:** The Chemist Agent flags the biochemical clash between Retinol and Vitamin C. The Schedule Agent then resolves this by separation: plotting the Vitamin C supplement in the **Morning** and Retinol at **Night**. Concurrently, it triggers an **Urgent Safety Warning** for the missing UV component and selectively recommends `Coralcare Regenerist Series: UV Protection` to lock in brand loyalty.

**Scenario C: Complex Routine Overload Test**
- **Input:** `Coralcare Regenerist Series: Retinol, Coralcare Regenerist Series: UV Protection, Coralvit Effervescent Calcium Multivitamin, Coralskin Essential Retinol, Coralskin Daily Sunscreen SPF 50`
- **Agent Behavior:** Demonstrates advanced deductive logic. Instead of overloading the schedule, the agents intelligently group duplicate product functions using an "OR" conditional selection table, guiding the user to choose one safe track.

**Scenario D: Real Brand Fuzzy Matching Test**
- **Input:** `Olay Regenerist Series: Retinol, CDR`
- **Agent Behavior:** Tests the robust fuzzy mapping engine. The system safely maps recognized external products to their closest database equivalents (Coralcare Retinol and Coralvit Multivitamin), applies proper morning/evening staggering logic, and transparently notes the mapping adjustment to the user.

**Scenario E: Out-of-Database Guardrail Test**
- **Input:** `Vaseline Gluta-Hya Serum Burst Lotion Flawless Bright`
- **Agent Behavior:** Enforces the strict Anti-Hallucination Lock. Because the brand and chemical substances are completely absent from the local database, both the Chemist and Schedule agents gracefully decline analysis to guarantee safety rather than hallucinating ingredients.

## ⚠️ IMPORTANT: How to Test Manually via Antigravity IDE Chat
To manually evaluate this program interactively inside the Antigravity IDE Chat window and view the beautifully rendered Markdown table layouts (instead of triggering automated headless test scripts), you MUST explicitly override the agent's autonomous behavior by initializing with this exact prompt:

"Please run python -u main.py now. Don't run the automated scripts from the README. Leave the program open and display a blank prompt because I want to type the product directly here."

Once the interactive unbuffered terminal session opens, you can input product strings manually at your own pace and observe the dynamic Multi-Agent response workflow.

## 🔗 Other Related Links
- **💻 GitHub Repository:** https://github.com/lusianaliu/coralonge-capstone
- **📊 Kaggle Competition:** https://www.kaggle.com/competitions/vibecoding-agents-capstone-project/
