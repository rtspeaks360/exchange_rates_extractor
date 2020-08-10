# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-02 23:03:47
# @Last Modified by:   rish
# @Last Modified time: 2020-08-10 12:35:20

### Imports START
import logging
import sys
import requests
import pandas as pd
import numpy as np
import mysql.connector as db_connector
from datetime import datetime, date, timedelta
from queue import Queue
from threading import Thread
from sqlalchemy.dialects import mysql
from sqlalchemy import exc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from er_extractor import models
### Imports END


### Global declarations START
logger = logging.getLogger(__name__)

engine = create_engine(config.DB_CONN_STRING)
models.Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
### Global declarations end


### Functions to support computation of target dates START


# [START Function to get dates alreday recorded]
def _get_recorded_dates():
	'''
	Function to get the dates from the database for which data has already
	been collected, so that we don't make the same request and persist the
	same data twice.
	'''
	session = DBSession()
	query = session.query(models.ExchangeRate).all()
	dates = []

	if len(query) > 0:
		for _ in query:
			dates.append(str(_.date))
	session.close()
	return dates
# [END]


# [START Function to get latest start date ]
def _get_latest_start_date():
	'''
	Function to get the start date for fetching the latest data.

	Args:
		-
	Returns:
		- start_date
	'''
	today = date.today()
	limit_date = today - timedelta(days=config.LATEST_LOWER_BOUND)
	return limit_date.strftime(config.DATE_FORMAT)
# [END]


# [START Function to specify interval edges]
def _get_edges_for_interval(mode, start_date, end_date):
	'''
	Function to specify the interval edges based on on run mode. Based on
	the edges we get the dates in the interval.

	Args:
		- mode
		- start_date
		- end_date
	Returns:
		- start_date_parsed
		- end_date_parsed
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
	Returns:
		- list of target dates
	'''
	start_date_parsed, end_date_parsed = _get_edges_for_interval(
		mode, start_date, end_date
	)
	print(start_date_parsed, end_date_parsed)
	if mode == 'date':
		return [start_date_parsed.strftime(config.DATE_FORMAT)]

	dates = []
	# Get already recored dates from db
	dates_from_db = _get_recorded_dates()

	# Create dates for interval
	delta = end_date_parsed - start_date_parsed

	for _ in range(delta.days + 1):
		day = start_date_parsed + timedelta(days=_)
		dates.append(day.strftime(config.DATE_FORMAT))

	# Exclude already recorded dates
	dates = list(set(dates) - set(dates_from_db))
	dates = [str(_) for _ in dates]
	return dates
# [END]


### Functions to support computation of target dates END

### Functions and classes for getting data from API START


# [START Worker class that defines what each worker needs to do]
class APIExtractionWorker(Thread):
	'''
	APIExtractionWorker class that provides the instructions for that each
	thread needs to execute for every input in the queue.
	'''

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
	Function to do the API request and do the processing on the
	response required

	Args:
		- date
	Returns:
		- response json
	'''
	req = requests.get(config.EXCHANGE_RATES_API_URL.format(date=date))
	req_json = req.json()
	req_json['request_status'] = req.status_code

	return req_json
# [END]


# [START Function to collect data from the api]
def _get_data_from_api(
	dates, multithreading, multithreading_after, num_threads
):
	'''
	Function that gets the data from the API either using multithreading
	and even wiuthout it.

	Args:
		- dates
		- multitheading
		- multithreading after
		- num of threads
	Returns:
		- list of results
	'''
	results = []

	if multithreading and len(dates) > multithreading_after:
		logger.info(
			'Setting up multithreading with {} threads'
			.format(num_threads)
		)
		queue = Queue()

		# Intialize worker threads
		for _ in range(num_threads):
			worker = APIExtractionWorker(queue)
			worker.daemon = True
			worker.start()

		# Queue dates
		for _d in dates:
			logger.info(
				'Queing URL - {}'
				.format(
					config.EXCHANGE_RATES_API_URL
					.format(date=_d)
				)
			)
			queue.put((results, _d))
		# Waiting for all workers to finish
		queue.join()
	else:
		logger.info('Getting results...')
		for _d in dates:
			results.append(_api_request(_d))
		logger.info('Use multithreading for better performance.')
	logger.info('')
	return results
# [END]


# [START Function to get the required results frame]
def extract_data(
	dates, multithreading, multithreading_after, num_threads
):
	'''
	Function to extract the data from the API, do the required
	preprocessing and return a frame with the target response.

	Args:
		- dates
		- multithreading
		- multithreading_after
		- num_threads
	Returns:
		- final dataframe
	'''
	# Collect data
	results = _get_data_from_api(
		dates, multithreading,
		multithreading_after, num_threads
	)
	logger.info('Total responses: {}'.format(len(results)))

	# process collected data
	df = pd.DataFrame(results)
	rates_df = pd.DataFrame(df.rates.to_list())
	_cols = (set(config.CURRENCY_MARKERS) - set(rates_df.columns))

	for _ in _cols:
		rates_df[_] = np.nan

	rates_df = rates_df[config.CURRENCY_MARKERS]
	df = pd.concat([df, rates_df], axis=1)
	df.rename(columns={'rates': 'rates_payload'}, inplace=True)

	# For dates that did not get a response
	df.drop_duplicates(subset=['date'], inplace=True)
	logger.info(
		'{} unique data points for exchange rates fetched'
		.format(df.shape[0])
	)

	# Check for dates not found
	dates_nf = list(set(dates) - set(df.date.to_list()))

	if len(dates_nf) > 0:
		logger.info(
			'{} dates in range for which no data was found'
			.format(len(dates_nf))
		)
		temp_df = pd.DataFrame(
			[[_, 404, 'EUR'] for _ in dates_nf],
			columns=['date', 'request_status', 'base']
		)
		df = df.append(temp_df, sort=False)
		df = df.loc[~df.date.isin(_get_recorded_dates())]
	df.sort_values(by='date', inplace=True)
	return df
# [END]


### Functions and classes for getting data from API END

### Functions to do the database setup and persist START


# [START Function to persist data into the database]
def persist_data(df):
	'''
	Function to persist the data into the database.

	Args:
		- dataframe
	Returns:
		-
	'''
	session = DBSession()

	df.fillna(value=np.nan, inplace=True)
	df.replace({np.nan: None}, inplace=True)

	insert_stmt = (
		mysql
		.insert(models.ExchangeRate.__table__)
		.values(df.to_dict(orient='records'))
	)

	try:
		session.execute(insert_stmt)
		session.commit()
		logger.info('Added {} rows in database'.format(df.shape[0]))
	except exc.SQLAlchemyError as e:
		logger.error('Session commit failed.')
		logger.error(e._message)
		session.rollback()

	session.close()

	return
# [END]


# [START Function to initialize the database]
def initdb():
	'''
	Function to initialize the database and create the database tables

	Args:
		-
	Returns:
		-
	'''

	query = 'CREATE DATABASE IF NOT EXISTS pd_exchangerates;'

	conn = db_connector.connect(
		host=config.HOST, user=config.USER_NAME,
		password=config.PASSWORD,
		port=config.PORT
	)
	cursor = conn.cursor()
	cursor.execute(query)
	conn.commit()
	conn.close()
	logger.info('Created database if didn\'t exist')

	models.convert_classes_into_tables(config.DB_CONN_STRING)
	logger.info('Mapped sqlalchemy models into databae tables')

	return

# [END]
### Functions to do the database setup and persist END
