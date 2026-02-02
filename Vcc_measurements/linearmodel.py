from main import read_and_concat
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import optimize






###Lets fit a model to this
###power in milliwatts
###Resistance in oohm
###CUrrent in mA
def model(P, R, I_q):
    # I = SQRT(P/R) + I_q
    return np.sqrt(np.divide(P,R))+I_q


# Takes
# I current vector in mA
# P power in mW
def fitcurve(I, P):
    return optimize.curve_fit(model, P, I)


    

if __name__ == "__main__":
    raws = read_and_concat("./raws")
    vcc_3v3 = raws[raws["vcc"] == 3300.0]
    vcc_3v3["pwr_lin"]  = np.power(10, (vcc_3v3["pwr"])/10) * 0.001

    params, _ = fitcurve(vcc_3v3["i_tx"], vcc_3v3["pwr_lin"])
    pwr_test = np.linspace(0, 0.1, 100)
    modelled = model(pwr_test, params[0], params[1])
    
    
    print(params)

    sns.lineplot(data=vcc_3v3, x="pwr_lin", y="i_tx") 
    sns.lineplot(x=pwr_test, y=modelled)
    plt.grid(True)
    plt.show()