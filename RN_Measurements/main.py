

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit
import numpy.typing as npt




def parse_measurements() -> list[pd.DataFrame]:
    results = []
    for i in range(1, 11):
        df = pd.read_csv(f"./raw/click{i}_3300.0.csv")
        df["pwr_lin"] = 10**(df["pwr"]/10) #Konverterer til milliwatts
        results.append(df)

    return results




def model(pwr_lin: npt.NDArray[np.floating], a: float, b: float, c: float, I_Q: float) -> float:
    return a*pwr_lin**3 + b*pwr_lin**2 + c*pwr_lin + I_Q





if __name__ == "__main__":
    results = parse_measurements()
    results_concatted = pd.DataFrame()
    for result in results:
        results_concatted = pd.concat([results_concatted, result], ignore_index=True)

    params, _ = curve_fit(model, results_concatted["pwr_lin"], results_concatted["i_tx"])
    #sns.lineplot(x=results_concatted["pwr_lin"],y=results_concatted["i_tx"], estimator="mean", errorbar=("sd", 2))
    
    points = np.linspace(0.01, 35, 100)
    
    pwr_lin =results_concatted["pwr_lin"].unique()
    pwr_mean = np.empty(len(pwr_lin))

    for i, pwr in enumerate(pwr_lin):
        pwr_mean[i] = np.mean(results_concatted["i_tx"][results_concatted["pwr_lin"] == pwr])
    
    mean_dict = dict(zip(pwr_lin, pwr_mean))
    for result in results:
        result["residuals"] = (
            result["i_tx"]
            - result["pwr_lin"].map(mean_dict)
        )
    

    #plt.scatter(pwr_lin, pwr_mean, color = "red")
#
    #for i, result in enumerate(results):
    #    nice_x = result["pwr_lin"] + np.random.normal(0, 0.08, len(result["pwr_lin"]))
#
    #    plt.scatter(nice_x, result["i_tx"], marker=".", s=1, label=f"click{i}")
    
    plt.grid(True)
    for i, result in enumerate(results):
        #sns.histplot(result["residuals"], label=f"click{i}", bins=50)
        sns.histplot(
        result["residuals"],
        label=f"click{i}",
        bins=50,
        kde=True,
        stat="density",   # important for proper KDE scaling
        element="step",   # cleaner when overlapping
        fill=True,        # optional: avoid solid blocks
        alpha=0.05,
        )
    
    plt.xlabel("difference in mA")
    plt.legend()
    plt.tight_layout()
    plt.grid("true")
    plt.legend()
    plt.show()