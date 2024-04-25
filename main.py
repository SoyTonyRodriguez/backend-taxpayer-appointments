import json

from haversine import haversine


# Main function
if __name__ == "__main__":
    # The office location, can be changed
    office_location = {"latitude": 19.3797208, "longitude": -99.1940332}

    distance = haversine(
        (20.28, -103.42),
        (office_location["latitude"], office_location["longitude"]),
    )

    print(distance)
