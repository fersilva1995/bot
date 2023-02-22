from iqoptionapi.stable_api import IQ_Option
from RSI import RSI_calc
import time
import numpy


#VARIABLES
goal="EURUSD"
candle_size=60
period=250


rsi_top = 90
rsi_bottom = 10
rsi_period = 7

rsi = RSI_calc(rsi_top, rsi_bottom, rsi_period)
Iq=IQ_Option("scolimoski1995@outlook.com","@Ipdpnm46")
Iq.connect()
Iq.start_candles_stream(goal,candle_size,period)


while True:
    candles=Iq.get_realtime_candles(goal,candle_size)
    inputs = {
        'open': numpy.array([]),
        'high': numpy.array([]),
        'low': numpy.array([]),
        'close': numpy.array([]),
        'volume': numpy.array([])
    }

    for timestamp in candles:
        inputs["open"]=numpy.append(inputs["open"],candles[timestamp]["open"] )
        inputs["high"]=numpy.append(inputs["high"],candles[timestamp]["max"] )
        inputs["low"]=numpy.append(inputs["low"],candles[timestamp]["min"] )
        inputs["close"]=numpy.append(inputs["close"],candles[timestamp]["close"] )
        inputs["volume"]=numpy.append(inputs["volume"],candles[timestamp]["volume"] )

    rsi.set_inputs(inputs)
    time.sleep(0.5)