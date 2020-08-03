# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-04 00:17:31
# @Last Modified by:   rish
# @Last Modified time: 2020-08-04 01:12:40

### Imports START
import argparse
import datetime
### Imports END

today = datetime.date.today().strftime('%Y-%m-%d')


# [START Function to define parser]
def parser_args():
	'''
	Function to define the structure for command line arguments parser.

	Args:
		-
	Retuns:
		- args
	'''

	parser = argparse.ArgumentParser(
		description='Pipeline to extract the exchange rates data using the\
		exchangerates.io API interface. Use the followring arguments to run\
		the pipeline to get the using the API, and then persist it into the\
		database, or run a flask application to explore the already recorded\
		data.'
	)

	parser.add_argument(
		'--run_as', dest='run_as', choices=['extractor', 'dashboard'],
		help='Use this argument to either extract the data using\
		`extractor` argument or initalize the dashboard to explore the data.'
	)

	parser.add_argument(
		'--get_data_by', dest='get_data_by', default='exhaustive',
		choices=['specific_date', 'specific_date_range', 'latest', 'exhaustive'],
		help='Use this subargument for extractor to\
		specify the criteria for the data retrieval'
	)

	parser.add_argument(
		'--start_date', dest='start_date', default='2000-01-01',
		help='Use this extractor argument to specifiy the start date\
		for the interval for which the data needs to be fetched. The date \
		specified should be greater than equal to 2000-01-01, and must be\
		less than equal to {today}.'.format(today=today)
	)

	parser.add_argument(
		'--end_date', dest='end_date', default=today,
		help='Use this extractor argument to specifiy the end date\
		for the interval for which the data needs to be fetched. The date\
		specified should be greater than equal to 2000-01-01, and must be\
		less than equal to {today}.'.format(today=today)
	)

	parser.add_argument(
		'--multithreading', dest='multithreading', action='store_true',
		help='Use this argument to enable multithreading in case of\
		numeral request urls to reduce the network overhead time. If number\
		of request urls excedes 10, then multitrheading is enabled by default.\
		You can use the multithreading_after argument to change this setting.'
	)

	parser.add_argument(
		'--multithreading_after', dest='multithreading_after', type=int, default=10,
		help='Use this argument to specifiy after how many requests should\
		multithreading be enabled.'
	)

	parser.add_argument(
		'--num_of_threads', dest='num_of_threads', type=int, default=8,
		help='Use this argument to specify how many threads you want to use\
		for multithreading. It is recomended to use the total number of cores you\
		have on your machine as the number of threads.'
	)

	parser.add_argument(
		'--port', dest='port_num', type=int, default=8080,
		help='Use this argument to specifiy the port numebr you wish to use\
		for your desktop application. When running the application in a docker \
		container, only a handful number of ports can be used. It is recomended to \
		stick to the default setting.'
	)

	parser.add_argument(
		'--env', choices=['dev', 'prod'], default='dev',
		help='Use this argument to specify whether the processes are to be run in a\
		development environment or production.'
	)

	# Parsing the arguments received
	args = parser.parse_args()

	return args
# [END]
