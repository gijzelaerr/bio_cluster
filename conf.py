from os import environ
from sys import exit

if 'OCA_USER' in environ:
    USER = environ['OCA_USER']
else:
    print("please set OCA_USER environment variable")
    exit(1)

if 'OCA_PASSWORD' in environ:
    PASSWORD = environ['OCA_PASSWORD']
else:
    print("please set OCA_PASSWORD environment variable")
    exit(1)

ENDPOINT = 'https://api.hpccloud.surfsara.nl/RPC2'
