import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import scipy
import seaborn as sns
from sklearn.neighbors import LocalOutlierFactor

# --------------------------------------------------------------
# Load Data
# --------------------------------------------------------------
df = pd.read_pickle("../../data/interim/01_data_processed.pkl")

# --------------------------------------------------------------
# Plotting Outliers
# --------------------------------------------------------------
plt.style.use("fivethirtyeight")
plt.rcParams['figure.figsize'] = (20,10)
plt.rcParams['figure.dpi'] = 100

df[["acc_y", "label"]].boxplot(by="label", figsize=(20,10))
plt.show()



# --------------------------------------------------------------
# Load Data
# --------------------------------------------------------------




# --------------------------------------------------------------
# Load Data
# --------------------------------------------------------------