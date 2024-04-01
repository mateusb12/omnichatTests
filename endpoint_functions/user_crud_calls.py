import requests
import json

BASE_URL = "http://localhost:3000"
BASE_PREFIX = "users"

USERNAME = "test_user"
USER_EMAIL = "test_user@example.com"
USER_PASSWORD = "123456"


def create_user():
    url = f"{BASE_URL}/{BASE_PREFIX}/create"
    headers = {"Content-Type": "application/json"}
    data = {
        "username": USERNAME,
        "email": USER_EMAIL,
        "password": USER_PASSWORD
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response


def read_user():
    url = f"{BASE_URL}/{BASE_PREFIX}/read/1"
    response = requests.get(url)
    return response


def update_user():
    url = f"{BASE_URL}/{BASE_PREFIX}/update/1"
    headers = {"Content-Type": "application/json"}
    data = {
        "username": "new_user",
        "email": "changed_user@example.com",
        "password": "654321"
    }
    response = requests.put(url, headers=headers, data=json.dumps(data))
    return response


def delete_user():
    url = f"{BASE_URL}/{BASE_PREFIX}/delete/1"
    response = requests.delete(url)
    return response


def main():
    create_response = create_user()
    print(create_response.text)
    read_response = read_user()
    print(read_response.text)
    update_response = update_user()
    print(update_response.text)
    delete_response = delete_user()
    print(delete_response.text)
    return


if __name__ == "__main__":
    main()
