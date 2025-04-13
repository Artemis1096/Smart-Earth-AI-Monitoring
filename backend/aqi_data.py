import os
import requests
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from dotenv import load_dotenv

# Load environment variables from .env file (if you're using one)
load_dotenv()

# Set API keys (you can replace or set these in a .env file)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")  # Replace with actual key if not using .env
WAQI_TOKEN = os.getenv("WAQI_TOKEN", "526e8f81879e0f2c4a9ed5c8956710d106a8ddb2")

os.environ["GROQ_API_KEY"] = GROQ_API_KEY  # Required for langchain_groq

def get_aqi_waqi(lat, lon, token=WAQI_TOKEN):
    """Fetch AQI data from WAQI API."""
    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={token}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'ok':
            aqi = data['data']['aqi']
            city = data['data']['city']['name']
            return city, aqi
        else:
            raise ValueError(f"API Error: {data.get('data')}")
    else:
        raise ConnectionError(f"Failed to fetch data. HTTP Status: {response.status_code}")

def ask_llm_about_aqi(city, aqi):
    """Use LLM to generate accurate AQI insights using structured prompt engineering."""
    # System role: define what the assistant does
    system_message = SystemMessagePromptTemplate.from_template(
        """
        You are an environmental analyst AI. Your job is to analyze AQI (Air Quality Index) data of a region and respond with exactly 3 sections:
        1. AQI Classification: Use standard categories like Good, Moderate, Unhealthy, Very Unhealthy, Hazardous.
        2. Improvement Suggestions: Suggest practical actions citizens and local authorities can take to improve air quality.
        3. Cause Analysis: ONLY if AQI is worse than 'Good', explain likely causes specific to that region (like traffic, industries, etc). If AQI is 'Good', return "Always keep your environment clean".
        Always keep responses concise, helpful, and factual.
        """
    )
    # Human message: dynamic input
    human_message = HumanMessagePromptTemplate.from_template(
        "The AQI of {city} is {aqi}. Provide your analysis as per instructions."
    )
    #Combine prompt parts
    prompt_template = ChatPromptTemplate.from_messages([system_message, human_message])
    # LLM selection (Groq)
    chat = ChatGroq(temperature=0.5, model="llama3-70b-8192")
    # Fill in prompt
    prompt = prompt_template.format_messages(city=city, aqi=aqi)
    # Get LLM response
    response = chat.invoke(prompt)
    return response.content

def get_aqi_insight(lat, lon):
    """Main handler to get AQI insights from lat/lon."""
    try:
        city, aqi = get_aqi_waqi(lat, lon)
        print(f"\n📍 Location: {city}")
        print(f"🌫️ AQI: {aqi}")
        insight = ask_llm_about_aqi(city, aqi)
        print("\n🤖 LLM Insight:\n")
        print(insight)
        return {
            "city": city,
            "aqi": aqi,
            "insight": insight
        }
    except Exception as e:
        return {
            "error": str(e)
        }

# Optional: Test it locally
if __name__ == "__main__":
    lat = input("Enter latitude: ")
    lon = input("Enter longitude: ")
    try:
        lat = float(lat)
        lon = float(lon)
        result = get_aqi_insight(lat, lon)
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
    except ValueError:
        print("❌ Please enter valid numbers for latitude and longitude.")
