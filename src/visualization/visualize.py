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

# --------------------------------------------------------------
# Creating a loop to plot all combinations per sensor
# --------------------------------------------------------------
labels = df['label'].unique()
participants = df['participant'].unique()

for label in labels:
    for participant in participants:
        all_axis_df = (
            df.query(f"label=='{label}'")
            .query(f"participant=='{participant}'")
            .reset_index()
        )
         # Check if the resulting dataframe is empty
        if not all_axis_df.empty:
            # If it's not empty, create the plot
            fig, ax = plt.subplots()
            all_axis_df[['acc_y','acc_z','acc_x']].plot(ax=ax)
            ax.set(
                xlabel="Samples", 
                ylabel="acc_y",
                title=f"{label} ({participant})".title()
                )
            plt.legend()
        
# --------------------------------------------------------------
# Combine plot in one figure
# --------------------------------------------------------------

label='row'
participant = "A"
combined_plot_df = (
    df.query(f"label=='{label}'")
    .query(f"participant=='{participant}'")
    .reset_index(drop=True)
    )

fig, (ax1,ax2) = plt.subplots(nrows=2, sharex=True, figsize=(20,10))
combined_plot_df[['acc_y','acc_z','acc_x']].plot(ax=ax1)
combined_plot_df[['gyr_y','gyr_z','gyr_x']].plot(ax=ax2)

ax1.legend(loc="upper center", bbox_to_anchor=(0.5,1.15),ncols=3, fancybox=True, shadow=True)
ax2.legend(loc="upper center", bbox_to_anchor=(0.5,1.15),ncols=3, fancybox=True, shadow=True)
ax2.set_xlabel("samples")

# --------------------------------------------------------------
# Looping over all combinations and exporting for both sensors
# --------------------------------------------------------------
 
labels = df['label'].unique()
participants = df['participant'].unique()

for label in labels:
    for participant in participants:
        combined_plot_df = (
            df.query(f"label=='{label}'")
            .query(f"participant=='{participant}'")
            .reset_index()
        )
         # Check if the resulting dataframe is empty
        if not combined_plot_df.empty:
            fig, (ax1,ax2) = plt.subplots(nrows=2, sharex=True, figsize=(20,10))
            combined_plot_df[['acc_y','acc_z','acc_x']].plot(ax=ax1)
            combined_plot_df[['gyr_y','gyr_z','gyr_x']].plot(ax=ax2)
            
            ax2.set(xlabel="Samples")
            
            ax1.legend(loc="upper center", bbox_to_anchor=(0.5,1.15),ncols=3, fancybox=True, shadow=True)
            ax2.legend(loc="upper center", bbox_to_anchor=(0.5,1.15),ncols=3, fancybox=True, shadow=True)
            
            plt.savefig(f"../../reports/figures/{label.title()} ({participant}).png")
