import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


if __name__ == "__main__":
    with_mirror = pd.read_csv("Package with mirror, 3v3.csv")
    without_mirror = pd.read_csv("Package without mirror, 3v3.csv")


    sns.histplot(data=with_mirror, x="Current(uA)", bins=1000, label="With mirroring")
    sns.histplot(data=without_mirror, x="Current(uA)", bins=1000, label="Without mirroring")
    plt.grid(True)
    plt.legend()
    plt.show()

