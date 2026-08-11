import os
import dotenv
import requests
import db_manager

# Initialize SBP API and .env file
dotenv.load_dotenv()
sbp_api_key = os.getenv("SBP_API_KEY")

# Function that GETs requested series from SBP EasyData using series key
def series_data(series, api_key, save=False):
    full_url = f"https://easydata.sbp.org.pk/api/v1/series/{series}/data?api_key={api_key}"
    r = requests.get(full_url,timeout=10)
    sbp_json_data = r.json()
    data = sbp_json_data["rows"][0][4]
    if save:
        data_name, stat_date, source, series_key = sbp_json_data["rows"][0][2], sbp_json_data["rows"][0][3], "SBP", sbp_json_data["rows"][0][1]
        db_manager.add_row(data_name,data,stat_date,source,series_key)
    return data

# Function that GETs current SBP policy rate
def policy_rate(api_key, save=False):
    return series_data("TS_GP_IR_SIRPR_AH.SBPOL0030", api_key, save)

# Function that GETs net SBP reserves (in millions of $USD)
def net_sbp_reserves(api_key, save=False):
    return series_data("TS_GP_EXT_PAKRES_M.Z00030",api_key, save)

if __name__ == "__main__":
    print(series_data("TS_GP_IR_SIRPR_AH.SBPOL0030",sbp_api_key, True))
    print(policy_rate(sbp_api_key, True))
    print(net_sbp_reserves(sbp_api_key, True))