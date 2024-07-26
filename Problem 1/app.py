from flask import Flask, jsonify
import requests
from collections import deque
from time import time
import logging
import json

app = Flask(__name__)

MAX_WINDOW_SIZE = 10
TIME_OUT = 0.5
window = deque(maxlen=MAX_WINDOW_SIZE)


logging.basicConfig(level=logging.DEBUG)

NUMBER_ID_MAP = {
    'p': 'primes',
    'f': 'fibo',
    'e': 'even',
    'r': 'rand'
}


def get_bearer_token():
    try:
        headers = {'Content-Type': 'application/json'}
        data = {
            "companyName": "Vignan Institute Of Technology and Science",
            "clientID": "bcfbc137-2bbd-412d-83b3-cf354c3465c0",
            "clientSecret": "BkcJuPjYIsBhkojV",
            "ownerName": "M Thanuj",
            "ownerEmail": "mullagurithanuj0@gmail.com",
            "rollNo": "21891A6638"
        }
        logging.debug(f"Requesting token with data: {data}")
        response = requests.post("http://20.244.56.144/test/auth",
                                 headers=headers, data=json.dumps(data), timeout=TIME_OUT)
        logging.info(response)
        if response.status_code == 201:
            token_data = response.json()
            return token_data.get('access_token')
        else:
            logging.error(
                f"Failed to get token: {response.status_code} {response.text}")
            return None
    except requests.RequestException as e:
        logging.error(f"RequestException while getting token: {e}")
        return None


def fetch_numbers_from_api(number_id):
    api_url = f"http://20.244.56.144/test/{NUMBER_ID_MAP[number_id]}"
    bearer_token = get_bearer_token()
    if not bearer_token:
        logging.error("Bearer token not available")
        return []
    headers = {
        'Authorization': f'Bearer {bearer_token}'
    }
    try:
        logging.debug(f"Fetching numbers from {api_url}")
        response = requests.get(api_url, headers=headers, timeout=TIME_OUT)
        if response.status_code == 200:
            data = response.json()
            logging.debug(f"Received data: {data}")
            return data.get('numbers', []) if isinstance(data.get('numbers'), list) else []
        else:
            logging.error(
                f"Failed to fetch numbers: {response.status_code} {response.text}")
            return []
    except requests.RequestException as e:
        logging.error(f"RequestException while fetching numbers: {e}")
        return []


@app.route('/numbers/<number_id>', methods=['GET'])
def get_numbers(number_id):
    start_time = time()
    logging.debug(f"Received request for number ID: {number_id}")

    if number_id not in NUMBER_ID_MAP:
        logging.error(f"Invalid number ID: {number_id}")
        return jsonify({"error": "Invalid number ID"}), 400

    numbers_from_api = fetch_numbers_from_api(number_id)
    if not numbers_from_api:
        logging.error("Failed to fetch numbers from the third-party server")
        return jsonify({"error": "Failed to fetch numbers from the third-party server"}), 500

    unique_numbers = set(window)
    prev_state = list(window)

    for number in numbers_from_api:
        if number not in unique_numbers:
            if len(window) >= MAX_WINDOW_SIZE:
                window.popleft()
            window.append(number)
            unique_numbers.add(number)

    curr_state = list(window)
    avg = sum(window) / len(window) if window else 0.0

    response_time = time() - start_time
    if response_time > TIME_OUT:
        logging.error("Response time exceeded 500ms")
        return jsonify({"error": "Response time exceeded 500ms"}), 500
    
    logging.info(window)

    return jsonify({
        "windowPrevState": prev_state,
        "windowCurrState": curr_state,
        "numbers": numbers_from_api,
        "avg": round(avg, 2)
    })


if __name__ == '__main__':
    app.run(debug=True)
