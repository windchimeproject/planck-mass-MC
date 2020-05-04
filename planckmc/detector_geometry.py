'''module to read detector geometry config'''
import json, sys
import numpy as np

def _pos_vec_list(filename):
    '''internal function to read detector geometry json'''
    pos_config_file = open(filename)

    with pos_config_file as f:
        pos_dict = json.load(f)
        
    version = pos_dict["version"]
    sensor_num = pos_dict["sensors"]
    lines = len(pos_dict["detectors"])
    serial_nums = []
    pos_vecs = []
    
    if version != 1:
        raise ValueError("You are running the incorrect version of the configuration file " +
                         filename + ".\nExiting.")

    if lines > sensor_num:
        raise ValueError("You have more sensors in your file "
                         + filename +
                         ' than you have indicated in your header!'
                         ' (Check for unintentional whitespace and newlines.)\nExiting.'
                        )

    elif lines < sensor_num:
        raise ValueError("You have less sensors in your file " +
                         filename +
                         ' than you have indicated in your header! '
                         '(Check for unintentional whitespace and newlines.)\nExiting.'
                        )

    for i in range(lines):
        serial_nums.append(pos_dict["detectors"][i]["serial"])
        vec = np.array([pos_dict["detectors"][i]["x"],
                        pos_dict["detectors"][i]["y"],
                        pos_dict["detectors"][i]["z"]]
                      )
        pos_vecs.append(vec)

    return serial_nums, pos_vecs

SENSOR_GEOM = _pos_vec_list('position.json')
