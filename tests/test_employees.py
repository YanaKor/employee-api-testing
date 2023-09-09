def test_fetch_single_employee(employees_endpoint):
    employees_endpoint.fetch_single_employee('1')


def test_all_employees(employees_endpoint):
    employees_endpoint.fetch_all_employees()


def test_create_employee(employees_endpoint):
    employees_endpoint.create_employee({
        "name": "Jack",
        "organization": "IT",
        "role": "Junior"
    })


def test_update_single_field(employees_endpoint):
    employees_endpoint.update_single_field('3', {'organization': 'Accounting'})


def test_update_entire_data(employees_endpoint):
    employees_endpoint.update_entire_data('4', {
        "name": "Ann",
        "organization": "Analytic",
        "role": "BA"
    })


def test_delete_employee(employees_endpoint):
    employees_endpoint.delete_employee('5')


def test_fetch_employee(employees_endpoint, get_id_created_employees, first_created_employee_data):
    employees_endpoint.fetch_employee(get_id_created_employees, first_created_employee_data)