'''Module for generation of tracks.'''
import numpy as np
from numba import njit
from ..config import CONFIG
from ..track_generation.halo_model import vel_calc

RADIUS = float(CONFIG['Track Generation']['BoundingSphereRadius'])

def sample_spherical(ndim=3, n=1):
    '''pick a random point on a unit sphere'''
    vec = np.random.randn(ndim, n) 
    vec /= np.linalg.norm(vec, axis=0)
    return vec

def generate_tracks(vel, t_entry, radius=RADIUS,):
    '''Return tracks with entry and exit vectors in local coords (x=north, y=east, z=up), and entry & exit time.
    vel is an array of velocities. t_entry is an array of time.
    generate_tracks(vel, t_entry):
    '''
    n = len(vel)
    if len(vel) != len(t_entry):
        raise ValueError('vel and t_entry array lengths not equal!')
    entry_vecs = sample_spherical(n=n)
    exit_vecs = sample_spherical(n=n)
    lengths = np.linalg.norm(entry_vecs-exit_vecs, axis=0)
    t_exit = lengths/vel
    return entry_vecs, exit_vecs, t_entry, t_exit
