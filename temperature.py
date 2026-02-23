import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D  
from scipy.stats import zscore
from file_concat import read_and_concat



def filter_zscore(g, col="t_meas", z=3, min_n=5):
    if len(g) < min_n:
        return g  # keep all measurements
    zs = zscore(g[col])
    return g[zs.abs() < z]




if __name__ == "__main__":
    data = read_and_concat("./Temperature_measurements")




    data["temp"] = (
    data["source_file"]
        .str[12:]
        .str.replace("deg", "", regex=False)
        .str.replace(".csv", "", regex=False)
    )

    filtered = data[data["i_tx"] > 10]


    filtered.to_csv("tester.csv")
    sns.lineplot(data=filtered, x="pwr", y="i_tx", hue="temp")

    plt.grid(True)
    plt.show()
