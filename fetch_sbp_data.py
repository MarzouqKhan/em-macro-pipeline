import os
import dotenv
import requests

# Initialize SBP API and .env file
dotenv.load_dotenv()
sbp_api_key = os.getenv("SBP_API_KEY")

# Function that GETs requested series from SBP EasyData using series key
def series_data(series, api_key):
    full_url = f"https://easydata.sbp.org.pk/api/v1/series/{series}/data?api_key={api_key}"
    r = requests.get(full_url,timeout=10)
    sbp_json_data = r.json()
    series_data = sbp_json_data["rows"][0][4]
    return series_data

# Function that GETs current SBP policy rate
def policy_rate(api_key):
    return series_data("TS_GP_IR_SIRPR_AH.SBPOL0030", api_key)
                       
# print(series_data("TS_GP_IR_SIRPR_AH.SBPOL0030",sbp_api_key))
# print(policy_rate(sbp_api_key))