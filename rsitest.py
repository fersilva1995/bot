from talib.abstract import *
from iqoptionapi.stable_api import IQ_Option
import time
import numpy as np
import datetime

Iq=IQ_Option("scolimoski1995@outlook.com","@Ipdpnm46")
Iq.connect()
goal="EURJPY"
interval=2592000
size = 8
end_from_time=time.time()
data=Iq.get_candles(goal, interval, size, end_from_time)

inputs = []
gain = []
losses = []
rsi = 0

for index in range(len(data)):
    inputs.append(data[index]["close"])


print(inputs)


for i in range(len(inputs)):
    if(i != 0):
        if(inputs[i] > inputs[i-1]):
            gain.append(inputs[i]-inputs[i-1])
            losses.append(0)
        else:
            losses.append(inputs[i-1]-inputs[i])
            gain.append(0)

#avggp = ((sum(gain)/len(gain))*(size-1))/len(gain)
#avglp = ((sum(losses)/len(losses))*(size-1))/len(losses)x
indicators = Iq.get_technical_indicators(goal)
avggp = (sum(gain)/size)
avglp = (sum(losses)/size)
avg = avggp/avglp
rsi = 100 -(100/(1+(avg)))

print("Show RSI")
print(rsi)
