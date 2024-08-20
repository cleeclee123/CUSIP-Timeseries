import os
import json
import time
from datetime import datetime
from collections import defaultdict


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


t1 = time.time()

input_directory = r"C:\Users\chris\CUSIP-Set"
output_directory = r"C:\Users\chris\CUSIP-Timeseries"

cusip_timeseries = defaultdict(list)

keys_to_include = [
    "Date",
    "cusip",
    "bid_price"
    "offer_price"
    "mid_price"
    "eod_price"
    "bid_yield"
    "offer_yield"
    "eod_yield",
]

""" Entire Dir """

for file_name in os.listdir(input_directory):
    try:
        if file_name.endswith(".json"):
            file_path = os.path.join(input_directory, file_name)
            with open(file_path, "r") as json_file:
                daily_data = json.load(json_file)

            date_str = file_name.split(".json")[0]
            date = datetime.strptime(date_str, "%Y-%m-%d")

            for entry in daily_data["data"]:
                cusip = entry["cusip"]
                to_write = {
                    "Date": date_str,
                    "bid_price": entry["bid_price"],
                    "offer_price": entry["offer_price"],
                    "mid_price": entry["mid_price"],
                    "eod_price": entry["eod_price"],
                    "bid_yield": entry["bid_yield"],
                    "offer_yield": entry["offer_yield"],
                    "eod_yield": entry["eod_yield"],
                }
                cusip_timeseries[cusip].append(to_write)

        print(bcolors.OKBLUE + f"Saw {file_name}" + bcolors.ENDC)

    except Exception as e:
        print(bcolors.FAIL + f"FAILED {file_name} - {str(e)}" + bcolors.ENDC)

""" Single File """

# file_name = r"C:\Users\chris\CUSIP-Set\2024-08-19.json"
# try:
#     if file_name.endswith(".json"):
#         file_path = os.path.join(input_directory, file_name)
#         with open(file_path, "r") as json_file:
#             daily_data = json.load(json_file)

#         date_str = file_name.split(".json")[0]
#         date = datetime.strptime(date_str, "%Y-%m-%d")

#         for entry in daily_data["data"]:
#             cusip = entry["cusip"]
#             to_write = {
#                 "Date": date_str,
#                 "bid_price": entry["bid_price"],
#                 "offer_price": entry["offer_price"],
#                 "mid_price": entry["mid_price"],
#                 "eod_price": entry["eod_price"],
#                 "bid_yield": entry["bid_yield"],
#                 "offer_yield": entry["offer_yield"],
#                 "eod_yield": entry["eod_yield"],
#             }
#             cusip_timeseries[cusip].append(to_write)

#     print(bcolors.OKBLUE + f"Saw {file_name}" + bcolors.ENDC)

# except Exception as e:
#     print(bcolors.FAIL + f"FAILED {file_name} - {str(e)}" + bcolors.ENDC)

""""""

for cusip, timeseries in cusip_timeseries.items():
    try:
        output_file = os.path.join(output_directory, f"{cusip}.json")
        with open(output_file, "w") as json_file:
            json.dump(timeseries, json_file, indent=4, default=str)
        print(
            bcolors.OKGREEN
            + f"Wrote time series for CUSIP {cusip} to {output_file}"
            + bcolors.ENDC
        )
    except Exception as e:
        print(bcolors.FAIL + f"FAILED to Write {cusip} to {output_file}" + bcolors.ENDC)

print(f"Script took: {time.time() - t1} seconds")
