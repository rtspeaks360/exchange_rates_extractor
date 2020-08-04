# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-02 23:03:47
# @Last Modified by:   rish
# @Last Modified time: 2020-08-04 21:16:45

### Imports START
import logging
import sys
import requests
import pandas as pd
from datetime import datetime, date, timedelta
from queue import Queue
from threading import Thread

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

# [START Worker class that defines what each worker needs to do]
class APIExtractionWorker(Thread):

	def __init__(self, queue):
		Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			# Get the work from the queue and expand the tuple
			results_list, date = self.queue.get()
			try:
				results_list.append(_api_request(date))
			finally:
				self.queue.task_done()
# [END]


# [START Function to make API request]
def _api_request(date):
	'''
	'''
	logger.info(config.EXCHANGE_RATES_API_URL.format(date=date))
	req = requests.get(config.EXCHANGE_RATES_API_URL.format(date=date))
	req_json = req.json()
	req_json['status_code'] = req.status_code

	return req_json
# [END]


# [START Function to collect data from the api]
def _get_data_from_api(
	dates, multithreading, multithreading_after, num_threads
):
	'''
	'''
	results = []

	if multithreading and len(dates) > multithreading_after:
		logger.info('Setting up multithreading')
		queue = Queue()
		for _ in range(num_threads):
			worker = APIExtractionWorker(queue)
			worker.daemon = True
			worker.start()
		for _d in dates:
			queue.put((results, _d))
		queue.join()
		logger.info(len(results))

	else:
		for _d in dates:
			results.append(_api_request(_d))

	return results
# [END]


# [START Function to get the required results frame]
def extract_data(
	dates, multithreading, multithreading_after, num_threads
):
	'''
	'''
	# Collect data
	results = _get_data_from_api(
		dates, multithreading,
		multithreading_after, num_threads
	)

	# process collected data
	df = pd.DataFrame(results)
	rates_df = pd.DataFrame(df.rates.to_list())
	rates_df = rates_df[config.CURRENCY_MARKERS]
	df = pd.concat([df, rates_df], axis=1)
	df.rename(columns={'rates': 'rates_payload'}, inplace=True)

	logger.info(df.columns)
	logger.info(df.shape)

	return df
# [END]


# [START Function to persist data into the database]
def persist_data(df):
	'''
	'''
	pass
# [END]
