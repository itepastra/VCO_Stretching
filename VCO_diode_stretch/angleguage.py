import os
import re
import matplotlib.pyplot as plt
import helpers
import pandas as pd

import numpy as np
import scipy.optimize


def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = np.deg2rad(np.array(tt))
    yy = np.array(yy)

    guess_offset = np.mean(yy)
    guess = np.array([20, guess_offset])

    def sinfunc(t, A, c): return A * np.sin(2*t + np.pi/2) + c
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, c = popt
    print(f"{A} * sin(2*t + pi) + {c}")

    def fitfunc(t): return A * np.sin(2*t + np.pi/2) + c
    return {"amp": A,  "offset": c, "fitfunc": fitfunc, "maxcov": np.max(pcov), "rawres": (guess, popt, pcov)}


def angle_gauge(dataframe):
    df2 = dataframe.copy()

    dfFirst = df2[df2['stretchAmt'] == 0]
    firstFreq = dfFirst["Freq1"].values[0:(dfFirst["Freq1"].count())]
    firstErr = dfFirst["errFreq1"].values[0:(dfFirst["errFreq1"].count())]

    gauges = []
    gaugeerrs = []
    angles = []

    for lab, df in dataframe.groupby("stretchAmt"):
        if lab <= 0.000060000:
            continue

        relFreq = (df["Freq1"]/firstFreq)-1
        relErr = df["errFreq1"]/np.sqrt(df["AmtFreq1"])/firstFreq
        gaugefac = relFreq / (df["stretchAmt"]/L0)
        gaugeerr = relErr
        gauges.append(gaugefac)
        gaugeerrs.append(gaugeerr)
        angles.append(df["stretchAngle"])


    return (gauges, gaugeerrs, angles)


def calc_gauge(dataframe):
    df2 = dataframe.copy()

    dfFirst = df2[df2['stretchAmt'] == 0]
    firstFreq = dfFirst["Freq1"].values[0:(dfFirst["Freq1"].count())]
    firstErr = dfFirst["errFreq1"].values[0:(dfFirst["errFreq1"].count())]
    firstStrain = dfFirst["strain"].values[0:(dfFirst["strain"].count())]

    gauges = []
    gaugeerrs = []
    angles = []

    for lab, df in dataframe.groupby("stretchAmt"):
        if lab <= 0.000060000:
            continue

        relFreq = (df["Freq1"]/firstFreq)-1
        relErr = df["errFreq1"]/np.sqrt(df["AmtFreq1"])/firstFreq
        gaugefac = relFreq / (df["strain"] - firstStrain)
        gaugeerr = relErr
        gauges.append(gaugefac)
        gaugeerrs.append(gaugeerr)
        angles.append(df["angle"])


    return (gauges, gaugeerrs, angles)


def check(file_path):
    regex = "VCO_diode_stretch\/data\/meas_\d+\/rising\/angle_\d+\.\d+\.csv"
    if re.match(regex, file_path):
        return True
    else:
        return False


def micrometer():
    # df = helpers.importCSV("VCO_diode_stretch/data/meas_4/rising/angle_90.0.csv")
    # angle_gauge(df)
    folder_path = "VCO_diode_stretch/data/"
    file_extension = ".csv"

    allgauges = []
    allgaugeerrs = []
    allangles = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(file_extension):
                file_path = os.path.join(root, file)
                if check(file_path):
                    newgauges, newgaugeerrs, newangles = angle_gauge(
                        helpers.importCSV(file_path))
                    allgauges.append(newgauges)
                    allgaugeerrs.append(newgaugeerrs)
                    allangles.append(newangles)

    allgauges = np.concatenate(
        [np.concatenate([x for x in v]) for v in allgauges])
    allangles = np.concatenate(
        [np.concatenate([x for x in v]) for v in allangles])
    
    dfout = pd.DataFrame(columns=["angle", "gaugefactors"])
    dfout["angle"] = allangles
    dfout["gaugefactors"] = allgauges
    finalavg = []
    finalerr = []
    finalang = []

    for lab, df in dfout.groupby("angle"):
        finalavg.append(df["gaugefactors"].mean())
        finalerr.append(df["gaugefactors"].std())
        finalang.append(lab)


    plt.errorbar(finalang, finalavg, finalerr, fmt="o", label= "micrometer factors")
    res = fit_sin(finalang, finalavg)
    print(res)

    return res


def strainGauge():

    folder_path = "VCO_diode_stretch/data/"
    file_extension = ".csv"

    allgauges = []
    allgaugeerrs = []
    allangles = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(file_extension):
                file_path = os.path.join(root, file)
                if check(file_path):
                    newgauges, newgaugeerrs, newangles = calc_gauge(
                        helpers.importCSV(file_path))
                    allgauges.append(newgauges)
                    allgaugeerrs.append(newgaugeerrs)
                    allangles.append(newangles)

    allgauges = np.concatenate(
        [np.concatenate([x for x in v]) for v in allgauges])
    allangles = np.concatenate(
        [np.concatenate([x for x in v]) for v in allangles])


    dfout = pd.DataFrame(columns=["angle", "gaugefactors"])
    dfout["angle"] = allangles % 360
    dfout["gaugefactors"] = allgauges
    finalavg = []
    finalerr = []
    finalang = []

    for lab, df in dfout.groupby(dfout['angle'].apply(lambda x: round(x, 0))):
        finalavg.append(df["gaugefactors"].mean())
        finalerr.append(df["gaugefactors"].std())
        finalang.append(lab)

    plt.errorbar(finalang, finalavg, finalerr, fmt="o", label = "strain gauge factors")

    res = fit_sin(finalang, finalavg)
    print(res)

    return res


if __name__ == "__main__":

    L0 = 0.1001

    mmfit = micrometer()
    # plt.show()
    sgfit = strainGauge()

    xs = np.linspace(0,np.deg2rad(360),1000)

    plt.plot(np.rad2deg(xs), mmfit["fitfunc"](xs), linestyle="dashed", label = f"micrometer: ${mmfit['amp']:.2f}cos(2x){'+' if mmfit['offset'] >= 0 else ''}{mmfit['offset']:.2f}$")
    plt.plot(np.rad2deg(xs), sgfit["fitfunc"](xs), label = f"strain gauges: ${sgfit['amp']:.2f}cos(2x){'+' if sgfit['offset'] >= 0 else ''}{sgfit['offset']:.2f}$")

    plt.legend()
    plt.savefig("VCO_diode_stretch/figures/angleswithgauges.png", dpi=500)
    plt.show()
