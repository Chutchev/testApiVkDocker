import json

import pytest
import requests
from jsonschema import validate
import re
from Model.User import users_json_scheme, user_json_scheme

BASE_URL = "http://localhost:5000/api/contacts"


# class TestPositive:
#     def setup_class(self):
#         print("Начинаем позитивные тесты")
#
#     def teardown_class(self):
#         print("Заканчиваем позитивные тесты")
#
#     def test_all_get_api_contacts(self):
#         response = requests.get(BASE_URL)
#         if response.status_code == 200:
#             answer = response.json()
#             validate(answer, users_json_scheme)
#
#     def test_post_positive_required_fields(self):
#         body = {
#             "first_name": "testuser2",
#             "email": "test_user_2@mail.ru"
#         }
#         response = requests.post(BASE_URL, json=body)
#         if response.status_code == 200:
#             answer = response.json()
#             msg = answer["SUCCESS"]
#             msg_pattern = r"User: User id: <\d+> is created"
#             assert re.match(msg_pattern, msg)
#
#     def test_post_all_fields_positive(self):
#         body = {
#             "first_name": "testuser4",
#             "email": "test_user_4@mail.ru",
#             "phone": "+79234567890",
#             "last_name": "test_last_name",
#             "city": "Yekaterinburg",
#             "country": "Russia",
#             "address": "Pushkina 187",
#         }
#         response = requests.post(BASE_URL, json=body)
#         if response.status_code == 200:
#             answer = response.json()
#             msg = answer["SUCCESS"]
#             msg_pattern = r"User: User id: <\d+> is created"
#             assert re.match(msg_pattern, msg)
#
#     def test_get_one_contact_positive(self):
#         response = requests.get(f"{BASE_URL}/1")
#         if response.status_code == 200:
#             answer = response.json()
#             validate(answer, user_json_scheme)
#
#     def test_put_positive(self):
#         body = {
#             "first_name": "Ivan",
#             "email": "ivan@mail.ru",
#             "city": "Moscow",
#             "country": "Russia",
#             "address": "Pushkina 187",
#         }
#         response = requests.put(f"{BASE_URL}/1", json=body)
#         if response.status_code == 200:
#             answer = response.json()
#             msg = answer["MESSAGE"]
#             msg_pattern = r"User with id: \d+ is changed"
#             assert re.match(msg_pattern, msg)
#
#     def test_delete_positive(self):
#         response = requests.delete(f"{BASE_URL}/3")
#         if response.status_code == 200:
#             answer = response.json()
#             msg = answer["MESSAGE"]
#             msg_pattern = r"User with id: \d+ is deleted"
#             assert re.match(msg_pattern, msg)


class TestNegative:

    def setup_class(self):
        print("Начинаем негативные тесты")

    def teardown_class(self):
        print("Заканчиваем негативные тесты")

    @pytest.mark.parametrize("field", [("email", "test_user_2@mail.ru", "first_name"), ("first_name", "Ivan", "email")])
    def test_post_without_required_fields(self, field):
        body = {
            field[0]: field[1]
        }
        response = requests.post(BASE_URL, json=body)
        if response.status_code == 404:
            answer = response.json()
            msg = answer["ERROR"]
            assert f"'{field[2]}' is a required property" in msg

    @pytest.mark.parametrize("phone", ["8912", "", "-79991234567", "+791227S1234"])
    def test_validation_phone(self, phone):
        body = {
            "phone": phone
        }
        response = requests.put(f"{BASE_URL}/1", json=body)
        if response.status_code == 404:
            answer = response.json()
            msg = answer["ERROR"]
            assert f"'{phone}' does not match" in msg

    @pytest.mark.parametrize("first_name", [None, "", 123, "123", "fdhsjgfdsg,jklkdjfhsbgsjdklfhgbjhklsdfgjhksdfgjho;sdfgjklhfsdglhjkdfsgjhklsdfgjhkdfslgjhkldfgssjldhkfgd"])
    def test_validation_first_name(self, first_name):
        body = { "first_name": first_name }
        response = requests.put(f"{BASE_URL}/1", json=body)
        if response.status_code == 404:
            answer = response.json()
            msg = answer["ERROR"]
            assert f"{first_name} does not match" in msg or f"{first_name} is not of type" in msg

    @pytest.mark.parametrize("email", [None, "", "123@sdfdag.sdfg", "1@fgdh.sfgd", "@.fgds", "@.@.@"])
    def test_validation_email(self, email):
        body = {
            "email": email
        }
        response = requests.put(f"{BASE_URL}/1", json=body)
        if response.status_code == 404:
            answer = response.json()
            msg = answer["ERROR"]
            assert f"'{email}' does not match" in msg or f"{email} is not of type" in msg

    @pytest.mark.parametrize("user_id", [None, "-1", "0", "5641456564", "@", 23, " "])
    def test_is_not_exists_put(self, user_id):
        body = {
            "city": "Ufa"
        }
        response = requests.put(f"{BASE_URL}/{user_id}", json=body)
        if response.status_code == 404:
            answer = response.json()
            msg = answer["MESSAGE"]
            msg_pattern = r"User with id: \d+ is not exists"
            assert re.match(msg_pattern, msg)
