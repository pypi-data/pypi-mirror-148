from setuptools import setup

with open('VERSION') as file:
    version = file.readline().strip()

setup(
    name="test_job_offer_service",
    version=version,
    packages=['src']
)