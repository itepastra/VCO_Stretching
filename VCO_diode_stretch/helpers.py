from matplotlib import pyplot as plt
from matplotlib.rcsetup import cycler
import pandas as pd



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
