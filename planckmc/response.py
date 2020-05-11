import numpy as np

def _sensor_response(acceleration):

    delta = [1]
            
    impulse = np.convolve(acceleration,delta)

    for i in range(len(acceleration)):
        step = .01
        bin_max = .01
        acc_int = 0
        while acceleration[i] > bin_max:
            bin_max += step
            acc_int += 1
        acceleration[i] = acc_int

    return impulse, acceleration
        
