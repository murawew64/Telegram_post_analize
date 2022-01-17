import configparser
from openapi_client import openapi
import csv
import time
from datetime import date, datetime, timedelta


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    token = config['TOKEN']['api_token']
    client = openapi.api_client(token)

    print(client.user.user_accounts_get())


if __name__ == '__main__':
    main()
