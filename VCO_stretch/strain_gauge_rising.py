

from matplotlib import pyplot as plt
from matplotlib.rcsetup import cycler
from numpy import NaN
import pandas as pd

L0 = 0.1001
meas="meas_2"


def importCSV(filepath, sortVctrl=True, maskFreqErr=1e99, maskApmErr=1e99):
    p_df = pd.read_csv(filepath,
                       sep=',',
                       skipinitialspace=True)
    # remove spaces in the column names
    p_df.columns = ((p_df.columns.str).strip()).str.strip()
    print(p_df.columns)
    # mask the necessary values
    return p_df.mask(p_df["errFreq1"] > maskFreqErr).mask(p_df["errAmp1"] > maskApmErr).mask(p_df["errFreq2"] > maskFreqErr).mask(p_df["errAmp2"] > maskApmErr)

def RelativeToRadius(num, thickness=50e-6):
    if num == 0:
        return pd.NA
    half_thickness = thickness/2
    return half_thickness / num - half_thickness

def MkCycle(num):
    lineStyles = ['-', '--', ':', '-.']
    # lineStyles = ['-']
    newColors = [plt.get_cmap('viridis')(1. * i/num) for i in range(num)]
    newPatterns = [lineStyles[i % len(lineStyles)] for i in range(num)]
    return (cycler(color=newColors) + cycler(linestyle=newPatterns))


def MakeStretchGraph(dataframe):
    fig, ax = plt.subplots(1,1, figsize=(8,6))
    numLines = dataframe["stretchAmt"].nunique()

    ax.set_xlabel(f"Strain (%)")
    ax.set_ylabel(f"Resistance (Ω)")
    ax.set_prop_cycle(MkCycle(numLines))

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
    angle = input("please give the whole part of the angle to plot. ")
    df = importCSV(f"./measurements_csv/{meas}/rising/angle_{angle}.0.csv")
    # print(df)
    fig2 = MakeStretchGraph(df)
    fig2.savefig(f"./figures/{meas}/gauge2_up_{angle}.png", dpi=500)
    plt.show()
