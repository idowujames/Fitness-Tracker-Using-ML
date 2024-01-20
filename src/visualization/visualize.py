import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from IPython.display import display

# --------------------------------------------------------------
# Load Data
# --------------------------------------------------------------
df = pd.read_pickle("../../data/interim/01_data_processed.pkl")

# --------------------------------------------------------------
# Plot Single Columns
# --------------------------------------------------------------

set_df = df[df["set"] == 2]
plt.plot(set_df["acc_y"].reset_index(drop=True))

# --------------------------------------------------------------
# Plot All Exercises
# --------------------------------------------------------------

for label in df["label"].unique():
    subset = df[df["label"] == label]
    fig, ax = plt.subplots()
    plt.plot(subset["acc_y"].reset_index(drop=True), label=label)
    plt.legend()

# --------------------------------------------------------------
# Plot First 100 Exercises
# --------------------------------------------------------------
for label in df["label"].unique():
    subset = df[df["label"] == label]
    fig, ax = plt.subplots()
    plt.plot(subset[:100]["acc_y"].reset_index(drop=True), label=label)
    plt.legend()


# --------------------------------------------------------------
# Adjusting plot settings
# --------------------------------------------------------------
mpl.style.use("seaborn-v0_8-deep")
mpl.rcParams["figure.figsize"] = (20, 5)
mpl.rcParams["figure.dpi"] = 100

# --------------------------------------------------------------
# Comparing Medium and Heavy Sets
# --------------------------------------------------------------
category_df = df.query("label== 'squat'").query('participant=="A"').reset_index()

fig, ax = plt.subplots()
category_df.groupby(["category"])["acc_y"].plot()
ax.set(xlabel="Samples", ylabel="acc_y")
plt.legend()

# --------------------------------------------------------------
# Comparing Participants
# --------------------------------------------------------------

participant_df = df.query("label== 'bench'").sort_values('participant').reset_index()

fig, ax = plt.subplots()
participant_df.groupby(["participant"])["acc_y"].plot()
ax.set(xlabel="Samples", ylabel="acc_y")
plt.legend()

# --------------------------------------------------------------
# Plotting Multiple Axis
# --------------------------------------------------------------

label='squat'
participant = "A"
all_axis_df = df.query(f"label=='{label}'").query(f"participant=='{participant}'").reset_index()

fig, ax = plt.subplots()
all_axis_df[['acc_y','acc_z','acc_x']].plot(ax=ax)
ax.set(xlabel="Samples", ylabel="acc_y")
plt.legend()