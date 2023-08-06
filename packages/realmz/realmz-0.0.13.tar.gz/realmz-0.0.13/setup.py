from setuptools                         import setup, find_packages


setup(
    name='realmz',
    version='0.0.13',
    license='MIT',
    author='Billy Katalayi',
    author_email='billysbn7@gmail.com',
    description="To send birthday wishes to employees",
    long_description='''
    A service component that will send birthday wishes to employees. The service extracts a list of employees whose birthdays occur today using the Realm Digital Employee API
and create a generic message E.g. “Happy Birthday {name 1}, {name 2}” and send the message to an email address configured for the component. https://interview-assessment-1.realmdigital.co.za/
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
        "Operating System :: OS Independent",
    ],
    install_requires=[
        # 'celery',
        'python-dotenv',
        # 'redis',
        'requests',
        'SQLAlchemy'
    ],
    include_package_data=True,
    python_requires = ">=3.6"
)
