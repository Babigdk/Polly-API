import requests

BASE_URL = "http://localhost:8000"

def register_user(username, password):
    """
    Registers a new user with the Polly-API.

    Args:
        username (str): The username to register.
        password (str): The password for the user.

    Returns:
        dict: The JSON response from the server if successful, otherwise None.
    """
    url = f"{BASE_URL}/register"
    user_data = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(url, json=user_data)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
        print(f"Response body: {errh.response.text}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else: {err}")
    return None

def login(username, password):
    """
    Logs in a user and returns the access token.

    Args:
        username (str): The username to login with.
        password (str): The password for the user.

    Returns:
        str: The access token if successful, otherwise None.
    """
    url = f"{BASE_URL}/login"
    data = {
        "username": username,
        "password": password
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json().get("access_token")
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
        print(f"Response body: {errh.response.text}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else: {err}")
    return None

def vote_on_poll(poll_id, option_id, token):
    """
    Casts a vote on a poll.

    Args:
        poll_id (int): The ID of the poll to vote on.
        option_id (int): The ID of the option to vote for.
        token (str): The JWT token for authentication.

    Returns:
        dict: The JSON response from the server if successful, otherwise None.
    """
    url = f"{BASE_URL}/polls/{poll_id}/vote"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"option_id": option_id}
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
        print(f"Response body: {errh.response.text}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else: {err}")
    return None

def get_poll_results(poll_id):
    """
    Retrieves the results of a poll.

    Args:
        poll_id (int): The ID of the poll to get results for.

    Returns:
        dict: The JSON response from the server if successful, otherwise None.
    """
    url = f"{BASE_URL}/polls/{poll_id}/results"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
        print(f"Response body: {errh.response.text}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else: {err}")
    return None

if __name__ == "__main__":
    # Example usage:
    new_username = "testuser"
    new_password = "testpassword"
    
    print(f"Attempting to register user: {new_username}")
    registered_user = register_user(new_username, new_password)
    
    if registered_user:
        print("User registered successfully!")
        print(f"User details: {registered_user}")
    else:
        print("User registration failed.")

    print("\nAttempting to login...")
    token = login(new_username, new_password)

    if token:
        print("Login successful!")
        # Assuming a poll with ID 1 and option with ID 1 exists
        poll_id_to_vote = 1
        option_id_to_vote = 1
        
        print(f"\nAttempting to vote on poll {poll_id_to_vote} with option {option_id_to_vote}...")
        vote_result = vote_on_poll(poll_id_to_vote, option_id_to_vote, token)

        if vote_result:
            print("Vote cast successfully!")
            print(f"Vote details: {vote_result}")
        else:
            print("Failed to cast vote.")

        print(f"\nAttempting to get results for poll {poll_id_to_vote}...")
        poll_results = get_poll_results(poll_id_to_vote)

        if poll_results:
            print("Poll results retrieved successfully!")
            print(f"Results: {poll_results}")
        else:
            print("Failed to retrieve poll results.")
    else:
        print("Login failed.")
