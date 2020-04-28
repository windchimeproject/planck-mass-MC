#!usr/local/bin/python2
import os, json, sys
import numpy as np

def detector_characteristics():
    characteristics_file = open(sys.argv[-1])
    lines = characteristics_file.readlines()
    sensor_num = int(sys.argv[-2])
    orientation = []
    sensitivity = []
    noise = []
    line_counter = 0

    for json_obj in lines:
        line_counter += 1
            
    if line_counter > sensor_num:
        raise ValueError("You have more sensors in your file than you have indicated for this program! (Check for unintentional whitespace.)\nExiting.")
        
    elif line_counter < sensor_num:
        raise ValueError("You have less sensors in your file than you have indicated for this program! (Check for unintentional whitespace.)\nExiting.")

    for json_obj in lines:
        char_dict = json.loads(json_obj)
        orien_vec = np.array([char_dict["x_orien"], char_dict["y_orien"], char_dict["z_orien"]])
        sens_vec = np.array([char_dict["x_sens"], char_dict["y_sens"], char_dict["z_sens"]])
        noise_vec = np.array([char_dict["x_noise"], char_dict["y_noise"], char_dict["z_noise"]])
        orientation.append(orien_vec)
        sensitivity.append(sens_vec)
        noise.append(noise_vec)

    print orientation
    print sensitivity
    print noise

detector_characteristics()
