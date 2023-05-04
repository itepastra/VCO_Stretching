import os
from typing import Tuple
import pandas as pd
import numpy as np


def ShuntCalc(voltageDiff: float, shuntResistance: float) -> float:
    # use ohm's law to calculate the current across the shunt
    return voltageDiff / shuntResistance


def RosetteCalc(gageResistances: Tuple[float, float, float], gagebases: Tuple[float, float, float], angle: float, gagefactor=2.16) -> Tuple[float, float]:
    y,x, xy = gageResistances
    bx, by, bxy = gagebases
    ex, ey, ez = (x-bx) / gagefactor, (y-by) / gagefactor, (xy-bxy) / gagefactor
    print(f"ex:{ex:.3f},ey:{ey:.3f},ez:{ez:.3f} @ {angle}")
    exy = ez - (ex+ey)/2
    m = np.array([[ex, exy], [exy, ey]])
    w,v = np.linalg.eig(m)
    # print(v,w)
    angles = np.rad2deg(np.arctan2(v[:,1], v[:,0]))
    print(f"m: \n{m}\n{v}, \nvals: {w}, \nangles: \n{angles}, real angle: {angle}")

    if w[0] > 0:
        if angles[0] < -90:
            angles[0] = angles[0] + 180
        angle = angles[0]
    elif w[1] > 0:
        if angles[1] < -90:
            angles[1] = angles[1] + 180
        angle = angles[1]
    else:
        angle = np.NaN

    # return ((angles[0] if w[0] > 0 else (angles[1] if w[1] > 0 else np.NaN)), max(w))
    return (angle, max(w))


def ModifyToCSV(filename):
    filePath = f"./VCO_diode_stretch/measurements/{filename}"
    outputPath = f"./VCO_diode_stretch/data/{meas}/{filename}.csv"

    df = pd.read_csv(filePath, sep='\t', header=None)
    df.columns = ["date", "time", "Vctrl", "stretchAmt", "stretchAngle", "AmtFreq1", "Freq1", "errFreq1", "AmtAmp1", "Amp1", "errAmp1", "AmtFreq2", "Freq2", "errFreq2",
                  "AmtAmp2", "Amp2", "errAmp2", "VDD_VCO1_shunt", "VDD_driver_shunt", "VDD", "VDD_VCO2_shunt", "VDD_ring_shunt", "strain_1", "strain_2", "strain_3", "temp", "V_diode_shunt", "V_diode"]

    print(df)

    df["VDD_VCO1_amps"] = ShuntCalc(df["VDD_VCO1_shunt"], 52.51)
    df["VDD_VCO2_amps"] = ShuntCalc(df["VDD_VCO2_shunt"], 52.28)
    df["VDD_driver_amps"] = ShuntCalc(df["VDD_driver_shunt"], 5.72)
    df["VDD_ring_amps"] = ShuntCalc(df["VDD_ring_shunt"], 985)
    df["Diode_amps"] = ShuntCalc(df["V_diode_shunt"], 1001)

    # the occiloscope only uses the last 512 values for the mean, so this puts limits on the uncertainty of the mean
    df["AmtFreq1"] = df["AmtFreq1"].map(lambda x: min(512, x))
    df["AmtAmp1"] = df["AmtAmp1"].map(lambda x: min(512, x))
    df["AmtFreq2"] = df["AmtFreq2"].map(lambda x: min(512, x))
    df["AmtAmp2"] = df["AmtAmp2"].map(lambda x: min(512, x))

    df.to_csv(outputPath, index=False)


def diodeCSV(filename):
    filePath = f"./VCO_diode_stretch/measurements/{filename}"
    outputPath = f"./VCO_diode_stretch/data/{meas}/{filename}.csv"

    df = pd.read_csv(filePath, sep='\t', header=None)
    df.columns = ["date", "time",  "stretchAngle", "stretchAmt", "Vtarget", "VDD_VCO1_shunt", "VDD_driver_shunt", "VDD",
                  "VDD_VCO2_shunt", "VDD_ring_shunt", "strain_1", "strain_2", "strain_3", "temp", "V_diode_shunt", "V_diode"]
    print(df)

    df["VDD_VCO1_amps"] = ShuntCalc(df["VDD_VCO1_shunt"], 52.51)
    df["VDD_VCO2_amps"] = ShuntCalc(df["VDD_VCO2_shunt"], 52.28)
    df["VDD_driver_amps"] = ShuntCalc(df["VDD_driver_shunt"], 5.72)
    df["VDD_ring_amps"] = ShuntCalc(df["VDD_ring_shunt"], 985)
    df["Diode_amps"] = ShuntCalc(df["V_diode_shunt"], 1001)

    # there is a -1.2V added after the value shown in Vtarget, this is intentional so should be represented
    df["Vtarget"] = df["Vtarget"] - 1.2

    df.to_csv(outputPath, index=False)


def importCSV(filepath, sortVctrl=True, maskFreqErr=1e99, maskApmErr=1e99):
    p_df = pd.read_csv(filepath,
                       sep=',',
                       skipinitialspace=True)
    # remove spaces in the column names
    p_df.columns = ((p_df.columns.str).strip()).str.strip()
    print(p_df.columns)
    # mask the necessary values
    return p_df.mask(p_df["errFreq1"] > maskFreqErr).mask(p_df["errAmp1"] > maskApmErr).mask(p_df["errFreq2"] > maskFreqErr).mask(p_df["errAmp2"] > maskApmErr)


def importDiodeCSV(filepath):
    p_df = pd.read_csv(filepath,
                       sep=',',
                       skipinitialspace=True)
    # remove spaces in the column names
    p_df.columns = ((p_df.columns.str).strip()).str.strip()
    print(p_df.columns)
    # mask the necessary values
    return p_df


def splitAngles(dataframe, affix=""):

    for angle, df in dataframe.groupby("stretchAngle"):
        # create csv per angle
        diffs = df["stretchAmt"].diff()
        df["stretchDiffs"] = diffs.replace(0, pd.NA).ffill().fillna(0)

        if not os.path.exists(f'./VCO_diode_stretch/data/{meas}/angle/'):
            os.makedirs(f'./VCO_diode_stretch/data/{meas}/angle/')

        outputPath = os.path.join(
            f"./VCO_diode_stretch/data/{meas}/angle/", f"angle_{angle}{affix}.csv")
        df.to_csv(outputPath, index=False)
        # create csv for the rising part of the angle
        splitRising(df, angle, affix)
        splitFalling(df, angle, affix)


def splitRising(dataframe, angle, affix=""):
    # df = dataframe.copy().dropna()

    if not os.path.exists(f'./VCO_diode_stretch/data/{meas}/rising/'):
        os.makedirs(f'./VCO_diode_stretch/data/{meas}/rising/')
    df_rising = dataframe[(dataframe["stretchDiffs"] >= 0)]
    outputPath = os.path.join(
        f"./VCO_diode_stretch/data/{meas}/rising/", f"angle_{angle}{affix}.csv")
    df_rising.to_csv(outputPath, index=False)


def splitFalling(dataframe, angle, affix=""):

    if not os.path.exists(f'./VCO_diode_stretch/data/{meas}/falling/'):
        os.makedirs(f'./VCO_diode_stretch/data/{meas}/falling/')
    max_stretch_amt = dataframe["stretchAmt"].max()
    df_falling = dataframe[(dataframe["stretchDiffs"] < 0) | (
        dataframe["stretchAmt"] == max_stretch_amt) & (dataframe["stretchAngle"] == angle)]
    outputPath = os.path.join(
        f"./VCO_diode_stretch/data/{meas}/falling/", f"angle_{angle}{affix}.csv")
    df_falling.to_csv(outputPath, index=False)


if (__name__ == "__main__"):
    meas = "meas_3"
    filename = "Measurement_stretch_3"

    # gageBaseResistances = (350.7475,350.93787,350.61167)
    

    diodeFilename = filename + "_diode"

    if not os.path.exists(f'./VCO_diode_stretch/data/{meas}'):
        os.makedirs(f'./VCO_diode_stretch/data/{meas}')

    ModifyToCSV(filename)
    diodeCSV(diodeFilename)
    df = importCSV(f"./VCO_diode_stretch/data/{meas}/{filename}.csv")
    

    # to calculate the base resistances of the strain gages we take the averages of the unstretched measurements
    groups = df[df["stretchAmt"] == 0]
    strain_1_avg = groups["strain_1"].mean()
    strain_2_avg = groups["strain_2"].mean()
    strain_3_avg = groups["strain_3"].mean()
    # we also calculate the standard-deviations to see if there are any big outliers
    strain_1_std = groups["strain_1"].std()
    strain_2_std = groups["strain_2"].std()
    strain_3_std = groups["strain_3"].std()
    print(f"strain_1: {strain_1_avg}/{strain_1_std}\nstrain_2: {strain_2_avg}/{strain_2_std}\nstrain_3: {strain_3_avg}/{strain_3_std}")
    gageBaseResistances = (strain_1_avg, strain_2_avg, strain_3_avg)
    df["angle"] = df.apply(lambda x: RosetteCalc((x['strain_1'], x['strain_2'], x['strain_3']), gageBaseResistances, x['stretchAngle'])[0], axis=1)
    df["strain"] = df.apply(lambda x: RosetteCalc((x['strain_1'], x['strain_2'], x['strain_3']), gageBaseResistances, x['stretchAngle'])[1], axis=1)
    print(df)
    splitAngles(df)

    df2 = importDiodeCSV(f"./VCO_diode_stretch/data/{meas}/{diodeFilename}.csv")
    splitAngles(df2, affix="_diode")
    print(f"strain_1: {strain_1_avg}/{strain_1_std}\nstrain_2: {strain_2_avg}/{strain_2_std}\nstrain_3: {strain_3_avg}/{strain_3_std}")


