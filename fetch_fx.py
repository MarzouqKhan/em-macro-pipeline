import os
import dotenv
import requests
import db_manager
from email.utils import parsedate_to_datetime

# Initialize FX API and .env file
dotenv.load_dotenv()
fx_api_key = os.getenv("FX_API_KEY")
base_url = "https://v6.exchangerate-api.com/v6"
api_url = f"{base_url}/{fx_api_key}/latest"

# Function that GETs exchange rate
def exchange_rate(base,target,url,save=False):
    full_url = f"{url}/{base}"
    # GET conversion rate of base-to-target currency
    try:
        r = requests.get(full_url,timeout=10)
    except requests.exceptions.ConnectionError:
        print("Encountered ConnectionError, please ensure you are connected to the Internet.")
        return None
    fx_json_data = r.json()
    conversion_rate = fx_json_data["conversion_rates"][target]
    if save:
        api_time = fx_json_data["time_last_update_utc"]
        time = parsedate_to_datetime(api_time)
        db_manager.add_row(f"{base}-{target} Exchange Rate",conversion_rate,time.strftime("%Y-%m-%d"),source="ExchangeRate-API")
    return conversion_rate

print(exchange_rate("USD","PKR",api_url,True))