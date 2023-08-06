import pathlib
import time

import requests
from os                                         import path

from .core.employee                              import Employee
from .core.mail                                  import SendWishEmail
from .core.process                               import ProcessEmployee
from .db.data                                    import JSONData
from .operation                                  import Operation as ops


class GetInput:
    current_date = ops.get_today_date()

    def __init__(self, selection, **kwargs):
        self.selection   = selection
        self.crontab     = kwargs.get('crontab')
        self.emp_list    = []
        self.emp_na_list = []
    
    def compare_api_and_local_data(self):
        for employee in self.employees_local:
            if self.worker['id'] == employee['id']:
                str_date = ''
                lastNotification     = employee.get('lastNotification')
                lastBirthdayNotified = employee.get('lastBirthdayNotified')
                if lastNotification:
                    str_date = lastNotification
                elif lastBirthdayNotified:
                    str_date = lastBirthdayNotified

                if str_date:
                    last_date = ops.str_to_date(str_date)
                    if self.current_date.month == last_date.month and self.current_date.day == last_date.day:
                        return True
        return False

    def call_real_endpoint(self):

        employees     = []
        exc_employees = []
        emp_resp      = requests.get('https://interview-assessment-1.realmdigital.co.za/employees')
        exc_emp_resp  = requests.get('https://interview-assessment-1.realmdigital.co.za/do-not-send-birthday-wishes')

        if emp_resp.status_code == 200:
            employees = emp_resp.json()
        if exc_emp_resp.status_code == 200:
            exc_employees = exc_emp_resp.json()

        data = {
            'employees'     : employees,
            'exc_employees' : exc_employees
        }

        return data

    def get_input_redirect(self):

        birthday_names       = []
        anniversary_names    = []
        self.employees_local = []

        data_api      = self.call_real_endpoint()
        employees_api = data_api['employees']
        employees     = employees_api

        current_dir = pathlib.Path(__file__).parent
        json_file   = f'{current_dir}/db/employeesZ.json'

        if path.isfile(json_file):
            data_local           = JSONData(None, None, None)
            self.employees_local = data_local.extract_employee_data(json_file)
            employees = self.employees_local

        # BIRTHDAY WISHES
        if self.selection == '1':
            self.wish_message_sender(employees, birthday_names)

        # ANNIVERSARY WISHES
        elif self.selection == '2':
            self.wish_message_sender(employees, anniversary_names)

        else:
            print('\t *** NO VALID SELECTION RECORDED ***')
            print('\t *** PROGRAM WILL EXIT NOW ***')
            time.sleep(2)

        return

    def wish_message_sender(self, employees, wish_names):

        for worker in employees:
            self.worker = worker

            if self.compare_api_and_local_data():
                continue

            employee = Employee(self.worker, employees)

            if self.selection == '1':
                is_valid = ProcessEmployee(employee).validate_birthdays_employees()
            else:
                is_valid = ProcessEmployee(employee).validate_anniversary_employees()

            if is_valid:
                # BirthdayMessage(employee)
                wish_names.append(employee.name)
                print(employee.name)
                self.worker['lastNotification'] = employee.get_current_date.strftime('%Y-%m-%d')

                if self.selection == '1':
                    self.worker['lastBirthdayNotified'] = employee.get_current_date.strftime('%Y-%m-%d')

                self.emp_list.append(self.worker)
            else:
                self.emp_na_list.append(self.worker)

        if self.emp_list:
            JSONData(self.emp_list, None, 'Y', self.emp_list, None).start()

        if self.emp_na_list:
            JSONData(None, self.emp_na_list, 'N', None, self.emp_na_list).start()

        if wish_names:
            SendWishEmail(self.selection, wish_names, crontab=self.crontab).start()
        else:
            if self.selection == '1':
                print('\n ****** NO EMPLOYEE HAS A BIRTHDAY TODAY *******')

            if self.selection == '2':
                print('\n ****** NO EMPLOYEE HAS A WORK-ANNIVERSARY TODAY *******')

        return self.selection
