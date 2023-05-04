

import os
from matplotlib import pyplot as plt
from matplotlib.rcsetup import cycler
from numpy import NaN, sqrt
import pandas as pd



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


def MakeStretchGraph1(dataframe):
    fig, ax = plt.subplots(1,1, figsize=(8,6))
    numLines = dataframe["stretchAmt"].nunique()

    ax.set_xlabel(f"Vctrl (V)")
    ax.set_ylabel(f"Frequency (MHz)")
    ax.set_prop_cycle(MkCycle(numLines))

    for lab, df in dataframe.groupby("stretchAmt"):
        label = f"{(lab/L0 * 100):.3f}% {RelativeToRadius(lab/L0) * 1000:.2f} mm"
        ax.errorbar(df["Vctrl"], df["Freq1"]/1e6, yerr=df["errFreq1"]/1e6/sqrt(df["AmtFreq1"]), capsize=None, lw=1, label=label)

    ax.grid()
    ax.legend()
    fig.tight_layout()
    return fig

def RelativeStretchGraph1(dataframe):
    fig, ax = plt.subplots(1,1, figsize=(8,6))
    numLines = dataframe["stretchAmt"].nunique()

    df2 = dataframe.copy()

    dfFirst = df2[df2['stretchAmt'] == 0]
    firstFreq = dfFirst["Freq1"].values[0:13]
    firstErr = dfFirst["errFreq1"].values[0:13]

    ax.set_xlabel(f"Vctrl (V)")
    ax.set_ylabel(f"relative Frequency")
    ax.set_prop_cycle(MkCycle(numLines))

    for lab, df in dataframe.groupby("stretchAmt"):
        print(df)
        print(df2[df2['stretchAmt'] == 0])
        label = f"{(lab/L0 * 100):.3f}% {RelativeToRadius(lab/L0) * 1000:.2f} mm"
        relFreq = df["Freq1"]/firstFreq
        # print(f"{lab} has relFreqs {relFreq}")
        relErr = df["errFreq1"]/firstFreq/sqrt(df["AmtFreq1"])
        # print(f"{lab} has relErr {relErr}")
        ax.errorbar(df["Vctrl"], relFreq, yerr=relErr, capsize=None, lw=1, label=label)

    ax.grid()
    ax.legend()
    fig.tight_layout()
    return fig


def MakeStretchGraph2(dataframe):
    fig, ax = plt.subplots(1,1, figsize=(8,6))
    numLines = dataframe["stretchAmt"].nunique()

    ax.set_xlabel(f"Vctrl (V)")
    ax.set_ylabel(f"Frequency (MHz)")
    ax.set_prop_cycle(MkCycle(numLines))

    for lab, df in dataframe.groupby("stretchAmt"):
        label = f"{(lab/L0 * 100):.3f}% {RelativeToRadius(lab/L0) * 1000:.2f} mm"
        ax.errorbar(df["Vctrl"], df["Freq2"]/1e6, yerr=df["errFreq2"]/1e6/sqrt(df["AmtFreq2"]), capsize=None, lw=1, label=label)

    ax.grid()
    ax.legend()
    fig.tight_layout()
    return fig

def RelativeStretchGraph2(dataframe):
    fig, ax = plt.subplots(1,1, figsize=(8,6))
    numLines = dataframe["stretchAmt"].nunique()

    df2 = dataframe.copy()

    dfFirst = df2[df2['stretchAmt'] == 0]
    firstFreq = dfFirst["Freq2"].values[0:13]
    firstErr = dfFirst["errFreq2"].values[0:13]

    ax.set_xlabel(f"Vctrl (V)")
    ax.set_ylabel(f"relative Frequency")
    ax.set_prop_cycle(MkCycle(numLines))

    for lab, df in dataframe.groupby("stretchAmt"):
        print(df)
        print(df2[df2['stretchAmt'] == 0])
        label = f"{(lab/L0 * 100):.3f}% {RelativeToRadius(lab/L0) * 1000:.2f} mm"
        relFreq = df["Freq2"]/firstFreq
        # print(f"{lab} has relFreqs {relFreq}")
        relErr = df["errFreq2"]/firstFreq/sqrt(df["AmtFreq2"])
        # print(f"{lab} has relErr {relErr}")
        ax.errorbar(df["Vctrl"], relFreq, yerr=relErr, capsize=None, lw=1, label=label)

    ax.grid()
    ax.legend()
    fig.tight_layout()
    return fig

if __name__ == "__main__":

    
    L0 = 0.1001
    meas = "meas_3"

    angle = input("please give the whole part of the angle to plot. ")
    df = importCSV(f"./VCO_diode_stretch/data/{meas}/falling/angle_{angle}.0.csv")
    if not os.path.exists(f'./VCO_diode_stretch/figures/{meas}/'):
        os.makedirs(f'./VCO_diode_stretch/figures/{meas}/')
    if not os.path.exists(f'./VCO_diode_stretch/figures/{meas}/{angle}/'):
        os.makedirs(f'./VCO_diode_stretch/figures/{meas}/{angle}/')
    # print(df)
    fig = MakeStretchGraph1(df)
    fig.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch1_down_{angle}.png", dpi=500)
    fig2 = RelativeStretchGraph1(df)
    fig2.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch1_down_{angle}_rel.png", dpi=500)
    fig3 = MakeStretchGraph2(df)
    fig3.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch2_down_{angle}.png", dpi=500)
    fig4 = RelativeStretchGraph2(df)
    fig4.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch2_down_{angle}_rel.png", dpi=500)
    # plt.show()
