from setuptools import setup, find_packages

VERSION = '1.0.0'

with open("README.md", "r") as f:
    long_description = f.read()

DESCRIPTION = ('A small library for getting information on cash '
               'exchange rates of the NBU for the selected date range')

setup(
    name="nbu-exchange-rates",
    version=VERSION,
    author="Oleksandr Sokyrka",
    author_email="sokyrkals@gmail.com",
    license='MIT',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=find_packages(),
    install_requires=['requests', 'matplotlib'],

    keywords=['python', 'exchange rate', 'nbu', 'bank', 'Ukrainian', 'diagram', 'chart', 'graph'],
    classifiers=[
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        'Source': 'https://github.com/lesykbiceps/nbu-exchange-rates',
    },
)
