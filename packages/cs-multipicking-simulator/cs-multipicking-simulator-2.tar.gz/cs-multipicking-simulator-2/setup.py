from setuptools import setup, find_packages

setup(
    author="CS Dispatcher Operational Research",
    description="CS Dispatcher MP Simulator",
    name='cs-multipicking-simulator',
    version="2",
    packages=find_packages(include=[
            "mp_simulator",
            "mp_simulator.*"
            ]
        ),
    install_requires=[
        'boto3>=1.21.43',
        'dask>=2022.4.1',
        'gurobipy>=9.5.1',
        'numpy>=1.20.2',
        'pandas>=1.2.4',
        'psycopg2_binary>=2.9.3',
        'requests>=2.22.0',
        'pyathena>=2.5.2',
        'requests>=2.22.0',
        'shapely>=1.8.1'
    ]
)