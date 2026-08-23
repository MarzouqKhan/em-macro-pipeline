from flask import Flask, render_template
from fetch_fx import exchange_rate, api_url
from fetch_sbp_data import SBPClient, sbp_api_key
from fetch_psx_data import psx_index_fetch

app = Flask(__name__)

@app.route('/') # https://flasky.com/index
def index():
    sbp_client = SBPClient(sbp_api_key)
    FX_rate = exchange_rate('USD', 'PKR', api_url)
    KSE100_data = psx_index_fetch('KSE100')
    policy_rate = sbp_client.policy_rate()
    net_reserves = sbp_client.net_sbp_reserves()
    return render_template('dashboard.html',FX_rate=FX_rate,KSE100_data=KSE100_data,policy_rate=policy_rate,net_reserves=net_reserves)