

import os
from matplotlib import pyplot as plt
from matplotlib.rcsetup import cycler
from numpy import NaN, sqrt
import pandas as pd



def importCSV(filepath, sortVctrl=True, maskAmpErr=1e99, maskApmErr=1e99):
    p_df = pd.read_csv(filepath,
                       sep=',',
                       skipinitialspace=True)
    # remove spaces in the column names
    p_df.columns = ((p_df.columns.str).strip()).str.strip()
    print(p_df.columns)
    # mask the necessary values
    return p_df.mask(p_df["errAmp1"] > maskAmpErr).mask(p_df["errAmp1"] > maskApmErr).mask(p_df["errAmp2"] > maskAmpErr).mask(p_df["errAmp2"] > maskApmErr)

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


def MakeStretchGraph1(dataframe):
    fig, ax = plt.subplots(1,1, figsize=(8,6))
    numLines = dataframe["stretchAmt"].nunique()

    ax.set_xlabel(f"Vctrl (V)")
    ax.set_ylabel(f"Amplitude (V)")
    ax.set_prop_cycle(MkCycle(numLines))

    for lab, df in dataframe.groupby("stretchAmt"):
        label = f"{(lab/L0 * 100):.3f}% {RelativeToRadius(lab/L0) * 1000:.2f} mm"
        ax.errorbar(df["Vctrl"], df["Amp1"], yerr=df["errAmp1"]/1e6/sqrt(df["AmtAmp1"]), capsize=None, lw=1, label=label)

    ax.grid()
    ax.legend()
    fig.tight_layout()
    return fig

def RelativeStretchGraph1(dataframe):
    fig, ax = plt.subplots(1,1, figsize=(8,6))
    numLines = dataframe["stretchAmt"].nunique()

    df2 = dataframe.copy()

    dfFirst = df2[df2['stretchAmt'] == 0]
    firstAmp = dfFirst["Amp1"].values[0:130]
    firstErr = dfFirst["errAmp1"].values[0:130]

    ax.set_xlabel(f"Vctrl (V)")
    ax.set_ylabel(f"relative Amplitude")
    ax.set_prop_cycle(MkCycle(numLines))

    for lab, df in dataframe.groupby("stretchAmt"):
        print(df)
        print(df2[df2['stretchAmt'] == 0])
        label = f"{(lab/L0 * 100):.3f}% {RelativeToRadius(lab/L0) * 1000:.2f} mm"
        relAmp = df["Amp1"]/firstAmp
        # print(f"{lab} has relAmps {relAmp}")
        relErr = df["errAmp1"]/firstAmp/sqrt(df["AmtAmp1"])
        # print(f"{lab} has relErr {relErr}")
        ax.errorbar(df["Vctrl"], relAmp, yerr=relErr, capsize=None, lw=1, label=label)

    ax.grid()
    ax.legend()
    fig.tight_layout()
    return fig


def MakeStretchGraph2(dataframe):
    fig, ax = plt.subplots(1,1, figsize=(8,6))
    numLines = dataframe["stretchAmt"].nunique()

    ax.set_xlabel(f"Vctrl (V)")
    ax.set_ylabel(f"Amplitude (V)")
    ax.set_prop_cycle(MkCycle(numLines))

    for lab, df in dataframe.groupby("stretchAmt"):
        label = f"{(lab/L0 * 100):.3f}% {RelativeToRadius(lab/L0) * 1000:.2f} mm"
        ax.errorbar(df["Vctrl"], df["Amp2"], yerr=df["errAmp2"]/1e6/sqrt(df["AmtAmp2"]), capsize=None, lw=1, label=label)

    ax.grid()
    ax.legend()
    fig.tight_layout()
    return fig

def RelativeStretchGraph2(dataframe):
    fig, ax = plt.subplots(1,1, figsize=(8,6))
    numLines = dataframe["stretchAmt"].nunique()

    df2 = dataframe.copy()

    dfFirst = df2[df2['stretchAmt'] == 0]
    firstAmp = dfFirst["Amp2"].values[0:130]
    firstErr = dfFirst["errAmp2"].values[0:130]

    ax.set_xlabel(f"Vctrl (V)")
    ax.set_ylabel(f"relative Amplitude")
    ax.set_prop_cycle(MkCycle(numLines))

    for lab, df in dataframe.groupby("stretchAmt"):
        print(df)
        print(df2[df2['stretchAmt'] == 0])
        label = f"{(lab/L0 * 100):.3f}% {RelativeToRadius(lab/L0) * 1000:.2f} mm"
        relAmp = df["Amp2"]/firstAmp
        # print(f"{lab} has relAmps {relAmp}")
        relErr = df["errAmp2"]/firstAmp/sqrt(df["AmtAmp2"])
        # print(f"{lab} has relErr {relErr}")
        ax.errorbar(df["Vctrl"], relAmp, yerr=relErr, capsize=None, lw=1, label=label)

    ax.grid()
    ax.legend()
    fig.tight_layout()
    return fig

if __name__ == "__main__":

    
    L0 = 0.1001
    meas = "meas_4"

    angle = input("please give the whole part of the angle to plot. ")
    df = importCSV(f"./VCO_diode_stretch/data/{meas}/rising/angle_{angle}.0.csv")
    if not os.path.exists(f'./VCO_diode_stretch/figures/{meas}/'):
        os.makedirs(f'./VCO_diode_stretch/figures/{meas}/')
    if not os.path.exists(f'./VCO_diode_stretch/figures/{meas}/{angle}/'):
        os.makedirs(f'./VCO_diode_stretch/figures/{meas}/{angle}/')
    # print(df)
    fig = MakeStretchGraph1(df)
    fig.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch1_up_{angle}_amp.png", dpi=500)
    fig2 = RelativeStretchGraph1(df)
    fig2.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch1_up_{angle}_amp_rel.png", dpi=500)
    fig3 = MakeStretchGraph2(df)
    fig3.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch2_up_{angle}_amp.png", dpi=500)
    fig4 = RelativeStretchGraph2(df)
    fig4.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch2_up_{angle}_amp_rel.png", dpi=500)
    # plt.show()
