import json
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import csv


student_schema = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'id': {
                'type': 'integer'
            },
            'name': {
                'type': 'string'
            },
            'department_id': {
                'type': 'integer'
            }
        },
        'required': [
            'name',
            'department_id'
        ]
    }
}


department_schema = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'id': {
                'type': 'integer'
            },
            'name': {
                'type': 'string'
            }
        },
        'required': [
            'id',
            'name'
        ]
    }
}


class InvalidInstanceError(Exception):
    pass


class DepartmentName(Exception):
    pass


def validate_json(data, schema):
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError:
        return False


def user_with_department(csv_file, user_json, department_json):
    with open(csv_file, 'w') as result_file, open(user_json, 'r') as user_file, open(department_json, 'r') as department_file:
        user_data = json.load(user_file)
        department_data = json.load(department_file)

        if not validate_json(user_data, student_schema):
            raise InvalidInstanceError()

        if not validate_json(department_data, department_schema):
            raise InvalidInstanceError()

        for user in user_data:
            for department in department_data:
                if user['department_id'] == department['id']:
                    user['department_name'] = department['name']
                    break
            else:
                raise DepartmentName()

        header = ['name', 'department']
        result_user_data = [[user['name'], user['department_name']] for user in user_data]
        writer = csv.writer(result_file)
        writer.writerow(header)
        writer.writerows(result_user_data)
