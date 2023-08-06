#!/usr/bin/env python

"""The setup script."""
from setuptools import setup

with open("README.md", encoding="utf8") as readme_file:
    long_description = readme_file.read()


requirements = [
    "shapash>=2.0.0",
    "nbconvert>=6.0.7",
    "papermill>=2.3.2",
    "seaborn<=0.11.1",
    "catboost>=0.22",
    "scipy>=1.4.0",
    "ipywidgets>=7.4.2",
    "jupyter",
    "datapane==0.14.0",
    "werkzeug==2.0.1",
    "jinja2>=2.11.0,<3.1.0",
]


setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest",
]

setup(
    name="eurybia",  # Replace with your own username
    version="0.0.1",
    python_requires=">3.6, < 3.10",
    url="https://github.com/MAIF/eurybia",
    author="Nicolas Roux, Johann Martin, Thomas Bouché",
    author_email="thomas.bouche@maif.fr",
    description="drift",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    license="Apache Software License 2.0",
    keywords="eurybia",
    package_dir={
        "eurybia": "eurybia",
        "eurybia.data": "eurybia/data",
        "eurybia.core": "eurybia/core",
        "eurybia.report": "eurybia/report",
        "eurybia.style": "eurybia/style",
        "eurybia.utils": "eurybia/utils",
    },
    packages=["eurybia", "eurybia.data", "eurybia.core", "eurybia.report", "eurybia.style", "eurybia.utils"],
    data_files=[
        ("data", ["eurybia/data/house_prices_dataset.csv"]),
        ("data", ["eurybia/data/house_prices_labels.json"]),
        ("data", ["eurybia/data/titanicdata.csv"]),
        ("style", ["eurybia/style/colors.json"]),
    ],
    include_package_data=True,
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    zip_safe=False,
)
