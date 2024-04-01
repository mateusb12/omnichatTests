import pytest
import requests_mock as mock

from endpoint_functions.user_crud_calls import create_user, read_user, update_user, delete_user


@pytest.mark.usefixtures("requests_mock")
class TestUserCRUD:
    def test_create_user(self, requests_mock):
        requests_mock.post("http://localhost:3000/users/create",
                           json={"data": {"email": "test_user@example.com", "id": 1, "username": "test_user"},
                                 "message": "User created!"})
        response = create_user()
        assert response.json() == {"data": {"email": "test_user@example.com", "id": 1, "username": "test_user"},
                                   "message": "User created!"}

    def test_read_user(self, requests_mock):
        requests_mock.get("http://localhost:3000/users/read/1",
                          json={"data": {"email": "test_user@example.com", "id": 1, "username": "test_user"}})
        response = read_user()
        assert response.json() == {"data": {"email": "test_user@example.com", "id": 1, "username": "test_user"}}

    def test_update_user(self, requests_mock):
        requests_mock.put("http://localhost:3000/users/update/1",
                          json={"data": {"email": "changed_user@example.com", "id": 1, "username": "new_user"},
                                "message": "User updated!"})
        response = update_user()
        assert response.json() == {"data": {"email": "changed_user@example.com", "id": 1, "username": "new_user"},
                                   "message": "User updated!"}

    def test_delete_user(self, requests_mock):
        requests_mock.delete("http://localhost:3000/users/delete/1", json={"message": "User deleted!"})
        response = delete_user()
        assert response.json() == {"message": "User deleted!"}


if __name__ == "__main__":
    pytest.main()
