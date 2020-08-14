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

def FIR_filter_Lin_Tri(desired_len = 100, max_val = 0.45):
    #len actually is: desired_len plus 1 if it is even, exactly equal to desired_len if it is odd

    dum_init = np.linspace(0, max_val, int((desired_len - 2) / 2))
    dum_fin = np.linspace(max_val, 0, int((desired_len - 2) / 2))
    actl_max = [((max_val / (int(desired_len - 2) / 2))) + max_val]

    if len(dum_init) + len(dum_fin) != desired_len:
        side_pad_FIR = int((desired_len - (len(dum_init) + len(dum_fin))) / 2)
        init_array, fin_array = np.zeros(side_pad_FIR), np.zeros(side_pad_FIR)
        arr_lin_resp_long = np.concatenate((init_array, dum_init, actl_max, dum_fin, fin_array))
        arr_lin_resp = arr_lin_resp_long / np.linalg.norm(arr_lin_resp_long, ord=1)
    return arr_lin_resp

def FIR_filter_Gauss(centr_gauss = 0, sigma_gauss = 0.25, desired_len_guass = 100):
    x_guass = np.linspace(-sigma_gauss * 4, sigma_gauss * 4, desired_len_guass)
    arr_lin_resp_long_gauss = (2 * np.pi * sigma_gauss ** 2) ** -.5 * np.exp(
        -.5 * (x_guass - centr_gauss) ** 2 / sigma_gauss ** 2)

    arr_lin_resp_gauss = arr_lin_resp_long_gauss / np.linalg.norm(arr_lin_resp_long_gauss, ord=1)
    return arr_lin_resp_gauss

def output_response_json(file, bits, min_acceleration, max_acceleration, Resp = 'FIR_filter'):
    '''generate response json'''
    bin_borders = list(np.linspace(min_acceleration, max_acceleration, 2**bits-1, endpoint=True))
    output_dict = {}
    if Resp == 'FIR_filter':
        Lin_Resp = list(FIR_filter())
    else if Resp == 'Tri_filter':
        Lin_Resp = list(FIR_filter_Lin_Tri())
    else if Resp == 'Gauss_filter':
        Lin_Resp = list(FIR_filter_Gauss)
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
