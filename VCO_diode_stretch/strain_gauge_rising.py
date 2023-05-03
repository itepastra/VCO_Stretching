import os
import helpers
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def MakeStretchGraph(dataframe):
    fig, ax = plt.subplots(1,1, figsize=(8,6))
    numLines = dataframe["stretchAmt"].nunique()

    ax.set_xlabel(f"Strain (%)")
    ax.set_ylabel(f"Resistance (Ω)")
    ax.set_prop_cycle(helpers.MkCycle(numLines))

    groups = dataframe.groupby("stretchAmt")
    strain_1_avg = groups["strain_1"].mean()
    strain_2_avg = groups["strain_2"].mean()
    strain_3_avg = groups["strain_3"].mean()
    strain_1_std = groups["strain_1"].std()
    strain_2_std = groups["strain_2"].std()
    strain_3_std = groups["strain_3"].std()

    # for lab, df in dataframe.groupby("stretchAmt"):
    #     label = f"{(lab/L0 * 100):.3f}% {RelativeToRadius(lab/L0) * 1000:.2f} mm"
    #     ax.errorbar(df["Vctrl"], df["Freq2"]/1e6, yerr=df["errFreq2"]/1e6, capsize=None, lw=1, label=label)

    ax.errorbar(strain_1_avg.index / L0 * 100, strain_1_avg.values, yerr=strain_1_std.values, label="strain 1")
    ax.errorbar(strain_2_avg.index / L0 * 100, strain_2_avg.values, yerr=strain_2_std.values, label="strain 2")
    ax.errorbar(strain_3_avg.index / L0 * 100, strain_3_avg.values, yerr=strain_3_std.values, label="strain 3")

    ax.grid()
    ax.legend()
    fig.tight_layout()
    return fig

if __name__ == "__main__":

    L0 = 0.1001
    meas = "meas_3"

    angle = input("please give the whole part of the angle to plot. ")
    df = helpers.importCSV(f"./data/{meas}/rising/angle_{angle}.0.csv")
    if not os.path.exists(f'./figures/{meas}/'):
        os.makedirs(f'./figures/{meas}/')

    if not os.path.exists(f'./figures/{meas}/{angle}/'):
        os.makedirs(f'./figures/{meas}/{angle}/')
    # print(df)
    fig = MakeStretchGraph(df)
    fig.savefig(f"./figures/{meas}/{angle}/strainGauges.png", dpi=500)

    plt.show()