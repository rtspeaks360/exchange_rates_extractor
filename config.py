# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-04 00:17:37
# @Last Modified by:   rish
# @Last Modified time: 2020-08-04 04:59:01


### Imports START
import datetime
import os
### Imports END

DATE_FORMAT = '%Y-%m-%d'
DATE_LOWER_BOUND = '2000-01-01'
DATE_UPPER_BOUND = datetime.date.today().strftime(DATE_FORMAT)
LATEST_LOWER_BOUND = 7
EXCHANGE_RATES_API_URL = 'https://api.exchangeratesapi.io/{date}'

if os.environ.keys().__contains__('ENV-INDICATOR') \
	and os.environ['ENV-INDICATOR'] == 'PROD':
	# Environment string
	env_str = 'PROD'
	DB_CONN_STRING = ''
	BASE_PATH = os.environ['SCPATH']
else:
	# Environment string
	env_str = 'DEV'
	DB_CONN_STRING = 'mysql+mysqlconnector://rish@localhost/pd_exchangerates'
	BASE_PATH = ''
