#!usr/bin/env python3
import json
import numpy as np

def characteristics_lists(serials, filename):
    characteristics_file = open(filename)
    header = characteristics_file.readline()
    split_header = header.split(',')
    version = int(split_header[0].lstrip('version: '))
    sensor_num = int(split_header[1].lstrip(' sensors: '))
    lines = characteristics_file.readlines()
    serial_nums = []
    orientation = []
    sensitivity = []
    noise = []
    line_counter = 0

    if version != 1:
        raise ValueError("You are running the incorrect version of the configuration file " + filename +".\nExiting.")
    
    for json_obj in lines:
        line_counter += 1
            
    if line_counter > sensor_num:
        print("File name: " + filename)
        raise ValueError("You have more sensors in your file " + filename + " than you have indicated in your header! (Check for unintentional whitespace and newlines.)\nExiting.")
        
    elif line_counter < sensor_num:
        print("File name: " + filename)
        raise ValueError("You have less sensors in your file " + filename + " than you have indicated in your header! (Check for unintentional whitespace and newlines.)\nExiting.")

    for json_obj in lines:
        char_dict = json.loads(json_obj)
        serial_nums.append(char_dict["serial"])
        orien_vec = np.array([char_dict["x_orien"], char_dict["y_orien"], char_dict["z_orien"]])
        sens_vec = np.array([char_dict["x_sens"], char_dict["y_sens"], char_dict["z_sens"]])
        noise_vec = np.array([char_dict["x_noise"], char_dict["y_noise"], char_dict["z_noise"]])
        orientation.append(orien_vec)
        sensitivity.append(sens_vec)
        noise.append(noise_vec)

    if len(serial_nums) != len(serials):
        raise ValueError("You do not have the same number of sensors in your configuration files.\nExiting.")

    for i in range(len(serial_nums)):
        if serial_nums[i] != serials[i]:
            raise ValueError("Your serial numbers on line " + str(i+2) + " in each configuration file are not the same.\nExiting")

    return orientation, sensitivity, noise


