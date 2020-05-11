#!/usr/bin/python3
import planckmc.response as response

acceleration = [0,.1,.02,.05,.01,.15]
impulse, table = response._sensor_response(acceleration)
print(impulse)
print(table)
