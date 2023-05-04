import os
import helpers
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def RelativeStretchGraphAmps(dataframe, column):
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    numLines = dataframe["stretchAmt"].nunique()

    df2 = dataframe.copy()

    dfFirst = df2[df2['stretchAmt'] == 0]
    firstCur = dfFirst[column].values[0:13]

    ax.set_xlabel(f"Vctrl (V)")
    ax.set_ylabel(f"Current relative to 0 strain")
    ax.set_prop_cycle(helpers.MkCycle(numLines))

    for lab, df in dataframe.groupby("stretchAmt"):
        print(df)
        print(df2[df2['stretchAmt'] == 0])
        label = f"{(lab/L0 * 100):.3f}% {helpers.RelativeToRadius(lab/L0) * 1000:.2f} mm"
        relCur = df[column]/firstCur
        ax.errorbar(df["Vctrl"], relCur, 
                    capsize=None, lw=1, label=label)

    ax.grid()
    ax.legend()
    fig.tight_layout()
    return fig

def AbsStretchGraphAmps(dataframe, column):
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    numLines = dataframe["stretchAmt"].nunique()

    ax.set_xlabel(f"Vctrl (V)")
    ax.set_ylabel(f"Current relative to 0 strain")
    ax.set_prop_cycle(helpers.MkCycle(numLines))

    for lab, df in dataframe.groupby("stretchAmt"):
        print(df)
        label = f"{(lab/L0 * 100):.3f}% {helpers.RelativeToRadius(lab/L0) * 1000:.2f} mm"
        ax.errorbar(df["Vctrl"], df[column], 
                    capsize=None, lw=1, label=label)

    ax.grid()
    ax.legend()
    fig.tight_layout()
    return fig


if __name__ == "__main__":

    L0 = 0.1001
    meas = "meas_3"

    angle = input("please give the whole part of the angle to plot. ")
    df = helpers.importCSV(f"./VCO_diode_stretch/data/{meas}/rising/angle_{angle}.0.csv")
    if not os.path.exists(f'./VCO_diode_stretch/figures/{meas}/'):
        os.makedirs(f'./VCO_diode_stretch/figures/{meas}/')

    if not os.path.exists(f'./VCO_diode_stretch/figures/{meas}/{angle}/'):
        os.makedirs(f'./VCO_diode_stretch/figures/{meas}/{angle}/')
    # print(df)
    fig1 = AbsStretchGraphAmps(df,"VDD_VCO1_amps")
    fig1.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch1_up_{angle}_VDD1_amps.png", dpi=500)
    fig2 = AbsStretchGraphAmps(df,"VDD_VCO2_amps")
    fig2.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch1_up_{angle}_VDD2_amps.png", dpi=500)
    fig3 = AbsStretchGraphAmps(df,"VDD_driver_amps")
    fig3.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch1_up_{angle}_driver_amps.png", dpi=500)
    fig4 = AbsStretchGraphAmps(df,"VDD_ring_amps")
    fig4.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch1_up_{angle}_ring_amps.png", dpi=500)
    fig5 = RelativeStretchGraphAmps(df,"VDD_VCO1_amps")
    fig5.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch1_up_{angle}_VDD1_amps_rel.png", dpi=500)
    fig6 = RelativeStretchGraphAmps(df,"VDD_VCO2_amps")
    fig6.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch1_up_{angle}_VDD2_amps_rel.png", dpi=500)
    fig7 = RelativeStretchGraphAmps(df,"VDD_driver_amps")
    fig7.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch1_up_{angle}_driver_amps_rel.png", dpi=500)
    fig8 = RelativeStretchGraphAmps(df,"VDD_ring_amps")
    fig8.savefig(f"./VCO_diode_stretch/figures/{meas}/{angle}/stretch1_up_{angle}_ring_amps_rel.png", dpi=500)

    # plt.show()