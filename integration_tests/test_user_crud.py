import pytest
import requests

# Assuming your Flask app is running on http://localhost:3000
from endpoint_functions.user_crud_calls import create_user, read_user, update_user, delete_user


class TestUserCRUDIntegration:
    base_url = "http://localhost:3000"
    base_prefix = "users"

    def test_create_user(self):
        response = create_user()
        assert response.status_code == 201
        assert response.json() == {"data": {"email": "test_user@example.com", "id": 1, "username": "test_user"},
                                   "message": "User created!"}

    def test_read_user(self):
        response = read_user()
        assert response.status_code == 200
        assert response.json() == {"data": {"email": "test_user@example.com", "id": 1, "username": "test_user"}}

    def test_update_user(self):
        response = update_user()
        assert response.status_code == 200
        assert response.json() == {"data": {"email": "changed_user@example.com", "id": 1, "username": "new_user"},
                                   "message": "User updated!"}

    def test_delete_user(self):
        response = delete_user()
        assert response.status_code == 200
        assert response.json() == {"message": "User deleted!"}
