#!usr/local/bin/python2
import os, json, sys
import numpy as np

def pos_vec_list():
    pos_config_file = open(sys.argv[-1])
    lines = pos_config_file.readlines()
    sensor_num = int(sys.argv[-2])
    serial_nums = []
    pos_vecs = []
    line_counter = 0

    for json_obj in lines:
        line_counter += 1
            
    if line_counter > sensor_num:
        sys.exit("You have more sensors in your file than you have indicated for this program!\nExiting. (Check for unintentional whitespace.)\n")
        
    elif line_counter < sensor_num:
        sys.exit("You have less sensors in your file than you have indicated for this program!\nExiting. (Check for unintentional whitespace.)\n")

    for json_obj in lines:
        pos_dict = json.loads(json_obj)
        serial_nums.append(pos_dict["serial"])
        vec = np.array([pos_dict["x"], pos_dict["y"], pos_dict["z"]])
        pos_vecs.append(vec)

    return serial_nums, pos_vecs
    

pos_vec_list()
    
