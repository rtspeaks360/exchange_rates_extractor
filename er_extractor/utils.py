# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-02 23:03:47
# @Last Modified by:   rish
# @Last Modified time: 2020-08-04 14:29:04

### Imports START
import logging
import sys
from datetime import datetime, date, timedelta

import config
from er_extractor import models
### Imports END


logger = logging.getLogger(__name__)


# [START Function to get dates alreday recorded]
def _get_recorded_dates():
	'''
	'''
	return []
# [END]


# [START Function to get latest start date ]
def _get_latest_start_date():
	# Get last recorded date
	# date = session.query()
	today = date.today()
	limit_date = today - timedelta(days=config.LATEST_LOWER_BOUND)
	return limit_date.strftime(config.DATE_FORMAT)
# [END]


# [START Function to specify interval edges]
def _get_edges_for_interval(mode, start_date, end_date):
	'''
	'''

	if mode == 'exhaustive':
		start_date = config.DATE_LOWER_BOUND
		end_date = config.DATE_UPPER_BOUND
	elif mode == 'latest':
		# TODO: Set start date as last date from db or 30 days prior
		start_date = _get_latest_start_date()
		end_date = date.today().strftime(config.DATE_FORMAT)

	try:
		start_date_parsed = (
			datetime.strptime(start_date, config.DATE_FORMAT)
			if start_date is not None else None
		)
		end_date_parsed = (
			datetime.strptime(end_date, config.DATE_FORMAT)
			if end_date is not None else None
		)

		# Limit the end date to today in case out of bound
		if end_date_parsed is not None and end_date_parsed.date() > date.today():
			end_date_parsed = datetime.today()
	except Exception as e:
		logger.error(e)
		raise(e)
		sys.exit()

	return start_date_parsed, end_date_parsed


# [START Function to collect request dates]
def collect_request_dates(mode, start_date, end_date):
	'''
	Function to collect request urls for which requests need to be made based
	on the run mode and already recorded dates.

	Args:
		- mode
		- start_date
		- end_date
	'''
	logger.info('collecting request urls')

	start_date_parsed, end_date_parsed = _get_edges_for_interval(
		mode, start_date, end_date
	)

	if mode == 'date':
		return [start_date_parsed.strftime(config.DATE_FORMAT)]

	dates = []
	# Get already recored dates from db
	dates_from_db = _get_recorded_dates()

	# Create dates for interval
	delta = end_date_parsed - start_date_parsed
	print(delta)
	for _ in range(delta.days + 1):
		day = start_date_parsed + timedelta(days=_)
		dates.append(day.strftime(config.DATE_FORMAT))

	# Exclude already recorded dates
	dates = list(set(dates) - set(dates_from_db))
	return dates
# [END]


# [START Function to make the network requests]
def get_data_from_api(
	urls, multithreading, multithreading_after, num_threads
):
	'''
	'''
	pass
# [END]
