import requests

def get_waqi_data(city, api_key):
    # Base URL for WAQI API
    url = f"http://api.waqi.info/feed/{city}/?token={api_key}"

    # Send request to the API
    response = requests.get(url)
    
    # Check for successful response
    if response.status_code == 200:
        data = response.json()
        
        if data["status"] == "ok":
            # AQI info
            aqi = data["data"]["aqi"]
            city_name = data["data"]["city"]["name"]
            time = data["data"]["time"]["s"]
            
            print(f"City: {city_name}")
            print(f"Time: {time}")
            print(f"AQI: {aqi}")
        else:
            print(f"Error: {data['data']}")
    else:
        print(f"Failed to fetch data: {response.status_code}")

# Example usage
api_key = "8dfcd39357bbc0c959488da5dd146b991279ec80"  # Replace with your WAQI API key
city = "beijing"  # Example: you can change this to the city you want

get_waqi_data(city, api_key)
