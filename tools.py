import requests

# Paste your NEW, SECRET key here. Do not share this key.
API_KEY = "2c7975976c1e1319f9ab958e93074ad4"

def get_weather(location_name):
    """
    Fetches and processes the 5-day weather forecast for a given location.
    """
    # API URL from the OpenWeatherMap documentation
    api_url = f"https://api.openweathermap.org/data/2.5/forecast?q={location_name}&appid={API_KEY}&units=metric"
    
    response = requests.get(api_url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        
        # Create an empty list to store our clean data
        clean_forecasts = []
        
        # Loop through the list of forecasts from the API response
        for forecast_item in data['list']:
            # Create a simple dictionary with only the data we need
            clean_item = {
                "time": forecast_item['dt_txt'],
                "temp": forecast_item['main']['temp'],
                "feels_like": forecast_item['main']['feels_like'],
                "description": forecast_item['weather'][0]['description']
            }
            # Add the clean dictionary to our list
            clean_forecasts.append(clean_item)
            
        # Return the final list of clean forecasts
        return clean_forecasts
    else:
        # If there was an error, print the error and return None
        print(f"Error: {response.status_code}, {response.text}")
        return None

# --- This block is for testing the function directly ---
if __name__ == "__main__":
    print("Testing the weather tool...")
    
    # We are testing with "Thanjavur"
    thanjavur_weather = get_weather("Thanjavur")
    
    if thanjavur_weather:
        # Print the first 5 forecast items to confirm it's working
        for forecast in thanjavur_weather[:5]:
            print(forecast)