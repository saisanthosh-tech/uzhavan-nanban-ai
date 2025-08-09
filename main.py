# main.py
import google.generativeai as genai
import json
import re

# Import the functions from your other files
import tools
import prompts

# --- Configuration ---
# PASTE YOUR NEW, SECRET GOOGLE AI STUDIO API KEY HERE
GOOGLE_API_KEY = "AIzaSyApimnZ88HXtIeSbxU7a_MfSejV3Cn9jYs"


# Configure the generative AI model
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash-latest')

# --- The Main Agent Logic (FINAL VERSION) ---
def run_agent(user_query):
    """
    Runs the main logic of the AI agent with location mapping.
    """
    print(f"User Query: {user_query}")

    # Step 1: Analyze the user's query to get intent and entities
    analyzer_prompt = prompts.create_analyzer_prompt(user_query)
    analyzer_response = model.generate_content(analyzer_prompt)
    
    try:
        response_text = analyzer_response.text
        json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if json_match:
            json_string = json_match.group(0)
            analysis_result = json.loads(json_string)
            print(f"Analysis Result: {analysis_result}")
        else:
            print(f"Error: No JSON object found in the LLM's response. Raw response: {response_text}")
            return "Sorry, I had trouble understanding the format of your request."
    except json.JSONDecodeError:
        print(f"Error: Could not parse JSON from LLM. Raw response: {analyzer_response.text}")
        return "Sorry, I could not understand your request."

    # Step 2: Use tools based on the intent
    intent = analysis_result.get("intent")

    if intent == "planting_advice":
        location_from_ai = analysis_result.get("location", "thanjavur")

        # --- NEW MAPPING LOGIC TO FIX "city not found" ERROR ---
        # Map a general region to a specific city for the weather API
        if "kaveri delta" in location_from_ai.lower():
            api_location = "Thanjavur"
        else:
            # If it's not a known region, use it directly
            api_location = location_from_ai
        
        print(f"Calling weather tool for specific city: {api_location}...")
        weather_data = tools.get_weather(api_location)
        
        if not weather_data:
            return "Sorry, I could not retrieve the weather information at this time."

        crop_info = "Paddy (Nel) is suitable for the current Samba season."
        
        # Step 3: Synthesize the final answer
        print("Synthesizing final answer...")
        synthesizer_prompt = prompts.create_synthesizer_prompt(weather_data, crop_info)
        final_answer_response = model.generate_content(synthesizer_prompt)
        
        return final_answer_response.text
    else:
        return "I can currently only provide planting advice. Other features are coming soon!"


# --- Testing Block ---
if __name__ == "__main__":
    test_query = "காவிரி டெல்டாவில் இப்போது நெல் பயிரிடலாமா?"
    final_response = run_agent(test_query)
    print("\n--- Final Response ---")
    print(final_response)