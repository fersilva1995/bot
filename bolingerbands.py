from talib.abstract import *
from iqoptionapi.stable_api import IQ_Option
import time
import numpy as np
import datetime
import statistics



Iq=IQ_Option("scolimoski1995@outlook.com","@Ipdpnm46")
Iq.connect()
goal="EURUSD"
candle_period=60
period = 21
period2 = 21
end_from_time=time.time()
data=Iq.get_candles(goal, candle_period, period, end_from_time)
indicators = Iq.get_technical_indicators(goal)


inputs = {
    'open': np.array([]),
    'high': np.array([]),
    'low': np.array([]),
    'close': np.array([]),
    'volume': np.array([])
}

for candle in data:

    inputs["open"]=np.append(inputs["open"],candle["open"] )
    inputs["high"]=np.append(inputs["high"],candle["max"] )
    inputs["low"]=np.append(inputs["low"],candle["min"] )
    inputs["close"]=np.append(inputs["close"],candle["close"] )
    inputs["volume"]=np.append(inputs["volume"],candle["volume"] )

sma = SMA(inputs, timeperiod=period)
print(sma)
print(sma[len(sma)-1] + (statistics.stdev(inputs["close"]))*3.6)
print(sma[len(sma)-1] - (statistics.stdev(inputs["close"]))*3.6)


