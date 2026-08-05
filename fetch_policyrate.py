import os
import dotenv
import requests

# Initialize SBP API and .env file
dotenv.load_dotenv()
sbp_api_key = os.getenv("SBP_API_KEY")
base_url = "https://easydata.sbp.org.pk/api/v1/series/TS_GP_IR_SIRPR_AH.SBPOL0030/data"
api_url = f"{base_url}?api_key={sbp_api_key}"

# Function that GETs current SBP policy rate
def policy_rate(url):
    r = requests.get(url,timeout=10)
    sbp_json_data = r.json()
    policy_rate = sbp_json_data["rows"][0][4]
    return policy_rate

# print(policy_rate(api_url))