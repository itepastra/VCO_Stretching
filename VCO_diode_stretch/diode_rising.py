

import os
from matplotlib import pyplot as plt
from matplotlib.rcsetup import cycler
from numpy import NaN, sqrt
import pandas as pd
import numpy as np



def importCSV(filepath):
    p_df = pd.read_csv(filepath,
                       sep=',',
                       skipinitialspace=True)
    # remove spaces in the column names
    p_df.columns = ((p_df.columns.str).strip()).str.strip()
    print(p_df.columns)
    return p_df



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

    ax.set_xlabel(f"Vdiode (V)")
    ax.set_ylabel(f"diode current (A)")
    ax.set_prop_cycle(MkCycle(numLines))
    ax.set_yscale("symlog", linthresh=1e-9)

    for lab, df in dataframe.groupby("stretchAmt"):
        label = f"{(lab/L0 * 100):.3f}% {RelativeToRadius(lab/L0) * 1000:.2f} mm"
        ax.errorbar(df["V_diode"], df["Diode_amps"], capsize=None, lw=1, label=label)

    ax.grid()
    ax.legend()
    fig.tight_layout()
    return fig

def RelativeStretchGraph1(dataframe):
    fig, ax = plt.subplots(1,1, figsize=(8,6))
    numLines = dataframe["stretchAmt"].nunique()

    df2 = dataframe.copy()

    dfFirst = df2[df2['stretchAmt'] == 0]
    firstDiode = dfFirst["Diode_amps"].values[0:650]

    ax.set_xlabel(f"Vdiode (V)")
    ax.set_ylabel(f"relative Amps")
    ax.set_prop_cycle(MkCycle(numLines))

    for lab, df in dataframe.groupby("stretchAmt"):
        print(df)
        print(df2[df2['stretchAmt'] == 0])
        label = f"{(lab/L0 * 100):.3f}% {RelativeToRadius(lab/L0) * 1000:.2f} mm"
        relAmps = df["Diode_amps"]/firstDiode
        ax.errorbar(df["V_diode"], relAmps, capsize=None, lw=1, label=label)

    ax.grid()
    ax.legend()
    fig.tight_layout()
    return fig



def MakeStretchGraph2(dataframe):
    fig, ax = plt.subplots(1,1, figsize=(8,6))
    numLines = dataframe["stretchAmt"].nunique()

    ax.set_ylabel(f"Vdiode (V)")
    ax.set_xlabel(f"diode current (mA)")
    ax.set_prop_cycle(MkCycle(numLines))

    for lab, df in dataframe.groupby("stretchAmt"):
        label = f"{(lab/L0 * 100):.3f}% {RelativeToRadius(lab/L0) * 1000:.2f} mm"
        ax.errorbar( df["Diode_amps"]*1000,df["V_diode"], capsize=None, lw=1, label=label)

    ax.grid()
    ax.legend()
    fig.tight_layout()
    return fig

def RelativeStretchGraph2(dataframe):
    fig, ax = plt.subplots(1,1, figsize=(8,6))
    numLines = dataframe["stretchAmt"].nunique()

    df2 = dataframe.copy()

    dfFirst = df2[df2['stretchAmt'] == 0]
    firstDiode = averageDiode = df2.groupby("Vtarget")["V_diode"].mean().values[0:650]

    ax.set_xlabel(f"amps (A)")
    ax.set_ylabel(f"relative voltage")
    ax.set_prop_cycle(MkCycle(numLines))
    ax.set_xscale('log')

    for lab, df in dataframe.groupby("stretchAmt"):
        print(df)
        print(df2[df2['stretchAmt'] == 0])
        label = f"{(lab/L0 * 100):.3f}% {RelativeToRadius(lab/L0) * 1000:.2f} mm"
        relAmps = df["V_diode"]/firstDiode
        ax.errorbar(df["Diode_amps"].mask(df["Diode_amps"] < 0), relAmps, capsize=None, lw=1, label=label)

    ax.grid()
    ax.legend()
    fig.tight_layout()
    return fig

def MakeStretchGraph3(dataframe):
    fig, ax = plt.subplots(1,1, figsize=(8,6))
    numLines = dataframe["stretchAmt"].nunique()

    ax.set_xlabel(f"V_input (V)")
    ax.set_ylabel(f"diode current (mA)")
    ax.set_prop_cycle(MkCycle(numLines))

    for lab, df in dataframe.groupby("stretchAmt"):
        label = f"{(lab/L0 * 100):.3f}% {RelativeToRadius(lab/L0) * 1000:.2f} mm"
        ax.errorbar(df["Vtarget"], df["Diode_amps"]*1000, capsize=None, lw=1, label=label)

    ax.grid()
    ax.legend()
    fig.tight_layout()
    return fig

def RelativeStretchGraph3(dataframe):
    fig, ax = plt.subplots(1,1, figsize=(8,6))
    numLines = dataframe["stretchAmt"].nunique()

    df2 = dataframe.copy()

    dfFirst = df2[df2['stretchAmt'] == 0]
    firstDiode = dfFirst["Diode_amps"].values[0:650]

    ax.set_xlabel(f"V_input (V)")
    ax.set_ylabel(f"relative Amps")
    ax.set_prop_cycle(MkCycle(numLines))

    for lab, df in dataframe.groupby("stretchAmt"):
        print(df)
        print(df2[df2['stretchAmt'] == 0])
        label = f"{(lab/L0 * 100):.3f}% {RelativeToRadius(lab/L0) * 1000:.2f} mm"
        relAmps = df["Diode_amps"]/firstDiode
        ax.errorbar(df["Vtarget"], relAmps, capsize=None, lw=1, label=label)

    ax.grid()
    ax.legend()
    fig.tight_layout()
    return fig


def RelativeStretchGraph4(dataframe):
    fig, ax = plt.subplots(1,1, figsize=(8,6))
    numLines = dataframe["stretchAmt"].nunique()

    df2 = dataframe.copy()

    averageDiode = df2.groupby("Vtarget")["Diode_amps"].mean().values[0:650]
    print(averageDiode)

    ax.set_xlabel(f"V_input (V)")
    ax.set_ylabel(f"relative Amps")
    ax.set_prop_cycle(MkCycle(numLines))

    for lab, df in dataframe.groupby("stretchAmt"):
        print(df)
        print(df2[df2['stretchAmt'] == 0])
        label = f"{(lab/L0 * 100):.3f}% {RelativeToRadius(lab/L0) * 1000:.2f} mm"
        relAmps = df["Diode_amps"]/averageDiode
        print(df["Vtarget"])
        print(relAmps)
        ax.errorbar(df["Vtarget"], relAmps, capsize=None, lw=1, label=label)

    ax.grid()
    ax.legend()
    fig.tight_layout()
    return fig


if __name__ == "__main__":

    
    L0 = 0.1001
    meas = "meas_4"

    angle = input("please give the whole part of the angle to plot. ")
    df = importCSV(f"./VCO_diode_stretch/data/{meas}/rising/angle_{angle}.0_diode.csv")
    if not os.path.exists(f'./VCO_diode_stretch/figures/{meas}/'):
        os.makedirs(f'./VCO_diode_stretch/figures/{meas}/')
    if not os.path.exists(f'./VCO_diode_stretch/figures/{meas}/{angle}/'):
        os.makedirs(f'./VCO_diode_stretch/figures/{meas}/{angle}/')
    print(df)
    fig = MakeStretchGraph1(df)
    fig.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch_up_{angle}_diode.png", dpi=500)
    fig2 = RelativeStretchGraph1(df)
    fig2.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch_up_{angle}_rel_diode.png", dpi=500)
    fig3 = MakeStretchGraph2(df)
    fig3.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch_up_{angle}_diode_alt.png", dpi=500)
    fig4 = RelativeStretchGraph2(df)
    fig4.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch_up_{angle}_rel_diode_alt.png", dpi=500)
    fig5 = MakeStretchGraph3(df)
    fig5.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch_up_{angle}_diode_vin.png", dpi=500)
    fig6 = RelativeStretchGraph3(df)
    fig6.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch_up_{angle}_rel_diode_vin.png", dpi=500)
    fig7 = RelativeStretchGraph4(df)
    fig7.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch_up_{angle}_rel_diode_vina.png", dpi=500)
    # plt.show()
