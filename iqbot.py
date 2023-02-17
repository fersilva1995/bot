from iqoptionapi.stable_api import IQ_Option
from talib.abstract import *
import time
import numpy as np
import statistics
import datetime
import csv
import socket
import sys
from playsound import playsound



TCP_IP = '127.0.0.1'
TCP_PORT = 11000


max_min_day={ "max_points": [], "min_points": []}
max_min_month={ "max_points": [], "min_points": []}
max_min_months={ "max_points": [], "min_points": []}

rsi_top = 90
rsi_bottom = 10

ema_100_duration = 90
ema_200_duration = 90
ema_100_lower_counter = 0
ema_100_upper_counter = 0
ema_200_lower_counter = 0
ema_200_upper_counter = 0
ema_100_lower_active = False
ema_100_upper_active = False
ema_200_lower_active = False
ema_200_upper_active = False
ema_100_status = "unknown"
ema_200_status = "unknown"
all_win = False

last_input = []


def bolinger_band(inputs, period, multiplicator):
    inputs_len = len(inputs["open"])
    bolinger_adjust = 1
    bolinge_inputs = {
        'open': np.array(inputs["open"][inputs_len - (period + bolinger_adjust):inputs_len - bolinger_adjust]),
        'high': np.array(inputs["high"][inputs_len - (period + bolinger_adjust):inputs_len - bolinger_adjust]),
        'low': np.array(inputs["low"][inputs_len - (period + bolinger_adjust):inputs_len - bolinger_adjust]),
        'close': np.array(inputs["close"][inputs_len - (period + bolinger_adjust):inputs_len - bolinger_adjust]),
        'volume': np.array(inputs["volume"][inputs_len - (period + bolinger_adjust):inputs_len - bolinger_adjust])
    }
    sma = SMA(bolinge_inputs, timeperiod=period) 
    return {
        'upper': sma[len(sma) - 1] + ((statistics.stdev(bolinge_inputs["close"]))*multiplicator),
        'middle': sma[len(sma) - 1] ,
        'lower': sma[len(sma) - 1] - ((statistics.stdev(bolinge_inputs["close"]))*multiplicator)
    }



def rsi_line(inputs, period):
    rsi_adjust = 1
    rsi_inputs = {
        'open': np.array(inputs["open"][len(inputs["open"]) - (period+rsi_adjust):]),
        'high': np.array(inputs["high"][len(inputs["high"]) - (period+rsi_adjust):]),
        'low': np.array(inputs["low"][len(inputs["low"]) - (period+rsi_adjust):]),
        'close': np.array(inputs["close"][len(inputs["close"]) - (period+rsi_adjust):]),
        'volume': np.array(inputs["volume"][len(inputs["volume"]) - (period+rsi_adjust):])
    }

    rsi = RSI(rsi_inputs, timeperiod=period)
    return rsi[len(rsi) - 1]

#def EMA_values(indicators):
#    return {
#        'EMA200': indicators[23]['value'],
#        'EMA100': indicators[21]['value'],
#        'EMA50': indicators[19]['value'],
#    }

def EMA_values( inputs, period):
    inputs_len = len(inputs["open"])
    ema_adjust = 0
    ema_inputs = {
        'open': np.array(inputs["open"][inputs_len - (period + ema_adjust):inputs_len - ema_adjust]),
        'high': np.array(inputs["high"][inputs_len - (period + ema_adjust):inputs_len - ema_adjust]),
        'low': np.array(inputs["low"][inputs_len - (period + ema_adjust):inputs_len - ema_adjust]),
        'close': np.array(inputs["close"][inputs_len - (period + ema_adjust):inputs_len - ema_adjust]),
        'volume': np.array(inputs["volume"][inputs_len - (period + ema_adjust):inputs_len - ema_adjust])
    }

    ema = EMA(ema_inputs, period)
    return ema[len(ema)-1]


def max_min_values(goal, candle_size, period, length, actual_value):
    end_from_time=time.time()
    data=Iq.get_candles(goal, candle_size, period, end_from_time)
    max_min={ "max_points": [], "min_points": []}
    max_values=[]
    min_values=[]
    for  val in data:
        max_values.append(val['max'])
        min_values.append(val['min'])


    for counter in range(length):   
        if(actual_value < max(max_values)):
            max_min["max_points"].append(max(max_values))
            max_values.remove(max(max_values))

        if(actual_value > min(min_values)):
            max_min["min_points"].append(min(min_values))
            min_values.remove(min(min_values))
        
    return max_min

def check_decreasing_increasing(input):
    if(input["open"] < input["close"]):
        return "increasing"
    else:
        return "decreasing"

def count_last_types(inputs):
    counter = len(inputs["close"]) -1
    stop = False
    last_value = check_decreasing_increasing(
        {
            'open': inputs["open"][counter],
            'high': inputs["high"][counter],
            'low': inputs["low"][counter],
            'close': inputs["close"][counter],
            'volume': inputs["volume"][counter]
        }
    )
    counter = counter - 1
    result = 1
    while counter > 0 and stop == False:
        old_value = check_decreasing_increasing(
            {
                'open': inputs["open"][counter],
                'high': inputs["high"][counter],
                'low': inputs["low"][counter],
                'close': inputs["close"][counter],
                'volume': inputs["volume"][counter]
            }
        )
        if last_value == old_value:
            result = result + 1
            counter =  counter - 1
        else:
            stop = True

    return { 
        "operation" : last_value,
        "result" : result
    }
    

Iq=IQ_Option("scolimoski1995@outlook.com","@Ipdpnm46")
Iq.connect()
goal="GBPUSD"
if(len(sys.argv) > 0):
    goal=sys.argv[1]

candle_size=60
period=250

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((TCP_IP, TCP_PORT))clea



Iq.start_candles_stream(goal,candle_size,period)

with open('data.csv', 'w', encoding='utf8') as file:
    writer = csv.writer(file)
    header = ['datetime', 'pontos','valor', 'rsi', 'b7l', 'b7u','b21l', 'b21u', 'ema100', 'ema200']
    writer.writerow(header)
    while True:
        points = 0
        candles=Iq.get_realtime_candles(goal,candle_size)
        #indicators = Iq.get_technical_indicators(goal)
        gain = []
        losses = []
        rsi = 0
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

    
        last_index = len(inputs["close"]) -1
        actual_value = inputs["close"][last_index]
        actual_candle_size = round(inputs["close"][last_index] - inputs["open"][last_index], 5)
        ema_values = {
            'EMA200': EMA_values( inputs, 200),
            'EMA100': EMA_values( inputs, 100),
            'EMA50': EMA_values( inputs, 50),
        }
        rsi = rsi_line(inputs, 7)

        
        if(rsi >= rsi_top):
            points = points + 1
        elif(rsi <= rsi_bottom):
            points = points - 1



        if(ema_100_status == "unknown"):
            if(actual_value < ema_values['EMA100']):
                ema_100_status = "lower"
            elif(actual_value > ema_values['EMA100']):
                ema_100_status = "upper"
        elif(ema_100_status == "lower"):
            if(actual_value > ema_values['EMA100']):
                if(ema_100_upper_counter == 0):
                    ema_100_upper_active = True
        elif(ema_100_status == "upper"):
            if(actual_value < ema_values['EMA100']):
                if(ema_100_lower_counter == 0):
                    ema_100_lower_active = True

        if(ema_100_upper_counter >= ema_100_duration):
            ema_100_upper_active = False
            ema_100_upper_counter = 0
            if(actual_value < ema_values['EMA100']):
                ema_100_status = "lower"
            elif(actual_value > ema_values['EMA100']):
                ema_100_status = "upper"
        
        if(ema_100_lower_counter >= ema_100_duration):
            ema_100_lower_active = False
            ema_100_lower_counter = 0
            if(actual_value < ema_values['EMA100']):
                ema_100_status = "lower"
            elif(actual_value > ema_values['EMA100']):
                ema_100_status = "upper"

        if(ema_100_upper_active):
            points = points + 1
            ema_100_upper_counter = ema_100_upper_counter + 1
        
        if(ema_100_lower_active):
            points = points - 1
            ema_100_lower_counter = ema_100_lower_counter + 1

        if(ema_200_status == "unknown"):
            if(actual_value < ema_values['EMA200']):
                ema_200_status = "lower"
            elif(actual_value > ema_values['EMA200']):
                ema_200_status = "upper"
        elif(ema_200_status == "lower"):
            if(actual_value > ema_values['EMA200']):
                if(ema_200_upper_counter == 0):
                    ema_200_upper_active = True
        elif(ema_200_status == "upper"):
            if(actual_value < ema_values['EMA200']):
                if(ema_200_lower_counter == 0):
                    ema_200_lower_active = True

        if(ema_200_upper_counter >= ema_200_duration):
            ema_200_upper_active = False
            ema_200_upper_counter = 0
            if(actual_value < ema_values['EMA200']):
                ema_200_status = "lower"
            elif(actual_value > ema_values['EMA200']):
                ema_200_status = "upper"
        
        if(ema_200_lower_counter >= ema_200_duration):
            ema_200_lower_active = False
            ema_200_lower_counter = 0
            if(actual_value < ema_values['EMA200']):
                ema_200_status = "lower"
            elif(actual_value > ema_values['EMA200']):
                ema_200_status = "upper"

        if(ema_200_upper_active):
            points = points + 1
            ema_200_upper_counter = ema_200_upper_counter + 1
        
        if(ema_200_lower_active):
            points = points - 1
            ema_200_lower_counter = ema_200_lower_counter +1


        sequence = count_last_types(inputs)

        
        
        if(len(max_min_month["max_points"]) == 0):
            max_min_months = (max_min_values(goal, 2592000, 6, 3, actual_value))
            max_min_month = (max_min_values(goal, 86400, 30, 3, actual_value))
            max_min_day = (max_min_values(goal, 60, 1440, 3, actual_value))
        else:
            for counter in range(0, len(max_min_month["max_points"])):
                element = max_min_month["max_points"][counter]
                if(actual_value > element):
                    points = points + 2
                    max_min_month["max_points"][counter] = actual_value

            for counter in range(0, len(max_min_month["min_points"])):
                element = max_min_month["min_points"][counter]
                if(actual_value < element):
                    points = points - 2
                    max_min_month["min_points"][counter] = actual_value


        bolinger_band_7 = bolinger_band(inputs, 7, 2.4)
        bolinger_band_21 = bolinger_band(inputs, 21, 3.6)
        #actual_bolinger_band_7 = bolinger_band(inputs, 7, 2.4)
        #actual_bolinger_band_21 = bolinger_band(inputs, 21, 3.6)

        if(actual_value >= bolinger_band_7['upper']):
            points = points + 1
        elif(actual_value <= bolinger_band_7['lower']):
            points = points - 1

        if(actual_value >= bolinger_band_21['upper']):
            points = points + 1
        elif(actual_value <= bolinger_band_21['lower']):
            points = points - 1


        if(sequence['result'] >= 9):
            all_win = True
        if(sequence['result'] > 6):
            if(sequence['operation'] == "decreasing"):
                points = points + 1
            else:
                points = points - 1

      
        last_input = inputs
        print(bolinger_band_7)
        print(bolinger_band_21)
        print("rsi:", rsi)
        print(ema_values)
        print("crescimento da vela", actual_candle_size)
        print("ultimo valor:", actual_value)
    
                
        print(max_min_months)
        print(max_min_month)
        print(max_min_day)



        
        print(sequence)
        print("ema_100_status", ema_100_status)
        print("ema_200_status", ema_200_status)
        print("GOAL", goal)
        print("POINTS", points)
        print("\n")



        if(points >= 3):
            print("DESCE")
           
        elif(points <= -3):
            print("SOBE")
 
        data = [datetime.datetime.now(), points, actual_value, rsi, bolinger_band_7['lower'], bolinger_band_7['upper'], bolinger_band_21['lower'], bolinger_band_21['upper'], ema_values['EMA100'], ema_values['EMA200'],''.join(str(x) for x in max_min_months['max_points']), ''.join(str(x) for x in max_min_months['min_points']), ''.join(str(x) for x in max_min_month['max_points']), ''.join(str(x) for x in max_min_month['min_points']),''.join(str(x) for x in max_min_day['max_points']), ''.join(str(x) for x in max_min_day['min_points'])],
        #s.send(str.encode(str(actual_value)))
        writer.writerow(data)
        time.sleep(1)


