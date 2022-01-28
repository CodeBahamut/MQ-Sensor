import time
from mq_sensor import *

try:
    print("Press CTRL+C to abort")

    sensor = mq_sensor()

    while True:
        print(sensor.get_gas_strings(0))
        print(sensor.get_gas_strings(1))
        print(sensor.get_gas_strings(2))
        # print(sensor.get_gas_strings(0), sensor.get_gas_strings(1), sensor.get_gas_strings(2))

        time.sleep(0.1)


except Exception as e:
    print(e)
    print("\nAbort by user")

