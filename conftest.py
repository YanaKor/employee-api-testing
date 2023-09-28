import time

import pytest
import requests
from endpoints.employees import Employees
from env_setup import Credentials, Endpoints
from support.custom_errors import TokenNotFoundError, TokenNotGeneratedError
from database.db_connection import DataBaseConnection
import json


#*************************** data base fixtures ***************************
@pytest.fixture(scope='session', autouse=True)
def db_connection():
    connection = DataBaseConnection(
        dbname='employeesdb',
        user='postgres',
        password='superuser',
        host='localhost',
        port='5432'
    )
    yield connection
    connection.close()

@pytest.fixture(scope="session", autouse=True)
def create_employees(db_connection):
    created_users = []
    cur = db_connection.connection.cursor()
    cur.execute("SELECT MAX(employee_id) FROM employees")
    max_employee_id = cur.fetchone()[0]
    cur.close()

    user_data_list = [
        {"name": "Eddy", "organization": "IT", "role": "Lead Developer"},
        {"name": "Jack", "organization": "Finance", "role": "Accountant"},
        {"name": "Ariel", "organization": "Marketing", "role": "Marketing Specialist"}
    ]

    for user_data in user_data_list:
        max_employee_id = max_employee_id + 1 if max_employee_id is not None and max_employee_id != 0 else 1
        user_id = db_connection.fetchone(
            "INSERT INTO employees (employee_id, name, organization, role) VALUES (%s, %s, %s, %s) RETURNING employee_id",
            max_employee_id, user_data["name"], user_data["organization"], user_data["role"]
        )[0]

        user_info = {
            "employeeId": user_id,
            "name": user_data["name"],
            "organization": user_data["organization"],
            "role": user_data["role"]
        }
        created_users.append(user_info)

        db_connection.connection.commit()

    if created_users:
        with open("first_created_employee.json", "w") as json_file:
            json.dump(created_users[0], json_file)

    return created_users

@pytest.fixture(scope="session", autouse=True)
def delete_employees(db_connection, create_employees):
    yield
    time.sleep(15)
    for user in create_employees:
        user_id = user.get("employeeId")
        db_connection.execute("DELETE FROM employees WHERE employee_id = %s", user_id)

@pytest.fixture(scope="function")
def get_id_created_employees(create_employees):
    employee_id = next((user["employeeId"] for user in create_employees if user["name"] == "Eddy"), None)
    return employee_id

@pytest.fixture(scope="session")
def first_created_employee_data():
    with open("first_created_employee.json", "r") as json_file:
        data = json.load(json_file)
    return data
# *************************** app fixtures ***************************


@pytest.fixture()
def create_session():
    yield requests.Session()


@pytest.fixture(scope="session")
def credentials():
    return Credentials.get_env_variables()


@pytest.fixture(scope="session")
def bearer_token(credentials):
    response = requests.post(f"{Endpoints.TOKEN_URL}",
                             json={"username": credentials.APP_USERNAME, "password": credentials.APP_PASSWORD},
                             headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        token = response.json().get("token")
        if token is None:
            raise TokenNotFoundError
        yield token
    else:
        raise TokenNotGeneratedError(response.status_code)


@pytest.fixture()
def employees_endpoint(create_session, bearer_token):
    yield Employees(Endpoints.EMPLOYEES_URL, create_session, bearer_token)


