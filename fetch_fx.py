import os
import dotenv
import requests

# Intialize FX API
dotenv.load_dotenv()
fx_api_key = os.getenv("FX_API_KEY")
base_url = "https://v6.exchangerate-api.com/v6"
api_url = f"{base_url}/{fx_api_key}/latest"

# Function that GETs exchange rate
def exchange_rate(base,target,url):
    full_url = f"{url}/{base}"
    # GET conversion rate of base-to-target currency
    try:
        r = requests.get(full_url,timeout=10)
    except requests.exceptions.ConnectionError:
        print("Encountered ConnectionError, please ensure you are connected to the Internet.")
        return None
    fx_json_data = r.json()
    conversion_rate = fx_json_data["conversion_rates"][target]
    return conversion_rate

print(exchange_rate("USD","PKR",api_url))