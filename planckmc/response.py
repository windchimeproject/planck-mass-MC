'''detector response module.'''
import json

import numpy as np
from scipy import signal

from .config import CONFIG

RESPONSE_FILE = CONFIG['Detector Config']['ResponseFile']

with open(RESPONSE_FILE) as f:
    RESPONSE_DICT = json.load(f)


def sensor_response(sensor, acceleration, response_dict=RESPONSE_DICT):
    '''returns ADC value based on true MC acceleration'''
    linear_response = response_dict[sensor]['linear_response']
    convolved_list = []
    for dim in range(acceleration.shape[1]):
        convolved_list.append(signal.convolve(acceleration[:, dim], linear_response))
    convolved_signal = np.array(convolved_list).T

    signal_transfer_response = response_dict[sensor]['signal_transfer_response']
    output_signal = np.searchsorted(signal_transfer_response, convolved_signal)

    return output_signal
