import requests
import os # Good for managing API keys

# It's better practice to get the key from environment variables,
# but for the hackathon, you can start with it directly.
API_KEY = "paste_your_api_key_here" 

def get_weather(location_name):
    """
    Fetches 5-day weather forecast for a given location.
    """
    # URL from the weather API documentation
    api_url = f"https://api.openweathermap.org/data/2.5/forecast?q={location_name}&appid={API_KEY}&units=metric"
    
    # Make the request
    response = requests.get(api_url)
    
    # Get the JSON data
    data = response.json()
    
    # For now, just print the data to see if it works
    print(data)
    
    # We will process this data later
    return data

# --- You can test your function directly in this file ---
if __name__ == "__main__":
    # This block runs only when you execute this file directly
    print("Testing the weather tool...")
    get_weather("Thanjavur")