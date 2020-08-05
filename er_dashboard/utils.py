### Import START
import io
import logging
import pandas as pd
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
	'''
	session = DBSession()
	query = session.query(models.ExchangeRate).all()

	graph_data = ''
	
	if len(query) > 0: 
		rates = [_.serialize_usd_rate for _ in query]
		rates_df = pd.DataFrame(rates)

		graph_data = graph_data + 'Date,USD\\n'
		for _ in rates:
			graph_data = (
				graph_data 
				+'{},{}\\n'
				.format(_['date'], _['usd'])
			)
	return graph_data