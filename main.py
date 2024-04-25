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


# Main function
if __name__ == "__main__":
    # The office location, can be changed
    office_location = {"latitude": 19.3797208, "longitude": -99.1940332}

    filepath = "./sample-data/taxpayers.json"
    clients = load_clients(filepath)

    for client in clients:
        client_location = client["location"]
        distance = haversine(
            (client_location["latitude"], client_location["longitude"]),
            (office_location["latitude"], office_location["longitude"]),
        )
        print(distance)

    # print(distance)
