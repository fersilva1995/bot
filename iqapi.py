from talib.abstract import *
from iqoptionapi.stable_api import IQ_Option
import time
import numpy as np
import datetime


def get_min_max(goal, size, interval):
    max_min_values=[]
    max_values=[]
    min_values=[]
    end_from_time=time.time()
    data=Iq.get_candles(goal, interval, size, end_from_time)

    for  val in data:
        max_values.append(val['max'])
        min_values.append(val['min'])

    max_min_values.append([max(max_values), min(min_values)])
    max_values.remove(max(max_values))
    min_values.remove(min(min_values))

    max_min_values.append([max(max_values), min(min_values)])
    max_values.remove(max(max_values))
    min_values.remove(min(min_values))

    max_min_values.append([max(max_values), min(min_values)])
    max_values.remove(max(max_values))
    min_values.remove(min(min_values))
    return max_min_values

Iq=IQ_Option("scolimoski1995@outlook.com","@Ipdpnm46")
Iq.connect()#connect to iqoption

goal="EURUSD"

date = datetime.datetime.now()
print(date)

#max_min_months = get_min_max(goal, 10, 2592000)
#max_min_week = get_min_max(goal, 7, 86400)
#max_min_day = get_min_max(goal, 1440, 60)

max_min_months = get_min_max(goal, date.day, 2592000)
max_min_week = get_min_max(goal, date.weekday()+1, 86400)
max_min_day = get_min_max(goal, 1440, 60)


  

size=30#size=[1,5,10,15,30,60,120,300,600,900,1800,3600,7200,14400,28800,43200,86400,604800,2592000,"all"]
timeperiod=10
maxdict=20
print("start stream...")
Iq.start_candles_stream(goal,size,maxdict)
print("Start EMA Sample")



while True:
    candles=Iq.get_realtime_candles(goal,size)

    inputs = {
        'open': np.array([]),
        'high': np.array([]),
        'low': np.array([]),
        'close': np.array([]),
        'volume': np.array([])
    }
    for timestamp in candles:

        inputs["open"]=np.append(inputs["open"],candles[timestamp]["open"] )
        inputs["high"]=np.append(inputs["high"],candles[timestamp]["max"] )
        inputs["low"]=np.append(inputs["low"],candles[timestamp]["min"] )
        inputs["close"]=np.append(inputs["close"],candles[timestamp]["close"] )
        inputs["volume"]=np.append(inputs["volume"],candles[timestamp]["volume"] )


    print("Show EMA")
    print(EMA(inputs, timeperiod=timeperiod))
    print("\n")
    time.sleep(1)

    indicators = Iq.get_technical_indicators(goal)
    print(indicators[23])
    print(indicators[21])
    print(indicators[19])
Iq.stop_candles_stream(goal,size)