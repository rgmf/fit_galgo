from setuptools import setup, find_packages


setup(
    name="fit_galgo",
    version="0.2.15",
    author="Román Martínez",
    author_email="rgmf@riseup.net",
    description="Descripción de tu proyecto",
    packages=find_packages(),
    install_requires=[
        "garmin-fit-sdk~=21.115",
        "pydantic~=2.4",
        "pytest~=7.4",
    ],
)
