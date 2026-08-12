import os
import dotenv
import requests
import db_manager

# Initialize .env file and API keys
dotenv.load_dotenv()
sbp_api_key = os.getenv("SBP_API_KEY")

# Client class for accessing SBP API
class SBPClient:

    # Initialize class with API key and default save behavior
    def __init__ (self, api_key, save=False):
        self.api_key = api_key
        self.save = save
    
    # Function that GETs requested series from SBP EasyData using series key
    def series_data(self, series, save=None):
        should_save = self.save if save is None else save # Manage save logic based off passed value for save (if any)
        full_url = f"https://easydata.sbp.org.pk/api/v1/series/{series}/data?api_key={self.api_key}"
        try:
            r = requests.get(full_url,timeout=10)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None
        except requests.ConnectionError as e:
            print(f"Encountered {e}, please ensure you are connected to the Internet.")
        sbp_json_data = r.json()
        data = sbp_json_data["rows"][0][4]
        if should_save:
            data_name, stat_date, source, series_key = sbp_json_data["rows"][0][2], sbp_json_data["rows"][0][3], "SBP", sbp_json_data["rows"][0][1]
            print("Saving data...")
            db_manager.add_row(data_name,data,stat_date,source,series_key)
        return data

    # Function that GETs current SBP policy rate
    def policy_rate(self, save=None):
        return self.series_data("TS_GP_IR_SIRPR_AH.SBPOL0030", save)

    # Function that GETs net SBP reserves (in millions of $USD)
    def net_sbp_reserves(self, save=None):
        return self.series_data("TS_GP_EXT_PAKRES_M.Z00030", save)

if __name__ == "__main__":
    client = SBPClient(sbp_api_key,True) # Intializes client with saving on by default
    print(client.series_data("TS_GP_IR_SIRPR_AH.SBPOL0030"))
    print(client.policy_rate())
    print(client.net_sbp_reserves())