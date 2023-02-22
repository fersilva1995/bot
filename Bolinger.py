import numpy as np
import statistics
import time
from threading import Thread
from talib.abstract import *

class Bolinger_calc:
    def __init__(self, multiplicator, period):
        self.thread = Thread(target=self.get_points)
        self.thread.start()
        self.multiplicator = multiplicator
        self.period = period
        self.points = 0
        self.inputs = []
        self.bolinger_upper = 0
        self.bolinger_middle = 0
        self.bolinger_lower = 0

    def get_bolinger(self):
        bolinger = {
            'upper': 0,
            'middle': 0,
            'lower': 0
        }
        status = False

        if(len(self.inputs) > 0):
            if(len(self.inputs["open"]) > 0):
                inputs_len = len(self.inputs["open"])
                status = True
        
        if(status):
            bolinger_adjust = 1
            bolinge_inputs = {
                'open': np.array(self.inputs["open"][inputs_len - (self.period + bolinger_adjust):inputs_len - bolinger_adjust]),
                'high': np.array(self.inputs["high"][inputs_len - (self.period + bolinger_adjust):inputs_len - bolinger_adjust]),
                'low': np.array(self.inputs["low"][inputs_len - (self.period + bolinger_adjust):inputs_len - bolinger_adjust]),
                'close': np.array(self.inputs["close"][inputs_len - (self.period + bolinger_adjust):inputs_len - bolinger_adjust]),
                'volume': np.array(self.inputs["volume"][inputs_len - (self.period + bolinger_adjust):inputs_len - bolinger_adjust])
            }
            sma = SMA(bolinge_inputs, timeperiod=self.period) 
            bolinger =  {
                'upper': sma[len(sma) - 1] + ((statistics.stdev(bolinge_inputs["close"]))*self.multiplicator),
                'middle': sma[len(sma) - 1] ,
                'lower': sma[len(sma) - 1] - ((statistics.stdev(bolinge_inputs["close"]))*self.multiplicator)
            }

            self.bolinger_upper = bolinger['upper']
            self.bolinger_middle = bolinger['middle']
            self.bolinger_lower =bolinger['lower']
                    
        return bolinger, status

    def get_points(self):
        while True:
            bolinger, status = self.get_bolinger()

            if(status):
                last_index = len(self.inputs["close"]) -1
                actual_value = self.inputs["close"][last_index]
                if(actual_value >= bolinger['upper']):
                    self.points = self.points + 1
                elif(actual_value <= bolinger['lower']):
                    self.points = self.points - 1

                if(actual_value >= bolinger['upper']):
                    self.points = self.points + 1
                elif(actual_value <= bolinger['lower']):
                    self.oints = self.points - 1

            time.sleep(0.5)
    
    def set_inputs(self, inputs):
        self.inputs = inputs