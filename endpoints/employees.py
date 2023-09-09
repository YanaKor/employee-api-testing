import requests


class Employees:

    def __init__(self, url: str, session: requests.Session, token):
        self.session = session
        self.url = url
        self.token = token
        self.headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    def fetch_single_employee(self, employee_id):
        employee_url = f'{self.url}/{employee_id}'
        response = self.session.get(employee_url, headers=self.headers)

        assert response.status_code == 200, f'Actual status code: {response.status_code}'
        assert response.json() == {
            "employeeId": 1,
            "name": "Mary",
            "organization": "IT",
            "role": "QA"
        }, f'Actual: {response.json()}'

    def fetch_all_employees(self):
        response = self.session.get(self.url, headers=self.headers)
        assert response.status_code == 200, f'Actual status code: {response.status_code}'
        assert response.json() == [{'employeeId': 1, 'name': 'Mary', 'organization': 'IT', 'role': 'QA'},
                                   {'employeeId': 2, 'name': 'Max', 'organization': 'IT', 'role': 'Senior PM'},
                                   {'employeeId': 3, 'name': 'Nick', 'organization': 'Accounting', 'role': 'BA'},
                                   {'employeeId': 4, 'name': 'Ann', 'organization': 'Analytic', 'role': 'BA'}],\
            f'Actual: {response.json()}'

    def create_employee(self, data):
        response = self.session.post(self.url, headers=self.headers, json=data)
        assert response.status_code == 200, f'Actual status code: {response.status_code}'
        assert response.json() == {
            'employeeId': 5,
            "name": "Jack",
            "organization": "IT",
            "role": "Junior"
        }

    def update_single_field(self, employee_id, data):
        employee_url = f'{self.url}/{employee_id}'
        response = self.session.patch(employee_url, headers=self.headers, json=data)

        assert response.status_code == 200, f'Actual status code: {response.status_code}'
        assert response.json() == {'message': 'Employee updated'}

    def update_entire_data(self, employee_id, data):
        employee_url = f'{self.url}/{employee_id}'
        response = self.session.put(employee_url, headers=self.headers, json=data)

        assert response.status_code == 200, f'Actual status code: {response.status_code}'
        assert response.json() == {'message': 'Employee updated'}

    def delete_employee(self, employee_id):
        employee_url = f'{self.url}/{employee_id}'
        response = self.session.delete(employee_url, headers=self.headers)

        assert response.status_code == 200
        assert response.json() == {
            "message": "Employee deleted"
        }


    def fetch_employee(self, employee_id, employee_data):
        employee_url = f'{self.url}/{employee_id}'
        response = self.session.get(employee_url, headers=self.headers)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data == employee_data, f'Expected result: {employee_data}. Actual: {response_data}'