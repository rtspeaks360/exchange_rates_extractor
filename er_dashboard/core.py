### Imports START
import logging
from flask import Flask, render_template

from er_dashboard import utils
### Imports END


### Initialize Flask app
app = Flask(__name__)
logger = logging.getLogger(__name__)


### Adding routes and handlers
@app.errorhandler(500)
def server_error(e):
	# Log the error and stacktrace.
	logger.error('An error occurred during a request.')
	return 'An internal error occurred.', 500

@app.route("/")
def index():
	graph_data = utils.get_er_csv_string()
	return render_template('dashboard.html', graph_data=graph_data)