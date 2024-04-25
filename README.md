# KEA Technical Interview

This Python script calculates a score for clients based on their geographic distance from an office and their behavioral data
such as age, offer acceptance, cancellations, and reply times. The scores help in identifying the top clients likely to accept 
appointment offers.

## Features

- Load client data from a JSON file.
- Calculate the great-circle distance between two geographic points using the haversine formula.
- Normalize data points to ensure fair scoring.
- Compute a composite score for each client using weighted criteria.
- Output the top 10 clients based on their scores into a new JSON file.

## Requirements

- Python 3.x
- `haversine` library: Used for calculating distances. Install via pip:

  ```shell
  pip install haversine
  ```

- If you wish you can use the `requirements.txt` file to install all depencies, if any are not installed
  ```shell
  pip install -r requirements.txt
  ```

## Usage

### Set-up

Ensure Python is installed on your system along with the `haversine` library, that was the unique third-party library used.

### Data Preparation 

Prepare a JSON file containing client data. **Ensure the file is in the next path `./sample-data/taxpayers.json`** 
You can change the pathfile if you want, located in the main function
```python
    # Load the clients from a JSON file
    # Change the path if is necessary
    filepath = "./sample-data/taxpayers.json"
```

### Running the Script

Execute the script.
```shell
python main.py
```

You can modify the office_location in the Script, if you want, located in the main function
```python
    # The office location, can be changed
    office_location = {"latitude": 19.3797208, "longitude": -99.1940332}
```
### Check Results

The top 10 clients will be saved in `taxpayers_Best.json` file in the same directory.

## Assumptions

In the `compute_scores` function, I subtracted normalized values from 1 for certain metrics due to their convenience in the
context of scoring.

```python 
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
```

#### Distance (norm_distance)

In the scoring system, a shorter distance is more favorable as it indicates proximity to the office, which is assumed to
correlate with a higher likelihood of the client accepting an appointment.

#### Canceled Offers (norm_canceled_offers)

Fewer cancellations suggest a reliable client, which is a desirable trait.
That means to convert fewer cancellations into a higher score, aligning with the goal of identifying dependable clients.

#### Average Reply Time (norm_average_reply_time)

Quick reply times are generally preferred as they indicate the client's promptness and potential readiness to engage
That means a quicker reply results in a higher score, thereby promoting clients who are more responsive.
