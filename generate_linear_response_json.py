#!usr/bin/env python3
'''script generate a linear response json. Meant to be a simple way to get MC up and running;
not to emulate a real experiment!'''

import argparse
import json

import numpy as np
from scipy.signal import kaiserord, firwin
from planckmc.config import CONFIG
from planckmc.detector_characteristics import DETECTOR_CHARACTERISTICS

def FIR_filter(sample_rate = 1 / (float(CONFIG['Track Generation']['Timestep']) * 10**(-9)), ripple_db = 20.0, cutoff_hz = 50000):
    nyq_rate = sample_rate / 2.0
    width = 10000.0/nyq_rate
    N, beta = kaiserord(ripple_db, width)
    taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
    return taps

def output_response_json(file, bits, min_acceleration, max_acceleration):
    '''generate response json'''
    bin_borders = list(np.linspace(min_acceleration, max_acceleration, 2**bits-1, endpoint=True))
    output_dict = {}
    Lin_Resp = list(FIR_filter())
    for sensor in DETECTOR_CHARACTERISTICS:
        output_dict[sensor] = {'linear_response': Lin_Resp, 'signal_transfer_response': bin_borders}
    json.dump(output_dict, file)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='script generate a linear response json. '
                                     'Meant to be a simple way to get MC up and running, '
                                     'not to emulate a real experiment!')
    PARSER.add_argument('output', type=str)
    PARSER.add_argument('bits', type=int)
    PARSER.add_argument('min_acceleration', type=float)
    PARSER.add_argument('max_acceleration', type=float)
    ARGS = PARSER.parse_args()
    with open(ARGS.output, 'w') as f:
        output_response_json(f, ARGS.bits, ARGS.min_acceleration, ARGS.max_acceleration)
