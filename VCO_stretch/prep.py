

import pandas as pd

meas="meas_2"

def ShuntCalc(voltageDiff: float, shuntResistance: float) -> float:
    # use ohm's law to calculate the current across the shunt
    return voltageDiff / shuntResistance


def ModifyToCSV(filename):
    print("heya")
    filePath = f"./measurements/{filename}"
    outputPath = f"./measurements_csv/{meas}/{filename}.csv"

    df = pd.read_csv(filePath, sep='\t', header=None)
    df.columns = ["date", "time", "Vctrl", "stretchAmt", "stretchAngle", "Freq1", "errFreq1", "Amp1", "errAmp1", "Freq2", "errFreq2", "Amp2", "errAmp2", "VDD_VCO1_shunt", "VDD_driver_shunt", "VDD", "VDD_VCO2_shunt", "VDD_ring_shunt", "strain_1", "strain_2", "strain_3", "temp"]

    print(df)

    df["VDD_VCO1_amps"] = ShuntCalc(df["VDD_VCO1_shunt"], 1000)
    df["VDD_VCO2_amps"] = ShuntCalc(df["VDD_VCO2_shunt"], 1000)
    df["VDD_driver_amps"] = ShuntCalc(df["VDD_driver_shunt"], 1000)
    df["VDD_ring_amps"] = ShuntCalc(df["VDD_ring_shunt"], 1000)

    df.to_csv(outputPath, index=False)


if (__name__ == "__main__"):
    ModifyToCSV("Measurement_stretch_2")