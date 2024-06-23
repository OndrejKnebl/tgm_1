# tgm_1_8.py
from influxdb import InfluxDBClient
from datetime import datetime
from dateutil import tz
import requests
import time
import pytz
import os

# Read parameters from environment variables
ttn_personal_API_key = os.getenv('TTN_PERSONAL_API_KEY')
ttn_url = os.getenv('TTN_URL')

db_url = os.getenv('DB_URL')
db_port = int(os.getenv('DB_PORT'))
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_measurement = os.getenv('DB_MEASUREMENT')

sleep_time = int(os.getenv('COLLECTION_INTERVAL'))

# Create the InfluxDB client object
db_client = InfluxDBClient(db_url, db_port, db_username, db_password, db_name)


def main():
    while True:
        session = requests.Session()
        header = {'Authorization': 'Bearer ' + ttn_personal_API_key}
        response = session.get(f"{ttn_url}/api/v3/gateways", headers=header)
        gateways_list = [gateway['ids']['gateway_id'] for gateway in response.json()['gateways']]

        int_parameters = ["uplink_count", "downlink_count"]
        time_parameters = ["last_uplink_received_at", "last_downlink_received_at", "last_status_received_at"]

        all_GWs = []

        my_main_time = int(datetime.now().timestamp() * 1000)

        for gateway in gateways_list:
            session = requests.Session()
            header = {'Authorization': 'Bearer ' + ttn_personal_API_key}
            response = session.get(f"{ttn_url}/api/v3/gs/gateways/{gateway}/connection/stats", headers=header)
            responseJSON = response.json()

            one_GW = {}
            one_GW["measurement"] = db_measurement
            one_GW["tags"] = {"host": str(gateway)}
            one_GW["time"] = my_main_time
            fields = {}


            for param in int_parameters:
                if responseJSON.get(param) != None:
                    fields[str(param)] = int(responseJSON.get(param))
                else:
                    fields[str(param)] = 0


            for param in time_parameters:
                if responseJSON.get(param) != None:
                    myTime = responseJSON.get(param)
                    myTime = myTime.split(".")
                    myTime = datetime.strptime(myTime[0],'%Y-%m-%dT%H:%M:%S')

                    # Convert timezone of datetime from UTC to local
                    myTime = myTime.replace(tzinfo=pytz.UTC)
                    local_zone = tz.tzlocal()
                    myTime = myTime.astimezone(local_zone).timestamp() * 1000

                    fields[str(param)] = int(myTime)
                else:
                    fields[str(param)] = 0
                    

            one_GW["fields"] = fields
            all_GWs.append(one_GW)

            print(one_GW)

        db_client.write_points(all_GWs, "ms")
        time.sleep(sleep_time)


if __name__ == "__main__":
    main()
