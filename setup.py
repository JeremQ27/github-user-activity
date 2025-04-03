from setuptools import setup
from setuptools.config.expand import entry_points

setup(
    name='Github User Activity App',
    version='1.0.0',
    description='A CLI App that monitors user at Github.',
    author='Jeremiah',
    author_email='jeremiahquinto0627@gmail.com',
    url='https://github.com/JeremQ27/github-user-activity',
    py_modules=['app', 'github_tracker'],
    entry_points={
        'console_scripts': [
            'github_monitor=app:main'
        ]
    },
    tests_require=[
        'pytest'
    ]
)