# -*- coding: utf-8 -*-
# @Author: rish
# @Date:   2020-08-02 23:09:08
# @Last Modified by:   rish
# @Last Modified time: 2020-08-04 05:07:12


### Imports START
from sqlalchemy import create_engine, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, BigInteger, Integer, DateTime, Date,\
	JSON, Numeric
from sqlalchemy.sql import func
### Imports END


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
	base = Column(String, nullable=False)

	USD = Column(Numeric)
	CAD = Column(Numeric)
	INR = Column(Numeric)
	SGD = Column(Numeric)
	RUB = Column(Numeric)
	CZK = Column(Numeric)
	ISK = Column(Numeric)
	HKD = Column(Numeric)

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
	print('created_tables')
	return
# [END]


### Creating schema in database START
if __name__ == '__main__':
	import context
	convert_classes_into_tables(context.config.DB_CONN_STRING)
### Creating schema in database END
