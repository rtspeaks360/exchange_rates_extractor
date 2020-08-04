# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-04 00:17:37
# @Last Modified by:   rish
# @Last Modified time: 2020-08-04 21:31:16


### Imports START
import datetime
import os
### Imports END

DATE_FORMAT = '%Y-%m-%d'
DATE_LOWER_BOUND = '2000-01-01'
DATE_UPPER_BOUND = datetime.date.today().strftime(DATE_FORMAT)
LATEST_LOWER_BOUND = 7
EXCHANGE_RATES_API_URL = 'https://api.exchangeratesapi.io/{date}'
CURRENCY_MARKERS = ['USD', 'CAD', 'INR', 'SGD', 'RUB', 'CZK', 'ISK', 'HKD']

if os.environ.keys().__contains__('ENV-INDICATOR') \
	and os.environ['ENV-INDICATOR'] == 'PROD':
	# Environment string
	env_str = 'PROD'
	BASE_PATH = os.environ['SCPATH']

	USER_NAME = ''
	PASSWORD = ''
	HOST = ''
	PORT = ''
	DATABASE = 'pd_exchangerates'
else:
	# Environment string
	env_str = 'DEV'
	BASE_PATH = ''

	USER_NAME = 'rish'
	PASSWORD = 'password'
	HOST = 'localhost'
	PORT = '5432'
	DATABASE = 'pd_exchangerates'

DB_CONN_STRING = 'postgres+psycopg2://{uname}:{pwd}@{host}:{port}/{db}'.format(
	uname=USER_NAME, pwd=PASSWORD, host=HOST, port=PORT, db=DATABASE
)
PG_DB_CONN_STRING = "dbname='{db}' user='{uname}' host='{host}' \
password='{pwd}' port={port}".format(
	uname=USER_NAME, pwd=PASSWORD, host=HOST, port=PORT, db=DATABASE
)
