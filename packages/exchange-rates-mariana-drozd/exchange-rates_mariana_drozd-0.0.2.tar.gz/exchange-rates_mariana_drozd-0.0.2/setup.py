from setuptools import setup, find_packages

VERSION = '0.0.2'

with open("README.md", "r") as f:
    long_description = f.read()

DESCRIPTION = ('A small library for getting information on cash '
               'exchange rates of PrivatBank and the NBU on the selected date')

setup(
    name="exchange-rates_mariana_drozd",
    version=VERSION,
    author="Mariana Drozd",
    author_email="mariana.drozd.work@gmail.com",
    license='MIT',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",

    packages=find_packages(),
    install_requires=['requests', 'pandas', 'matplotlib'],

    keywords=['python', 'exchange rate', 'privatbank'],
    classifiers=[
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        'Source': 'https://gtlb.jetsoftpro.com/mariana.drozd/exchange_rates_mariana_drozd',
    },
)
