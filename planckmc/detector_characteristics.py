'''module to read detector characteristics config'''
import json
import numpy as np
from .detector_geometry import _pos_vec_list
from .config import CONFIG

GEOMETRY_FILE = CONFIG['Detector Config']['GeometryFile']
CHARACTERISTICS_FILE = CONFIG['Detector Config']['CharacteristicsFile']
_VERSION = int(CONFIG['Detector Config']['Version'])

def characteristics_lists(serials, filename):
    '''internal function to read detector characteristics json'''
    characteristics_file = open(filename)

    with characteristics_file as file:
        char_dict = json.load(file)

    version = char_dict["version"]
    sensor_num = char_dict["sensors"]
    lines = len(char_dict["detectors"])
    serial_nums = []
    orientation = []
    sensitivity = []
    noise = []

    if version != _VERSION:
        raise ValueError("You are running the incorrect version of the configuration file " +
                         filename + ".\nExiting.")

    if lines > sensor_num:
        raise ValueError("You have more sensors in your file "
                         + filename +
                         ' than you have indicated in your header!'
                         ' (Check for unintentional whitespace and newlines.)\nExiting.'
                        )

    elif lines < sensor_num:
        raise ValueError("You have less sensors in your file "
                         + filename +
                         ' than you have indicated in your header!'
                         '(Check for unintentional whitespace and newlines.)\nExiting.'
                        )

    for i in range(lines):
        serial_nums.append(char_dict["detectors"][i]["serial"])
        orien_vec = np.array([char_dict["detectors"][i]["x_orien"],
                              char_dict["detectors"][i]["y_orien"],
                              char_dict["detectors"][i]["z_orien"]]
                            )
        sens_vec = np.array([char_dict["detectors"][i]["x_sens"],
                             char_dict["detectors"][i]["y_sens"],
                             char_dict["detectors"][i]["z_sens"]]
                           )
        noise_vec = np.array([char_dict["detectors"][i]["x_noise"],
                              char_dict["detectors"][i]["y_noise"],
                              char_dict["detectors"][i]["z_noise"]]
                            )
        #orientation.append(orien_vec)
        orientation.append(np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])) #Needs to be changed!!! Temporary rotation matrix that does not read from config.
        sensitivity.append(sens_vec)
        noise.append(noise_vec)

    if len(serial_nums) != len(serials):
        raise ValueError("You do not have the same number "
                         "of sensors in your configuration files.\nExiting.")

    for i, serial_num in enumerate(serial_nums):
        if serial_num != serials[i]:
            raise ValueError("Your serial numbers of detector " +
                             str(i+1) +
                             " in each configuration file are not the same.\nExiting")

    return orientation, sensitivity, noise


def generate_detectors_dict():
    '''Create dict to contain all detector configuration information.'''
    serials, pos_vecs = _pos_vec_list(GEOMETRY_FILE)
    orientation, sensitivity, noise = characteristics_lists(serials, CHARACTERISTICS_FILE)
    output_dict = {}
    for i, serial in enumerate(serials):
        output_dict[serial] = {
            'position': pos_vecs[i],
            'orientation': orientation[i],
            'sensitivity': sensitivity[i],
            'noise': noise[i],
        }
    return output_dict

DETECTOR_CHARACTERISTICS = generate_detectors_dict()
