'''module to read detector geometry config'''
import json
import numpy as np

def _pos_vec_list(filename):
    '''internal function to read detector geometry json'''
    pos_config_file = open(filename)
    header = pos_config_file.readline()
    split_header = header.split(',')
    version = int(split_header[0].lstrip('version: '))
    sensor_num = int(split_header[1].lstrip(' sensors: '))
    lines = pos_config_file.readlines()
    serial_nums = []
    pos_vecs = []
    line_counter = 0
    pos_config_file.close()
    if version != 1:
        raise ValueError("You are running the incorrect version of the configuration file " +
                         filename + ".\nExiting.")

    for json_obj in lines:
        line_counter += 1

    if line_counter > sensor_num:
        raise ValueError("You have more sensors in your file "
                         + filename +
                         ' than you have indicated in your header!'
                         ' (Check for unintentional whitespace and newlines.)\nExiting.'
                        )

    elif line_counter < sensor_num:
        raise ValueError("You have less sensors in your file " +
                         filename +
                         ' than you have indicated in your header! '
                         '(Check for unintentional whitespace and newlines.)\nExiting.'
                        )

    for json_obj in lines:
        pos_dict = json.loads(json_obj)
        serial_nums.append(pos_dict["serial"])
        vec = np.array([pos_dict["x"], pos_dict["y"], pos_dict["z"]])
        pos_vecs.append(vec)

    return serial_nums, pos_vecs

SENSOR_GEOM = _pos_vec_list('position.json')
