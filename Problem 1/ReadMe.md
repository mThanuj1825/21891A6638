# _Simple API for Number fetching_

### Overview

This is an API designed for fetching and processing numerical responses. This server provides dynamic interface to retrieve and manage sequences of numbers based on predefined categories. The server utilizes bearer tokens for authentication.

### Features

- Token-Based Authentication: Securely obtain and use tokens to access API endpoints
- Dynamic Data Fetching: Retrieve numerical data in real-time from the server
- Efficient Data Handling: Maintain a sliding window of recent numbers to avoid duplication and optimize processing
- Performance Monitoring: Check and log response times to ensure service quality

### Endpoints

`/numbers/<number_id>`

### Method: `GET`

#### Description: Retrieves a list of numbers based on the specified category identifier

### Parameters:

- `number_id` (string): The category for the numbers. Possible values are:
  - `p`: primes
  - `f`: fibonacci
  - `e`: even
  - `r`: random

### Responses:

- 200 OK: Returns a JSOn object like this:
  {
  "windowPrevState": [array of previous window numbers],
  "windowCurrState": [array of current window numbers],
  "numbers": [array of numbers fetched from the API],
  "avg": [average of current window numbers]
  }
- 400 Bad Request: If the `number_id` is invalid
- 500 Internal Server Error: If the's a failure to fetch data or if the response time exceeds 500ms

### Authentication

This API uses bearer tokens for authentication. A valid token is required to access the endpoints. The server automatically manages token retrieval and caching to enhance performance.

### Token Retrieval

Tokens are fetched from a dedicated authentication service. If a token is not available or expired, a new token is requested. The token is cached for one hour to reduce the frequency of authentication requests.

### Error Handling

Errors are logged with detailed messages to help diagnose issues. Ensure to check the logs for any anomalies or errors encountered.

### Running the Server

To run the API server locally, use the following command:
`python app.py`

## Dependencies

- Flask: For building the web server.
- Requests: For making HTTP requests.
- Collections: For managing data with a sliding window.
- JSON: For handling JSON data.
- Logging: For error and debug logging.
