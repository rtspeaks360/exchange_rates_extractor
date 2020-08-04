# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-02 23:09:08
# @Last Modified by:   rish
# @Last Modified time: 2020-08-04 22:05:26


### Imports START
import logging
from sqlalchemy import create_engine, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, Date,\
	JSON, Float
from sqlalchemy.sql import func
### Imports END

logger = logging.getLogger(__name__)

# Object for the delcaratove base class
Base = declarative_base()

### Model Class to define the data base structure START


# [START ExchangeRate model to define the exchange_rates table]
class ExchangeRate(Base):
	'''
	Model class that defines the structure for the exchange rates
	table in the database.
	'''

	__tablename__ = 'exchange_rates'

	_id = Column(BigInteger, primary_key=True)

	date = Column(Date, nullable=False, unique=True)
	base = Column(String(3), nullable=False)

	USD = Column(Float)
	CAD = Column(Float)
	INR = Column(Float)
	SGD = Column(Float)
	RUB = Column(Float)
	CZK = Column(Float)
	ISK = Column(Float)
	HKD = Column(Float)

	rates_payload = Column(JSON, nullable=False)
	request_status = Column(Integer, nullable=False)

	insert_time = Column(DateTime, nullable=False, default=func.now())
	update_time = Column(
		DateTime, nullable=False,
		default=func.now(),
		onupdate=func.current_timestamp()
	)

	UniqueConstraint(
		date, base,
		name='unique_date_base_exchange_rates'
	)
# [END]


# [START Code to create the database from all the above schema classes]
def convert_classes_into_tables(connection_string):
	'''
	Function that maps and creates the tables in the databse from all
	the above schema.

	Args:
		- connection string
	Returns:
		-
	'''

	engine = create_engine(connection_string)
	Base.metadata.create_all(engine)
	logger.info('created_tables')
	return
# [END]


### Creating schema in database START
if __name__ == '__main__':
	import context
	convert_classes_into_tables(context.config.DB_CONN_STRING)
### Creating schema in database END
