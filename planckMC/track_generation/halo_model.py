import numpy as np
from numba import njit
import wimprates
import numericalunits as nu

def Vel_makeCDF():
    v_Vals = np.linspace(0,1000000,1000)
    Vel_Dist = wimprates.observed_speed_dist(v_Vals * nu.m/nu.s)
    
    integrated_Vel_rate = sum([x*((max(v_Vals)-min(v_Vals))/len(v_Vals)) for x,y in zip(Vel_Dist,v_Vals)])
    vel_PDF = np.array(Vel_Dist)/integrated_Vel_rate
    vel_CDF = [sum(vel_PDF[:i])/sum(vel_PDF) for i in range(len(vel_PDF))]
    return v_Vals, vel_CDF

def Vel_Calc(v_Vals,vel_CDF):
    
    rndUntNum_Vel = np.random.uniform()
    Vel_index = np.argmin(abs(np.array(vel_CDF) - rndUntNum_Vel))
    Vel = v_Vals[Vel_index]
    
    return Vel

