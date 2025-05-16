import subprocess
import random
import json
# List of mobile numbers to test
mobile_numbers = [str(random.randint(1000000000, 9999999999)) for _ in
                  range(15)]
print(mobile_numbers)

# Base URL
url = "http://127.0.0.1:8001/login"


for mobile in mobile_numbers:
    # Prepare the curl command
    command = [
        "curl",
        "--location",
        "http://127.0.0.1:8001/login",
        "--header", f"X-User-Mobile: {mobile}",
        "--header", "Content-Type: application/json",
        "--data", json.dumps({"mobile": mobile})
    ]


    # Run the command and capture output
    result = subprocess.run(command, capture_output=True, text=True)

    # Print the response
    print(f"Response for {mobile}: {result.stdout}")
