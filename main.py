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


# Main function
if __name__ == "__main__":
    # The office location, can be changed
    office_location = {"latitude": 19.3797208, "longitude": -99.1940332}

    filepath = "./sample-data/taxpayers.json"
    clients = load_clients(filepath)

    for client in clients:
        client["distance"] = get_distance(client["location"], office_location)

    normalize_data(
        clients,
        [
            "age",
            "accepted_offers",
            "canceled_offers",
            "average_reply_time",
            "distance",
        ],
    )

    # Calculated score of each client
    for client in clients:
        score = (
            client.get("norm_age", 0) * 0.10
            + (client.get("norm_distance", 0)) * 0.10
            + client.get("norm_accepted_offers", 0) * 0.30
            + (client.get("norm_canceled_offers", 0)) * 0.30
            + (client.get("norm_average_reply_time", 0)) * 0.20
        )

        client["score"] = score

    for client in clients:
        print(client)
