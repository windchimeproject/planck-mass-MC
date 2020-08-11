#!usr/bin/env python3
'''script generate a linear response json. Meant to be a simple way to get MC up and running;
not to emulate a real experiment!'''

import argparse
import json

import numpy as np
from planckmc.detector_characteristics import DETECTOR_CHARACTERISTICS

#test

def output_response_json(file, bits, min_acceleration, max_acceleration):
    '''generate response json'''
    bin_borders = list(np.linspace(min_acceleration, max_acceleration, 2**bits-1, endpoint=True))
    output_dict = {}
    for sensor in DETECTOR_CHARACTERISTICS:
        output_dict[sensor] = {'linear_response': [1], 'signal_transfer_response': bin_borders}
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
