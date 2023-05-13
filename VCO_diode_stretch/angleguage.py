from math import sqrt
import matplotlib.pyplot as plt
import numpy as np

angles = np.array([0, 15, 30, 45, 60, 75, 90])
gauges = np.array([13, 9, 6, 1, -6, -12, -15])
anglesnp = np.linspace(min(angles),max(angles),(max(angles)-min(angles)))

plt.plot(angles, gauges, label="gauge factor")
plt.xlabel("angle (°)")
plt.ylabel("gauge factor")
plt.plot(anglesnp, np.cos(2*np.deg2rad(anglesnp)) * 14, label="$14cos(2x)$")
plt.legend()
plt.savefig("./VCO_diode_stretch/figures/angleswithvisualgauges", dpi=1000)
plt.show()

import pandas as pd



def angle_gauge(dataframe):
    df2 = dataframe.copy()

    dfFirst = df2[df2['stretchAmt'] == 0]
    firstFreq = dfFirst["Freq1"].values[0:13]
    firstErr = dfFirst["errFreq1"].values[0:13]

    gauges = []

    for lab, df in dataframe.groupby("stretchAmt"):
        # print(df)
        # print(df2[df2['stretchAmt'] == 0])
        # label = f"{(lab/L0 * 100):.3f}% {RelativeToRadius(lab/L0) * 1000:.2f} mm"
        # relFreq = df["Freq2"]/firstFreq
        # # print(f"{lab} has relFreqs {relFreq}")
        # relErr = df["errFreq2"]/firstFreq/sqrt(df["AmtFreq2"])
        # # print(f"{lab} has relErr {relErr}")

        relFreq = df["Freq1"]/firstFreq
        relErr = df["errFreq1"]/firstFreq/sqrt(df["amtFreq1"])