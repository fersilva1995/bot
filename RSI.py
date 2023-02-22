import numpy as np
import time
from threading import Thread
from talib.abstract import *

class RSI_calc():
    def __init__(self, rsi_top, rsi_bottom, period):
        self.thread = Thread(target=self.get_points)
        self.thread.start()
        self.rsi_top = rsi_top
        self.rsi_bottom = rsi_bottom
        self.period = period
        self.points = 0
        self.inputs = []


    def get_rsi(self):
        rsi = 0
        status = False

        if(len(self.inputs) > 0):
            if(len(self.inputs["open"]) > 0):
                status = True
  
        if(status):
            rsi_adjust = 1
            rsi_inputs = {
                'open': np.array(self.inputs["open"][len(self.inputs["open"]) - (self.period+rsi_adjust):]),
                'high': np.array(self.inputs["high"][len(self.inputs["high"]) - (self.period+rsi_adjust):]),
                'low': np.array(self.inputs["low"][len(self.inputs["low"]) - (self.period+rsi_adjust):]),
                'close': np.array(self.inputs["close"][len(self.inputs["close"]) - (self.period+rsi_adjust):]),
                'volume': np.array(self.inputs["volume"][len(self.inputs["volume"]) - (self.period+rsi_adjust):])
            }
            rsi_values = RSI(rsi_inputs, timeperiod=self.period)
            rsi = rsi_values[len(rsi_values) - 1]

        return rsi, status
    
    def get_points(self):
        while True:
            rsi, status = self.get_rsi()
            print("RSI:" , round(rsi,4))
            
            if(status):
                if(rsi >= self.rsi_top):
                    self.points = self.points + 1
                elif(rsi <= self.rsi_bottom):
                    self.points = self.points - 1
            
            time.sleep(0.5)

    def set_inputs(self, inputs):
        self.inputs = inputs
