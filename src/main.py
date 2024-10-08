import re
import csv
import json
import time
import pandas as pd
import api_client
from distance import haversine_distance


def load_address_file(filename:str):
    """
    Load addresses from file, assuming 1 address per line.
    """
    with open(filename, "r") as file:
        lines = [re.split(r"\W-", line) for line in file]
    df = pd.DataFrame(lines, columns=["Name", "Address"])
    df["Name"] = df["Name"].map(lambda name: name.strip())
    df["Address"] = df["Address"].map(lambda address: address.strip())
    return df


def get_positions(query:str, api_key=None, **kwargs):
    """
    Query via the api client, incrementally removing query detail if no results are returned.
    """
    curr_query = query
    positions = api_client.geocode_positions(curr_query, api_key, **kwargs)
    while not positions:
        match = re.match(r"[^,]*,\s?(.*)", curr_query)
        if not match:
            break
        curr_query = match.group(1)
        positions = api_client.geocode_positions(curr_query, api_key, **kwargs)
    return positions


def main():
    # Load config
    with open("config.json", "r") as file:
        config = json.load(file)

    # Load Addresses
    df = load_address_file("data/adresses.txt")

    # For this sample problem DataFrame.map() does not work because the free api is QPS limited.
    positions = []
    for idx, row in df.iterrows():
        position = get_positions(row["Address"], config["api_key"])
        positions.append(position)
        time.sleep(0.5)
    pos_0 = [p[0] for p in positions]  # Keep only the most confident match.
    df["Position"] = pos_0

    # Find position of Adchieve HQ
    origin = df["Position"].loc[df["Name"] == "Adchieve HQ"].values[0]

    # Calculate distances
    df["distance_raw"] = df["Position"].map(lambda position: haversine_distance(origin , position))

    # Reformat & sort DataFrame for saving to .csv
    df["Distance"] = df["distance_raw"].map(lambda dist: f"{dist/1e3:.2f} km")
    df.sort_values(by=["distance_raw"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.index.names = ["Sortnumber"]

    # Save to .csv
    cols = ["Distance", "Name", "Address"]
    df[cols].loc[1:].to_csv("output/distances.csv", quoting=csv.QUOTE_NONNUMERIC)



if __name__ == "__main__":
    main()