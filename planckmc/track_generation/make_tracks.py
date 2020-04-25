import numpy as np
from numba import njit
from ..config import CONFIG

@njit
def generate_tracks(vel, t_entry):
    '''Return track with entry and exit vectors in local coords (x=north, y=east, z=up), and entry & exit time.
    vel is an array of velocities. t_entry is an array of time.
    generate_tracks(vel, t_entry):
        return ((x_entry, y_entry, z_entry, time_exit), (x_exit, y_exit, z_exit, time_exit))
    '''
    radius = float(CONFIG['Track Generation']['BoundingSphereRadius'])
    return ((0, 0, 1, t_entry), (0, 1, 0, t_entry))
