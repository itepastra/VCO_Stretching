import os
from matplotlib import pyplot as plt
from matplotlib.rcsetup import cycler
import pandas as pd

meas = "meas_2"


def importCSV(filepath, sortVctrl=True, maskFreqErr=1e99, maskApmErr=1e99):
    p_df = pd.read_csv(filepath,
                       sep=',',
                       skipinitialspace=True)
    # remove spaces in the column names
    p_df.columns = ((p_df.columns.str).strip()).str.strip()
    print(p_df.columns)
    # mask the necessary values
    return p_df.mask(p_df["errFreq1"] > maskFreqErr).mask(p_df["errAmp1"] > maskApmErr).mask(p_df["errFreq2"] > maskFreqErr).mask(p_df["errAmp2"] > maskApmErr)


def splitAngles(dataframe):

    for angle, df in dataframe.groupby("stretchAngle"):
        # create csv per angle
        diffs = df["stretchAmt"].diff()
        df["stretchDiffs"] = diffs.replace(0, pd.NA).ffill().fillna(0)
        outputPath = os.path.join(
            f"./measurements_csv/{meas}/angle/", f"angle_{angle}.csv")
        df.to_csv(outputPath, index=False)
        # create csv for the rising part of the angle
        splitRising(df, angle)
        splitFalling(df, angle)


def splitRising(dataframe, angle):
    # df = dataframe.copy().dropna()
    df_rising = dataframe[(dataframe["stretchDiffs"] >= 0)]
    outputPath = os.path.join(
        f"./measurements_csv/{meas}/rising/", f"angle_{angle}.csv")
    df_rising.to_csv(outputPath, index=False)


def splitFalling(dataframe, angle):
    max_stretch_amt = dataframe["stretchAmt"].max()
    df_falling = dataframe[(dataframe["stretchDiffs"] < 0) | (
        dataframe["stretchAmt"] == max_stretch_amt) & (dataframe["stretchAngle"] == angle)]
    outputPath = os.path.join(
        f"./measurements_csv/{meas}/falling/", f"angle_{angle}.csv")
    df_falling.to_csv(outputPath, index=False)


if __name__ == '__main__':
    df = importCSV(f"./measurements_csv/{meas}/Measurement_stretch_2.csv")
    splitAngles(df)
