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

def FIR_filter_Lin_Tri(desired_len, max_val):
    #len actually is: desired_len plus 1 if it is even, exactly equal to desired_len if it is odd

    side_sum = (1 + max_val) / 2
    constant = side_sum / max_val
    num_of_vals = round(2 * constant)

    init_array = np.linspace(0, max_val, num_of_vals)[0:-1]
    end_array = np.linspace(max_val, 0, num_of_vals)[1:]
    dum_side_array = np.zeros(int((desired_len - (len(init_array) + len(end_array))) / 2))
    arr_lin_resp = np.concatenate((dum_side_array, init_array, [max_val], end_array, dum_side_array))
    return arr_lin_resp

def FIR_filter_Gauss(centr_gauss, sigma_gauss, desired_len):
    x_guass = np.linspace(-sigma_gauss * 4, sigma_gauss * 4, desired_len)
    arr_lin_resp_long_gauss = (2 * np.pi * sigma_gauss ** 2) ** -.5 * np.exp(
        -.5 * (x_guass - centr_gauss) ** 2 / sigma_gauss ** 2)

    arr_lin_resp_gauss = arr_lin_resp_long_gauss / np.linalg.norm(arr_lin_resp_long_gauss, ord=1)
    return arr_lin_resp_gauss

def output_response_json(file, bits, min_acceleration, max_acceleration, desired_len = 801, max_val = 0.5, centr_gauss = 0, sigma_gauss = 0.25, Resp = 'FIR_filter'):
    '''generate response json'''
    bin_borders = list(np.linspace(min_acceleration, max_acceleration, 2**bits-1, endpoint=True))
    output_dict = {}
    if Resp == 'FIR_filter':
        Lin_Resp = list(FIR_filter())
    elif Resp == 'Tri_filter':
        Lin_Resp = list(FIR_filter_Lin_Tri(desired_len, max_val))
    elif Resp == 'Gauss_filter':
        Lin_Resp = list(FIR_filter_Gauss(centr_gauss, sigma_gauss, desired_len))

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
