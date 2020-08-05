# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-02 23:03:52
# @Last Modified by:   rish
# @Last Modified time: 2020-08-05 01:50:19

### Imports START
import logging

from er_extractor import utils
### Impors END


logger = logging.getLogger(__name__)


# [START Procedure for extracting and persisting data]
def get_exchange_rates(
	mode, start_date, end_date, num_threads=4,
	multithreading=True, multithreading_after=10
):
	# Get urls for requests

	logger.info('Collecting dates for request urls')
	dates = utils.collect_request_dates(mode, start_date, end_date)
	logger.info(
		'Extracted dates for which requests need to made: {num}'
		.format(num=len(dates))
	)
	if len(dates) > 0:
		logger.info(
			'Date lowerbound: {} | Date upperbound: {}'
			.format(dates[0], dates[-1])
		)
		logger.info('')

		# Do the requests and get the data
		logger.info('Data collection starts')
		result_df = utils.extract_data(
			dates, multithreading, multithreading_after, num_threads
		)
		logger.info('')

		# Persist the data
		logger.info('Data collected now db persist begins')
		utils.persist_data(result_df)
		logger.info('')
	else:
		logger.info('No new dates found')
		logger.info('')

	return
# [END]
