import numpy as np

def _sensor_response(acceleration):

    delta = [1]

    for i in range(len(acceleration)):
        if acceleration[i] in range(.02):
            acceleration[i]=0
        elif acceleration[i] in range(.01,.03):
            acceleration[i]=1
        elif acceleration[i] in range(.02,.04):
            acceleration[i]=2
        elif acceleration[i] in range(.03,.05):
            acceleration[i]=3
        elif acceleration[i] in range(.04,.06):
            acceleration[i]=4
        elif acceleration[i] in range(.05,.07):
            acceleration[i]=5
        elif acceleration[i] in range(.06,.08):
            acceleration[i]=6
        elif acceleration[i] in range(.07,.09):
            acceleration[i]=7
        elif acceleration[i] in range(.08,.10):
            acceleration[i]=8
        elif acceleration[i] in range(.09,.11):
            acceleration[i]=9
        elif acceleration[i] in range(.10,.12):
            acceleration[i]=10
            
    impulse = np.convolve(acceleration,delta)

    return impulse
        
