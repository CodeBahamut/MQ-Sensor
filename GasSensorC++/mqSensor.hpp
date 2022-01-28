//
// @Author Abdelrahman El-Khenizy
//
#include <iostream>
#include <unistd.h>
#include <cmath>
#include <string>

#ifndef ULTRASOON_CPP_MQSENSOR_HPP
#define ULTRASOON_CPP_MQSENSOR_HPP


class mqSensor {

    //Constants:
    const int MQ_SENSOR_PIN = 0; // The pin of the adc that is used for reading.
    const int RESISTANCE_VALUE = 5; // Resistance of the board itself
    const double CLEAN_AIR_RESISTANCE = 9.8; // Resistance in clean air
    const int MILLISECONDS_TO_SECONDS = 1000; // Variable with number of ms in s
    const int CALIBRATION_SAMPLES = 100; // Amount of calibration samples
    const int CALIBRATION_INTERVAL = 250; // Time between samples in milliseconds
    const int SENSOR_SAMPLES = 5; // Amount of samples which the avg of is shown
    const int SENSOR_SAMPLE_INTERVAL = 50; // Time between samples in milliseconds
    // This would equate to an update every 250ms so 4 times a second.

    //Constant numbers for different gases
    //Some gas values can represent two gases since the values are not accurate
    //enough to measure the gases with similar values.
    const int CO = 0; // Carbon monoxide (Bad to breathe)
    const int SMOKE = 1; // Smoke (Bad to breathe) & ~methane & ~alcohol
    const int LPG = 2; // Liquefied petroleum gas (Flammable) & ~propane


    //Arrays for the curves of the resistances in the graph
    //The first and second values are the X and Y of the first value in the graph
    //the third value represents the curve.
    const float CO_CURVE[3] = {2.3,0.72, -0.34};
    const float SMOKE_CURVE[3] = {2.3, 0.53, -0.44};
    const float LPG_CURVE[3] = {2.3, 0.21, -0.47};
    float Ro;

    mqSensor() {


    }

    //Calculates/reads the resistance of the sensor to be used later to find the value the sensor is giving.
    //The 1023 stand for the value given with 10 bits of data. It forms a voltage divider so what is calculated
    //is the percentage of resistance of the base resistance.
    float getSensorResistance(int analogInput){
        float resistance = float((1023 - analogInput) / analogInput * RESISTANCE_VALUE);
        return resistance;
    }


    //Calibration code for the sensor, Gives the Ro value from the graphs.
    //Takes 100 samples with an interval of 250 milli seconds and then calculates the average.
    float sensorCalibration(){
        float value;

        //Take 100 samples
        for (int i = 0; i < CALIBRATION_SAMPLES; ++i) {
            value += getSensorResistance(adc.read(mqSensorPin)); // todo adc
            sleep(CALIBRATION_INTERVAL / MILLISECONDS_TO_SECONDS);
        }
        //Calculate the average and divide by the resistance in clean air to get a base value
        value = value / CALIBRATION_SAMPLES;
        value = value / CLEAN_AIR_RESISTANCE;

        return value;
    }

    // Gives the rs value which is the resistance of the sensor at the time of invoking the method.
    float readRsValue(){
        float rs;

        for (int i = 0; i < SENSOR_SAMPLES; ++i) {
            rs += getSensorResistance(adc.read(MQ_SENSOR_PIN)); //todo adc
            sleep(SENSOR_SAMPLE_INTERVAL / MILLISECONDS_TO_SECONDS);
        }
        rs = rs / SENSOR_SAMPLES;
        return rs;
    }

    // This calculates the ppm per gas by using the values from the graph.
    // Curve[1] stands for the y-axis (Rs/Ro)in the graph, curve[2] stands for the curve of the graph and
    // curve[0] stand for the x-axis (ppm).
    // The values are turned back to log values to correspond with the graph.
    float calculatePpmGas(float gasCurve[]){
        float ppm = pow(10 (((log(readRsValue()) - gasCurve[1]) / gasCurve[2]) + gasCurve[0]));
        return ppm;
    }

    // Gives the ppm using the previous method depending on the gas id/number given.
    float getPpm(int gasNumber){
        if(gasNumber == CO){
            return calculatePpmGas(CO_CURVE);
        } else if(gasNumber == SMOKE){
            return calculatePpmGas(SMOKE_CURVE);
        } else if(gasNumber == LPG){
            return calculatePpmGas(LPG_CURVE);
        } else
            return 0.0;
    }

    // Method to return ppm + strings with gas names. todo
//    string getPpm(int gasNumber){
//        if(gasNumber == CO){
//            return calculatePpmGas(CO_CURVE);
//        } else if(gasNumber == SMOKE){
//            return calculatePpmGas(SMOKE_CURVE);
//        } else if(gasNumber == LPG){
//            return calculatePpmGas(LPG_CURVE);
//        } else
//            return 0.0;
//    }
};


#endif //ULTRASOON_CPP_MQSENSOR_HPP
