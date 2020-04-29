#!usr/bin/env python3
import sys
import detector_geometry as dg
import detector_characteristics as dc

pos_filename = sys.argv[-2]
char_filename = sys.argv[-1]
serials, positions = dg.pos_vec_list(pos_filename)
print(serials)
print(positions)

ort, sens, noise = dc.characteristics_lists(serials, char_filename)
print(ort)
print(sens)
print(noise)
