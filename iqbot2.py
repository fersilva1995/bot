from iqoptionapi.stable_api import IQ_Option
from paho.mqtt import client as mqtt_client
from RSI import RSI_calc
from Bolinger import Bolinger_calc
from EMA import EMA_calc
import time
import numpy
import random
import json



def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def publish(client, topic, message):
    result = client.publish(topic, message)



#VARIABLES
#------------------------------------------------------------------------
goal="EURUSD"
candle_size=60
period=250


broker = 'localhost'
port = 1883
topic = 'EURUSD'
client_id = f'python-mqtt-{random.randint(0, 1000)}'


rsi_top = 90
rsi_bottom = 10
rsi_period = 7

bolinger_7_multiplier = 2.4
bolinger_7_period = 7
bolinger_21_multiplier = 3.6
bolinger_21_period = 21

ema_100_period = 100
ema_100_duration = 360
ema_200_period = 200
ema_200_duration = 360


#------------------------------------------------------------------------



rsi = RSI_calc(rsi_top, rsi_bottom, rsi_period)
bolinger_7 = Bolinger_calc(bolinger_7_multiplier,bolinger_7_period)
bolinger_21 = Bolinger_calc(bolinger_21_multiplier,bolinger_21_period)
ema100 = EMA_calc(ema_100_duration, ema_100_period)
ema200 = EMA_calc(ema_200_duration, ema_200_period)

#------------------------------------------------------------------------


client = mqtt_client.Client(client_id)
client.on_connect = on_connect
client.connect(broker, port)


Iq=IQ_Option("scolimoski1995@outlook.com","@Ipdpnm46")
Iq.connect()
Iq.start_candles_stream(goal,candle_size,period)

#------------------------------------------------------------------------



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
    bolinger_7.set_inputs(inputs)
    bolinger_21.set_inputs(inputs)
    ema100.set_inputs(inputs)
    ema200.set_inputs(inputs)

    message =  {
        "rsi": round(rsi.rsi, 4),
        "upperBolinger7": round(bolinger_7.bolinger_upper,5),
        "middleBolinger7": round(bolinger_7.bolinger_middle,5),
        "lowerBolinger7": round(bolinger_7.bolinger_lower,5),
        "upperBolinger21": round(bolinger_21.bolinger_upper,5),
        "middleBolinger21": round(bolinger_21.bolinger_middle,5),
        "lowerBolinger21": round(bolinger_21.bolinger_lower,5),
        "ema100": round(ema100.ema, 5),
        "ema200": round(ema200.ema, 5),
    }

    publish(client, topic, json.dumps(message))
    time.sleep(0.5)