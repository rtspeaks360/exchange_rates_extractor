# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-04 00:16:57
# @Last Modified by:   rish
# @Last Modified time: 2020-08-05 00:59:51

### Imports START
import os
import sys
import time
import logging

import config
import parser
### Imports END

# Logger settings
logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get script name and extract script path.
script_name = sys.argv[0]
script_path = script_name[:-8]

# Get arguments received
args = parser.parser_args()


if args.env == 'prod':
	logger.info('prod environment')
	os.environ['ENV-INDICATOR'] = 'PROD'
	os.environ['SCPATH'] = script_path

	# Activate virtual environment with installed dependencies
	activate_this = script_path + 'env/bin/activate_this.py'
	with open(activate_this) as file_:
		exec(file_.read(), dict(__file__=activate_this))

	# Use project directory
	sys.path.insert(0, script_path)
else:
	os.environ['ENV-INDICATOR'] = 'DEV'


from er_extractor import core as er_extractor


# [START Main function for the pipeline]
def main(args):
	'''
	Main function for the extraction pipeline as well as the exploration
	dashboard.

	Args:
		- args
	Returns:
		-
	'''

	if args.run_as == 'extractor':
		logger.info('Running application as extractor process')
		logger.info('')

		er_extractor.get_exchange_rates(
			args.get_data_by, args.start_date, args.end_date,
			args.num_of_threads, args.multithreading,
			args.multithreading_after
		)
	elif args.run_as == 'dashboard':
		pass
	elif args.initdb:
		er_extractor.utils.models.convert_classes_into_tables(config.DB_CONN_STRING)
	else:
		logger.warning('Invalid `run_as` argument.')

	return
# [END]


if __name__ == '__main__':
	# Process start time
	process_start = time.time()

	logger.info('Your namespace - ' + str(args))
	logger.info('')

	# Call for main function
	main(args)

	process_time = time.time() - process_start
	mins = int(process_time / 60)
	secs = int(process_time % 60)

	logger.info(
		'Total time consumed: {mins} minutes {secs} seconds'
		.format(mins=mins, secs=secs)
	)
	logger.info('')
	logger.info('-*-*-*-*-*-*-*-*-*-*-*-*-END-*-*-*-*-*-*-*-*-*-*-*-*-')
	logger.info('')
