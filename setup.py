from setuptools import setup, find_packages
from os import environ

setup(
        name="urlsafe",
        verison="1.0.0",
        package_dir={'':'src'},
        packages=find_packages('src'),
        include_package_data=True,
        install_requires=list(line.strip() for line in open('requirements.txt')),
        entry_points={
            'console_scripts': [
                'urlsafe = urlsafe:main'
            ]
        }
    )
