import json
from haversine import haversine


def load_clients(filepath):
    try:
        with open(filepath, "r") as file:
            clients = json.load(file)
        return clients
    except FileNotFoundError:
        print("The file was not found")
        return []


def get_distance(client_location, office_location):
    return haversine(
        (client_location["latitude"], client_location["longitude"]),
        (office_location["latitude"], office_location["longitude"]),
    )


def normalize_data(clients, keys):
    stats = {}
    for key in keys:
        all_values = [client[key] for client in clients]

        min_val = min(all_values)
        max_val = max(all_values)
        range_val = max_val - min_val

        stats[key] = {"min": min_val, "max": max_val, "range": range_val}

        for client in clients:
            client[f"norm_{key}"] = (client[key] - min_val) / range_val

    return clients, stats


def top_clients_File(top_clients):
    try:
        filepath = "./taxpayers_Best.json"
        with open(filepath, "w") as file:
            json.dump(top_clients, file, indent=4)
        print(f"\n\n JSON file was successfully created and saved as {filepath}.")
    except IOError:
        print("An error occurred while writing the file.")


# Main function
if __name__ == "__main__":
    # The office location, can be changed
    office_location = {"latitude": 19.3797208, "longitude": -99.1940332}

    filepath = "./sample-data/taxpayers.json"
    clients = load_clients(filepath)

    for client in clients:
        client["distance"] = get_distance(client["location"], office_location)

    keys = ["age",
            "accepted_offers",
            "canceled_offers",
            "average_reply_time",
            "distance"]

    normalize_data( clients, keys)

    # Calculated score for each client
    for client in clients:
        score = (
            client.get("norm_age", 0) * 0.10
            + (1 - client.get("norm_distance", 0)) * 0.10
            + client.get("norm_accepted_offers", 0) * 0.30
            + (1 - client.get("norm_canceled_offers", 0)) * 0.30
            + (1 - client.get("norm_average_reply_time", 0)) * 0.20
        )

        client["score"] = int(score * 10)

        # Remove normalization keys from setlist
        client.pop("distance", None)
        for key in keys:
            client.pop(f"norm_{key}", None)

    top_clients = sorted(clients, key=lambda x: x["score"], reverse=True)[:10]
    print(top_clients)

    top_clients_File(top_clients)
