import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from mpl_toolkits.mplot3d import Axes3D  # noqa




def read_and_concat(folder, pattern="*.csv"):
    """
    Read all CSV files in a folder and concatenate them into one DataFrame.
    
    Parameters
    ----------
    folder : str or Path
        Directory containing CSV files
    pattern : str
        File pattern (default: "*.csv")
    
    Returns
    -------
    pandas.DataFrame
    """
    folder = Path(folder)
    dfs = []

    for file in folder.glob(pattern):
        df = pd.read_csv(file)
        
        # Drop unnamed index column if present
        df = df.loc[:, ~df.columns.str.contains("Unnamed")]
        
        # Optional: keep track of source file
        df["source_file"] = file.name
        
        dfs.append(df)

    return pd.concat(dfs, ignore_index=True)


if __name__ == "__main__":

    data = read_and_concat("./raws")
    
    filtered = data[data["pwr"] == 20]

    sns.lineplot(data=filtered, x="vcc", y="i_tx")
    plt.title("I_tx for 20dBm")
    plt.xlabel("vcc [mV]")
    plt.ylabel("I_tx [mA]")


    plt.grid(True)
    plt.show()