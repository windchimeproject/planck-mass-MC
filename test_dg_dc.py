#!usr/bin/env python3
import sys
import planckmc.detector_geometry as dg
import planckmc.detector_characteristics as dc

pos_filename = sys.argv[-2]
char_filename = sys.argv[-1]
serials, positions = dg._pos_vec_list(pos_filename)
print(serials)
print(positions)

ort, sens, noise = dc.characteristics_lists(serials, char_filename)
print(ort)
print(sens)
print(noise)
