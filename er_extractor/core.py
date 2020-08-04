# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-02 23:03:52
# @Last Modified by:   rish
# @Last Modified time: 2020-08-04 20:41:23

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
	dates = utils.collect_request_dates(mode, start_date, end_date)
	logger.info(len(dates))
	logger.info(dates[0])
	logger.info(dates[-1])

	# Do the requests and get the data
	result_df = utils.extract_data(
		dates, multithreading, multithreading_after, num_threads
	)

	# Persist the data
	utils.persist_data(result_df)
	pass
# [END]
