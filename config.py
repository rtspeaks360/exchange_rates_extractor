# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-04 00:17:37
# @Last Modified by:   rish
# @Last Modified time: 2020-08-04 04:08:23


### Imports START
import datetime
### Imports END

DATE_FORMAT = '%Y-%m-%d'
DATE_LOWER_BOUND = '2000-01-01'
DATE_UPPER_BOUND = datetime.date.today().strftime(DATE_FORMAT)
LATEST_LOWER_BOUND = 7
EXCHANGE_RATES_API_URL = 'https://api.exchangeratesapi.io/{date}'
