import numpy as np
from numba import njit
import wimprates
import numericalunits as nu
from ..config import CONFIG

V_MAX = float(CONFIG['Track Generation']['TrackMaxVel'])
V_MIN = float(CONFIG['Track Generation']['TrackMinVel'])
V_BINS = float(CONFIG['Track Generation']['TrackVelBins'])
def vel_make_cdf():
    v_vals = np.linspace(V_MIN, V_MAX, V_BINS)
    vel_dist = wimprates.observed_speed_dist(v_vals * nu.m/nu.s)
    integrated_vel_rate = sum([x*((max(v_vals)-min(v_vals))/len(v_vals)) for x, y in zip(vel_dist, v_vals)])
    vel_pdf = np.array(vel_dist)/integrated_vel_rate
    vel_cdf = [sum(vel_pdf[:i])/sum(vel_pdf) for i in range(len(vel_pdf))]
    return v_vals, vel_cdf

@njit
def vel_calc(v_vals, vel_cdf):
    rnd_unt_num_vel = np.random.uniform()
    vel_index = np.argmin(abs(np.array(vel_cdf) - rnd_unt_num_vel))
    vel = v_vals[vel_index]
    return vel
