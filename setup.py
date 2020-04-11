from setuptools import find_packages, setup
import os

HERE = os.path.dirname(__name__)
REQUIRED = [
    "Flask", "mypy", "mistune"
]

setup(
    name="blog",
    version="0.0.1",
    install_requires=REQUIRED,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)