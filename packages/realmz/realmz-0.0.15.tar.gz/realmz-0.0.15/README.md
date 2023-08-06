# Wish - A Birthday wishing App

-------------------------------------------------------------------------------------------------

A service component that will send birthday wishes to employees. The service extracts a list of employees whose 
birthdays occur today using the Realm Digital Employee API 
and create a generic message E.g. “Happy Birthday {name 1}, {name 2}” and send the message to an email address 
configured for the component.

------------------------------------------------------------------------------------------------

# INSTRUCTIONS 

Please follow the following steps to set up and run the project on your local environment.

Steps:

1. Clone the repository onto your local environment.

2. Create a virtual environment (using virtualenv or pipenv).
    - pip install virtualenv or 
    - pip install pipenv

3. Install the requirements located in dev.txt in requirements directory.

4. Or download realmz from Pypi (https://pypi.org/project/realmz/) - pip install realmz

5. Locate 'main.py' file as follows src --> realmz --> main.py

6. Run 'main.py' with python main.py

7. Follow the instructions on the screen.
   
-------------------------------------------------------------------------------------

A service component that will send birthday wishes to employees.
The service extracts a list of employees whose birthdays occur today using the Realm Digital Employee API
and create a generic message E.g. “Happy Birthday {name 1}, {name 2}” and send the message to an email
address configured for the component.

The following needs to be considered:
    - Leap years.
    - Employee exclusions. An exclusion can be any of the following:
        - The employee no longer works for Realm Digital;
        - The employee has not started working for Realm Digital;
        - Or the employee has been specifically configured to not receive birthday wishes.
The component must support being executed at most once for a specific employee’s birthday wish, regardless of
how many times the service is scheduled to run on a specific day.

Note: The work anniversary requirement does not need to be coded but the solution design should cater for the
additional requirement.

#API Service
https://interview-assessment-1.realmdigital.co.za/

#PyPI
https://pypi.org/project/realmz/