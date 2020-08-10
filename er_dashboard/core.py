### Imports START
import logging
import os
from flask import Flask, render_template, jsonify

import config
from er_dashboard import utils
### Imports END


### Initialize Flask app
app = Flask(__name__)
logger = logging.getLogger(__name__)


### Adding routes and handlers


# [START Error handler for internal server error]
@app.errorhandler(500)
def server_error(e):
	# Log the error and stacktrace.
	logger.error('An error occurred during a request.')
	return 'An internal error occurred.', 500
# [END]


# [START Exception handlers for bad request handlers.]
@app.errorhandler(400)
def bad_request_error(e):
	# Log the error and stacktrace
	logger.exception('Bad Request. {}'.format(e.description))
	return jsonify(message='Bad Request. {}'.format(e.description)), 400
# [END]


# [START Exception handler for URL not found 404 errors.]
@app.errorhandler(404)
def not_found_error(e):
	# Log the error and stacktrace.
	logger.exception('Not Found. {}'.format(e.description))
	return jsonify(message='Not Found. {}'.format(e.description)), 404
# [END]


# [START Route for the dashboard]
@app.route("/")
def index():
	graph_data = utils.get_er_csv_string()
	return render_template('dashboard.html', graph_data=graph_data)
# [END]


# [START Route to check application status]
@app.route("/status")
def status_check():
	return jsonify(status='200')
# [END]
