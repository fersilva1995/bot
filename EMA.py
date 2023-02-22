import time
import numpy as np
from talib.abstract import *
from threading import Thread

class EMA_calc:
    def __init__(self, ema_duration, period):
        self.thread = Thread(target=self.get_points)
        self.thread.start()
        self.ema_duration = ema_duration
        self.period = period
        self.ema_lower_counter = 0
        self.ema_upper_counter = 0
        self.ema_lower_active = False
        self.ema_upper_active = False
        self.ema_status = "unknown"
        self.points = 0
        self.inputs = []
        self.ema = 0

    def get_ema(self):
        ema = 0
        status = False

        if(len(self.inputs) > 0):
            if(len(self.inputs["open"]) > 0):
                inputs_len = len(self.inputs["open"])
                status = True
        
        if(status):
            ema_adjust = 0
            ema_inputs = {
                'open': np.array(self.inputs["open"][inputs_len - (self.period + ema_adjust):inputs_len - ema_adjust]),
                'high': np.array(self.inputs["high"][inputs_len - (self.period + ema_adjust):inputs_len - ema_adjust]),
                'low': np.array(self.inputs["low"][inputs_len - (self.period + ema_adjust):inputs_len - ema_adjust]),
                'close': np.array(self.inputs["close"][inputs_len - (self.period + ema_adjust):inputs_len - ema_adjust]),
                'volume': np.array(self.inputs["volume"][inputs_len - (self.period + ema_adjust):inputs_len - ema_adjust])
            }

            ema_values = EMA(ema_inputs, self.period)
            ema = ema_values[len(ema_values)-1]
            self.ema = ema

        return ema, status

    def get_points(self):
        while True:
            ema, status = self.get_ema()

            if(status):      
                last_index = len(self.inputs["close"]) -1
                actual_value = self.inputs["close"][last_index]
                if(self.ema_status == "unknown"):
                    self.ema_status = "lower" if actual_value < ema else "upper"

                if(self.ema_status == "lower" and actual_value > ema and self.ema_upper_counter == 0):
                    self.ema_upper_active = True
                        
                if(self.ema_status == "upper" and actual_value < ema and self.ema_lower_counter == 0):
                    self.ema_lower_active = True

                if(self.ema_upper_active):
                    self.points = self.points + 1
                    self.ema_upper_counter = self.ema_upper_counter + 1
                
                if(self.ema_lower_active):
                    self.points = self.points - 1
                    self.ema_lower_counter = self.ema_lower_counter + 1
                        
                if(self.ema_upper_counter >= self.ema_duration):
                    self.ema_upper_active = False
                    self.ema_upper_counter = 0
                    self.ema_status = "lower" if actual_value < ema else "upper"
                
                if(self.ema_lower_counter >= self.ema_duration):
                    self.ema_lower_active = False
                    self.ema_lower_counter = 0
                    self.ema_status = "lower" if actual_value < ema else "upper"

            time.sleep(0.5)

    def set_inputs(self, inputs):
        self.inputs = inputs






