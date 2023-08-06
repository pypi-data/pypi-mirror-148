from setuptools                         import setup, find_packages


setup(
    name='realmz',
    version='0.0.17',
    license='MIT',
    author='Billy Katalayi',
    author_email='billysbn7@gmail.com',
    description="To send birthday wishes to employees",
    long_description='''\n\n
    Realmz
    
    This is a very small module built for a private project. Should you want to do more than the basis functionalities 
    supported by this package, then you are looking on the wrong place. A service component that will send birthday 
    wishes to employees. The service extracts a list of employees whose birthdays occur today using the Realm Digital 
    Employee API and create a generic message E.g. “Happy Birthday {name 1}, {name 2}” and send the message to an 
    email address configured for the component. https://interview-assessment-1.realmdigital.co.za/
    
    Example:
    
        from realmz import main as realmz_main
        
        def test():
            realmz.start_wish()
            
        test()
                        
    You'd input the database full path in case you'd like to save data to a database instead of a json file.
    Please note that we currently only support sqlite.
    
    When prompted with options:
        1. Birthday
        2. Anniversary
        
    This package uses 'https://pypi.org/project/python-dotenv/' to handle .env variable for this project.
    
    This package uses 'https://pypi.org/project/schedule/' to schedule the app, when and how it would run.
    ''',
    packages=find_packages('src'),
    package_dir={'' : 'src'},
    url='https://github.com/Billykat7/wishes',
    keywords='employees birthday, anniversary automated wishes',
    project_urls = {
        "Bug Tracker": 'https://github.com/Billykat7/wishes/issues',
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        # 'celery',
        'python-dotenv',
        # 'redis',
        'requests',
        'schedule',
        # 'SQLAlchemy'
    ],
    include_package_data=True,
    python_requires = ">=3.6"
)
