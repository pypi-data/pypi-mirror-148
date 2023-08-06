from influxdb_lite.client import Client
from influxdb_lite.measurement import Measurement
from influxdb_lite.attributes import Tag, Field, Timestamp
import configparser
import datetime as dt
import time

def create_db_session(org: str = 'perrytec', timeout: int = None):
    """ Returns an influxdb session instance """
    host, token = get_db_credentials()
    if timeout:
        return Client(url=host, token=token, org=org)
    else:
        return Client(url=host, token=token, org=org, timeout=timeout)


# noinspection PyBroadException
def get_db_credentials():
    environ = configparser.ConfigParser()
    filename = '../../environment.ini'
    environ.read(filename)
    return environ['influxdb']['host'], environ['influxdb']['token']


class FundingRates(Measurement):
    name = 'funding_rates'
    bucket = 'market_data'
    inst_id = Tag()
    current_funding = Field()
    funding_time = Field()
    predicted_funding = Field()


class InterestRates(Measurement):
    name = 'interest_rates'
    bucket = 'market_data'
    exchange = Tag()
    currency = Tag()
    interest_rate = Field()

fundings = FundingRates

funding_measure = fundings(inst_id=1, funding_time=0.0, predicted_funding=1)
interest_measure = InterestRates(currency='btc', interest_rate=0.2)

#interests = InterestRates
#print(fundings.name)
#with create_db_session() as client:
#    result = client.\
#        query(measurement=interests).\
#        range(start=int(time.time())-3600*24*7).\
#        filter(interests.exchange.in_(['bybit'])).last("_time")
#
#        #group_by(['inst_id']).order_by(['inst_id']).limit(1)
#        #select(['current_funding', '_time', 'inst_id']).\
#    print(result.query_str)
#    tables = result.all()
#    print(tables[0].records[0].values)
measures = [interest_measure]#, fundings(inst_id=2, current_funding=0.02, funding_time=0.0, predicted_funding=0.2,
                            #          _time=int(time.time()))]
with create_db_session() as client:
    client.bulk_insert(measures)
