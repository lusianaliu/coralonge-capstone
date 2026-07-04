import os
import json
import sys
from google import genai
from google.genai import types

def load_db(file_path):
    """Helper function to load and parse local JSON databases."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Database file not found at {file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON from {file_path}")
        sys.exit(1)

def main():
    # CRITICAL SECURITY: Fetch the Gemini API Key strictly from the environment
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("CRITICAL ERROR: GEMINI_API_KEY environment variable is not set.")
        print("Please set your API key as an environment variable before running the program.")
        sys.exit(1)
        
    client = genai.Client(api_key=api_key)
    
    # Load databases
    chemical_db_path = os.path.join("data", "chemical_db.json")
    product_db_path = os.path.join("data", "product_db.json")
    
    chemical_db = load_db(chemical_db_path)
    product_db = load_db(product_db_path)

    print("==========================================================")
    print(" Welcome to Coralonge-Capstone Multi-Agent CLI System")
    print("==========================================================")
    print("Type 'quit' or 'exit' at any prompt to stop the program.\n")
    
    while True:
        user_input = input("Enter the products you use (separated by commas):\n> ")
        if user_input.strip().lower() in ['quit', 'exit']:
            print("Exiting Coralonge-Capstone. Goodbye!")
            break
            
        if not user_input.strip():
            continue
            
        print("\n[System] Orchestrating agents...")
        
        # ---------------------------------------------------------
        # CHEMIST AGENT
        # ---------------------------------------------------------
        print("\n[Chemist Agent] Analyzing ingredients and contraindications...")
        chemist_prompt = f"""
You are the Chemist Agent for Coralonge-Capstone.
Here is our product database:
{json.dumps(product_db, indent=2)}

Here is our chemical knowledge base:
{json.dumps(chemical_db, indent=2)}

The user has inputted the following products:
"{user_input}"

Task:
1. Identify the matching products from the user's input in the product database.
2. Identify the active ingredients for each product.
3. Cross-reference these ingredients with the chemical knowledge base.
4. Analyze any biochemical contraindications (e.g., Retinol + Vitamin C) or missing safety components (e.g., using Retinol without Sunscreen).

Output a concise, professional report of your findings.
"""
        
        try:
            chemist_response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=chemist_prompt,
            )
            chemist_report = chemist_response.text
            print("\n--- Chemist Agent Report ---")
            print(chemist_report)
            print("----------------------------")
        except Exception as e:
            print(f"Error calling Chemist Agent: {e}")
            continue

        # ---------------------------------------------------------
        # SCHEDULE AGENT
        # ---------------------------------------------------------
        print("\n[Schedule Agent] Drafting schedule and checking business rules...")
        schedule_prompt = f"""
You are the Schedule Agent for Coralonge-Capstone.
Here is the product database:
{json.dumps(product_db, indent=2)}

The user inputted these products:
"{user_input}"

Here is the Chemist Agent's report:
{chemist_report}

Task:
1. Draft a structured Morning/Night routine table based on the user's products and the Chemist Agent's report. 
   - Ensure products with contraindications are scheduled at different times (e.g., Vitamin C in the morning, Retinol at night).
   - If they cannot be used on the same day, warn the user.
2. STRICT BUSINESS LOGIC RULE: If the user inputted a 'Retinol' product but HAS NOT included a Sunscreen/UV product, you MUST trigger a safety warning and actively recommend a Sunscreen from the SAME BRAND as the user's inputted Retinol product. 
   - For example, if they use 'Coralcare Regenerist Series: Retinol', you MUST recommend 'Coralcare Regenerist Series: UV Protection'.
   - If they use 'Coralskin Essential Retinol', you MUST recommend 'Coralskin Daily Sunscreen SPF 50'.
   - DO NOT recommend a competitor's sunscreen.

Output the final routine table, followed by any critical warnings and product recommendations.
"""
        
        try:
            schedule_response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=schedule_prompt,
            )
            print("\n--- Schedule Agent Output ---")
            print(schedule_response.text)
            print("-----------------------------")
        except Exception as e:
            print(f"Error calling Schedule Agent: {e}")
            continue
            
        print("\n" + "="*58 + "\n")

if __name__ == "__main__":
    main()
