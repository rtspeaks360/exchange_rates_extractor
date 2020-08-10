### Import START
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from er_extractor import models
### Import END


### Global declarations START
logger = logging.getLogger(__name__)

engine = create_engine(config.DB_CONN_STRING)
models.Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
### Global declarations end


# [START Function to get the csv string for dashboard]
def get_er_csv_string():
	'''
	Function to get the overall exchange rates, and convert
	them into csv string for Dygraph plot.

	Args:
		-
	Returns:
		- graph data csv string
	'''
	session = DBSession()
	query = session.query(models.ExchangeRate).all()

	graph_data = ''

	if len(query) > 0:
		rates = [_.serialize_usd_rate for _ in query]

		graph_data = graph_data + 'Date,USD\\n'
		for _ in rates:
			graph_data = (
				graph_data + '{},{}\\n'
				.format(_['date'], _['usd'])
			)
	return graph_data
