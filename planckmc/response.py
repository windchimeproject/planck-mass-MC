import numpy as np

def _sensor_response(acceleration):

    delta = []

    for i in range(len(acceleration)):
        delta.append(1)

    impulse = np.convolve(acceleration,delta)

    return impulse
        
