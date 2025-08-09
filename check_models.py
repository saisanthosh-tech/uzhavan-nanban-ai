import google.generativeai as genai

# PASTE YOUR SAME GOOGLE AI STUDIO API KEY HERE
GOOGLE_API_KEY = "AIzaSyAOsk3oryXQWj0npdLRWHf4gR8TNgZ4zYw"

genai.configure(api_key=GOOGLE_API_KEY)

print("--- Available Generative Models ---")
for m in genai.list_models():
  # Check if 'generateContent' is a supported method for the model
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
print("---------------------------------")