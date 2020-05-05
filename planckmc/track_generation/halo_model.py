'''Module for random velocity generation based on SHM.
Excepted to be upgraded to generate vectors eventually!
'''
import numpy as np
from numba import njit
import wimprates
import numericalunits as nu
from ..config import CONFIG

V_MAX = float(CONFIG['Track Generation']['TrackMaxVel'])
V_MIN = float(CONFIG['Track Generation']['TrackMinVel'])
V_BINS = float(CONFIG['Track Generation']['TrackVelBins'])
def _vel_make_cdf():
    '''Generates velocity cdf. Internal function.'''
    v_vals = np.linspace(V_MIN, V_MAX, V_BINS)
    vel_dist = wimprates.observed_speed_dist(v_vals * nu.m/nu.s)
    integrated_vel_rate = sum([x*((max(v_vals)-min(v_vals))
                                  /len(v_vals)) for x, y in zip(vel_dist, v_vals)])
    vel_pdf = np.array(vel_dist)/integrated_vel_rate
    vel_cdf = [sum(vel_pdf[:i])/sum(vel_pdf) for i in range(len(vel_pdf))]
    return v_vals, np.array(vel_cdf)

V_VALS, VEL_CDF = _vel_make_cdf()

@njit
def vel_calc(v_vals=V_VALS, vel_cdf=VEL_CDF):
    '''Generate random velocity.'''
    rnd_unt_num_vel = np.random.rand()
    vel_index = np.argmin(np.abs(vel_cdf - rnd_unt_num_vel))
    vel = v_vals[vel_index]
    return vel

@njit
def generate_vel_array(n=1):
    '''Generate random velocities.'''
    return np.array([vel_calc() for _ in range(n)])