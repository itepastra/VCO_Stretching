import os
from typing import Tuple
import pandas as pd
import numpy as np


def ShuntCalc(voltageDiff: float, shuntResistance: float) -> float:
    # use ohm's law to calculate the current across the shunt
    return voltageDiff / shuntResistance


def RosetteCalc(gaugeResistances: Tuple[float, float, float], gaugeBases: Tuple[float, float, float], gagefactor=2.16) -> Tuple[float, float, float]:
    y, x, xy = gaugeResistances
    bx, by, bxy = gaugeBases
    ex, ey, ez = (x-bx) / gagefactor, (y-by) / gagefactor, (xy-bxy) / gagefactor
    exy = ez - (ex+ey)/2
    m = np.array([[ex, exy], [exy, ey]])
    w,v = np.linalg.eig(m)
    print(f"m: \n{m}, \nvals: {w}, \nvecs: \n{np.rad2deg(np.arctan2(v[:,0], v[:,1]))}")

    return (ex, ey)


def ModifyToCSV(filename):
    filePath = f"./measurements/{filename}"
    outputPath = f"./data/{meas}/{filename}.csv"

    df = pd.read_csv(filePath, sep='\t', header=None)
    df.columns = ["date", "time", "Vctrl", "stretchAmt", "stretchAngle", "AmtFreq1", "Freq1", "errFreq1", "AmtAmp1", "Amp1", "errAmp1", "AmtFreq2", "Freq2", "errFreq2",
                  "AmtAmp2", "Amp2", "errAmp2", "VDD_VCO1_shunt", "VDD_driver_shunt", "VDD", "VDD_VCO2_shunt", "VDD_ring_shunt", "strain_1", "strain_2", "strain_3", "temp", "V_diode_shunt", "V_diode"]

    print(df)

    df["VDD_VCO1_amps"] = ShuntCalc(df["VDD_VCO1_shunt"], 1000)
    df["VDD_VCO2_amps"] = ShuntCalc(df["VDD_VCO2_shunt"], 1000)
    df["VDD_driver_amps"] = ShuntCalc(df["VDD_driver_shunt"], 1000)
    df["VDD_ring_amps"] = ShuntCalc(df["VDD_ring_shunt"], 1000)
    df["Diode_amps"] = ShuntCalc(df["V_diode_shunt"], 1000)

    # the occiloscope only uses the last 512 values for the mean, so this puts limits on the uncertainty of the mean
    df["AmtFreq1"] = df["AmtFreq1"].map(lambda x: min(512, x))
    df["AmtAmp1"] = df["AmtAmp1"].map(lambda x: min(512, x))
    df["AmtFreq2"] = df["AmtFreq2"].map(lambda x: min(512, x))
    df["AmtAmp2"] = df["AmtAmp2"].map(lambda x: min(512, x))

    df.to_csv(outputPath, index=False)


def diodeCSV(filename):
    filePath = f"./measurements/{filename}"
    outputPath = f"./data/{meas}/{filename}.csv"

    df = pd.read_csv(filePath, sep='\t', header=None)
    df.columns = ["date", "time",  "stretchAngle", "stretchAmt", "Vtarget", "VDD_VCO1_shunt", "VDD_driver_shunt", "VDD",
                  "VDD_VCO2_shunt", "VDD_ring_shunt", "strain_1", "strain_2", "strain_3", "temp", "V_diode_shunt", "V_diode"]
    print(df)

    df["VDD_VCO1_amps"] = ShuntCalc(df["VDD_VCO1_shunt"], 1000)
    df["VDD_VCO2_amps"] = ShuntCalc(df["VDD_VCO2_shunt"], 1000)
    df["VDD_driver_amps"] = ShuntCalc(df["VDD_driver_shunt"], 1000)
    df["VDD_ring_amps"] = ShuntCalc(df["VDD_ring_shunt"], 1000)
    df["Diode_amps"] = ShuntCalc(df["V_diode_shunt"], 1000)

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

        if not os.path.exists(f'./data/{meas}/angle/'):
            os.makedirs(f'./data/{meas}/angle/')

        outputPath = os.path.join(
            f"./data/{meas}/angle/", f"angle_{angle}{affix}.csv")
        df.to_csv(outputPath, index=False)
        # create csv for the rising part of the angle
        splitRising(df, angle, affix)
        splitFalling(df, angle, affix)


def splitRising(dataframe, angle, affix=""):
    # df = dataframe.copy().dropna()

    if not os.path.exists(f'./data/{meas}/rising/'):
        os.makedirs(f'./data/{meas}/rising/')
    df_rising = dataframe[(dataframe["stretchDiffs"] >= 0)]
    outputPath = os.path.join(
        f"./data/{meas}/rising/", f"angle_{angle}{affix}.csv")
    df_rising.to_csv(outputPath, index=False)


def splitFalling(dataframe, angle, affix=""):

    if not os.path.exists(f'./data/{meas}/falling/'):
        os.makedirs(f'./data/{meas}/falling/')
    max_stretch_amt = dataframe["stretchAmt"].max()
    df_falling = dataframe[(dataframe["stretchDiffs"] < 0) | (
        dataframe["stretchAmt"] == max_stretch_amt) & (dataframe["stretchAngle"] == angle)]
    outputPath = os.path.join(
        f"./data/{meas}/falling/", f"angle_{angle}{affix}.csv")
    df_falling.to_csv(outputPath, index=False)


if (__name__ == "__main__"):
    meas = "meas_3"
    filename = "Measurement_stretch_3"

    diodeFilename = filename + "_diode"

    if not os.path.exists(f'./data/{meas}'):
        os.makedirs(f'./data/{meas}')

    ModifyToCSV(filename)
    diodeCSV(diodeFilename)
    df = importCSV(f"./data/{meas}/{filename}.csv")
    splitAngles(df)

    df2 = importDiodeCSV(f"./data/{meas}/{diodeFilename}.csv")
    splitAngles(df2, affix="_diode")


RosetteCalc((350.06729,351.67155,350.57103), (350,350,350)) # 0
RosetteCalc((350.28975,351.61059,350.24055), (350,350,350)) # 15
RosetteCalc((350.44376,351.44695,349.94644), (350,350,350)) # 30
RosetteCalc((350.79562,351.09402,349.96355), (350,350,350)) # 45
RosetteCalc((351.10899,350.81701,350.06943), (350,350,350)) # 60
RosetteCalc((351.38920,350.55605,350.27050), (350,350,350)) # 75
RosetteCalc((351.59775,350.33467,350.59884), (350,350,350)) # 90