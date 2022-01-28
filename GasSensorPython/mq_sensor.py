#Author: Abdelrahman El-Khenizy

import time
import math
from MCP3008 import MCP3008

class mq_sensor():

    mq_sensor_pin = 0 # The pin of the adc that is used for reading.
    resistance_value = 5 # Resistance of the board itself
    clean_air_resistance = 9.8 # Resistance in clean air
    milliseconds_to_seconds = 1000 # Variable with number of ms in s
    calibration_samples = 100 # Amount of calibration samples
    calibration_intervals = 250 # Time between samples in milliseconds
    sensor_samples = 5 # Amount of samples which the avg of is shown
    sensor_sample_interval = 50 # Time between samples in milliseconds
    Ro = 0 # Variable for Ro
    # This would equate to an update every 250ms so 4 times a second.

    #Constant id numbers for different gases
    #Some gas values can represent two gases since the values are not accurate
    #enough to measure the gases with similar values.
    CO = 0 # Carbon monoxide (Bad to breathe)
    smoke = 1 # Smoke (Bad to breathe) & ~methane & ~alcohol
    LPG = 2 # Liquefied petroleum gas (Flammable) & ~propane

    #Lists for the curves of the resistances in the graph
    #The first and second values are the X and Y of the first value in the graph
    #the third value represents the curve.
    CO_curve = [2.3, 0.72, -0.34]
    smoke_curve = [2.3, 0.53, -0.44]
    LPG_curve = [2.3, 0.21, -0.47]

    def __init__(self):
        self.adc = MCP3008()
        print("Calibrating...")
        self.Ro = self.sensor_calibration()
        print("Calibration is done...\n")

    # Calculates/reads the resistance of the sensor to be used later to find the value the sensor is giving.
    # The 1023 stand for the value given with 10 bits of data. It forms a voltage divider so what is calculated
    # is the percentage of resistance of the base resistance.
    def get_sensor_resistance(self, analog_input):
        resistance = float(self.resistance_value * (1023 - analog_input) / analog_input)
        return resistance

    # Calibration code for the sensor, Gives the Ro value from the graphs.
    # Takes 100 samples with an interval of 250 milli seconds and then calculates the average.

    def sensor_calibration(self):
        value = 0

        #Take 100 samples
        for i in range(self.calibration_samples):
            value += self.get_sensor_resistance(self.adc.read(self.mq_sensor_pin))
            time.sleep(self.calibration_intervals / self.milliseconds_to_seconds)

        #Calculate the average and divide by the resistance in clean air to get a base value
        value = value / self.calibration_samples
        value = value / self.clean_air_resistance

        return value

    # Gives the rs value which is the resistance of the sensor at the time of invoking the method.
    def read_rs_value(self):
        rs = 0

        # Take 5 samples
        for i in range(self.sensor_samples):
            rs += self.get_sensor_resistance(self.adc.read(self.mq_sensor_pin))
            time.sleep(self.sensor_sample_interval / self.milliseconds_to_seconds)

        # Calculate the average
        rs = rs / self.sensor_samples

        return rs

    # This calculates the ppm per gas by using the values from the graph.
    # Curve[1] stands for the y axis (Rs/Ro)in the graph, curve[2] stands for the curve of the graph and
    # curve[0] stand for the x axis (ppm).
    # The values are turned back to log values to correspond with the graph.
    def calculate_ppm_gas(self, gas_curve):
        ppm = math.pow(10, (((math.log(self.read_rs_value()) - gas_curve[1]) / gas_curve[2]) + gas_curve[0]))
        return ppm

    # Gives the ppm using the previous method depending on the gas id/number given.
    def get_ppm(self, gas_number):
        if (gas_number == self.CO):
            return self.calculate_ppm_gas(self.CO_curve)
        elif (gas_number == self.smoke):
            return self.calculate_ppm_gas(self.smoke_curve)
        elif (gas_number == self.LPG_curve):
            return self.calculate_ppm_gas(self.LPG_curve)
        else:
            return 0

    # Method to return ppm + strings with gas names.
    def get_gas_strings(self, gas_number):
        if (gas_number == self.CO):
            return ("CO: ", self.calculate_ppm_gas(self.CO_curve))
        elif (gas_number == self.smoke):
            return ("Smoke: ", self.calculate_ppm_gas(self.smoke_curve))
        elif (gas_number == self.LPG_curve):
            return ("LPG: ", self.calculate_ppm_gas(self.LPG_curve))
        else:
            return 0
