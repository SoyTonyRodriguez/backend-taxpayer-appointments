import json
from haversine import haversine


# Constants for weighting
AGE_WEIGHT = 0.10
DISTANCE_WEIGHT = 0.10
ACCEPTED_OFFERS_WEIGHT = 0.30
CANCELED_OFFERS_WEIGHT = 0.30
REPLY_TIME_WEIGHT = 0.20


# List that contains the keys used to normalize each data
NORMALIZATION_KEYS = [
    "age",
    "accepted_offers",
    "canceled_offers",
    "average_reply_time",
    "distance",
]


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
        # Verify if the 'key' exists in the list
        all_values = [client[key] for client in clients if key in client]

        min_val = min(all_values)
        max_val = max(all_values)
        range_val = max_val - min_val

        # Get the stats to normalize data from each client
        stats[key] = {"min": min_val, "max": max_val, "range": range_val}

        for client in clients:
            # Prevent division by 0
            if range_val > 0:
                # Add each normalized value to file
                client[f"norm_{key}"] = (client[key] - min_val) / range_val
            else:
                client[f"norm_{key}"] = 0

    return clients, stats


def compute_scores(clients, office_location):
    # For each client get the distance
    for client in clients:
        client["distance"] = get_distance(client["location"], office_location)

    # Store in clients the normalized values for each specified key
    clients, stats = normalize_data(clients, NORMALIZATION_KEYS)

    # For each client calculates a score based on normalized values, with weights:
    for client in clients:
        score = (
            client.get("norm_age", 0) * AGE_WEIGHT
            # 1 minus normalized value, because a shorter distance is preferable
            + (1 - client.get("norm_distance", 0)) * DISTANCE_WEIGHT
            + client.get("norm_accepted_offers", 0) * ACCEPTED_OFFERS_WEIGHT
            # 1 minus normalized value, because fewer cancellations are better.
            + (1 - client.get("norm_canceled_offers", 0)) * CANCELED_OFFERS_WEIGHT
            # 1 minus normalized value, because a quicker reply is better
            + (1 - client.get("norm_average_reply_time", 0)) * REPLY_TIME_WEIGHT
        )

        # Add the score to client data
        client["score"] = int(score * 10)

        # Remove normalization keys from setlist
        client.pop("distance", None)
        for key in NORMALIZATION_KEYS:
            client.pop(f"norm_{key}", None)

    # return the 10 best clients
    return sorted(clients, key=lambda x: x["score"], reverse=True)[:10]


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

    top_clients = compute_scores(clients, office_location)
    print(top_clients)

    top_clients_File(top_clients)
