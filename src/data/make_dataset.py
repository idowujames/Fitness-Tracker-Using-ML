import pandas as pd
from glob import glob

# --------------------------------------------------------------
# Read single CSV file
# --------------------------------------------------------------
# single_file_acc = pd.read_csv(
#     "../../data/raw/meta_motion_csv_files/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv"
# )

# single_file_gry = pd.read_csv(
#     "../../data/raw/meta_motion_csv_files/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv"
# )
# # --------------------------------------------------------------
# # List all data in data/raw/MetaMotion
# # --------------------------------------------------------------

# files = glob("../../data/raw/meta_motion_csv_files/*.csv")
# len(files)
# # --------------------------------------------------------------
# # Extract features from filename
# # --------------------------------------------------------------
# data_path = "../../data/raw/meta_motion_csv_files/"

# f = files[0]

# split_f = f.split("-")

# participant = split_f[0].replace(data_path, "")
# label = split_f[1]
# category = split_f[2].split("_")[0].rstrip("123")

# df = pd.read_csv(f)

# df["participant"] = participant
# df["label"] = label
# df["category"] = category

# # --------------------------------------------------------------
# # Read all files
# # --------------------------------------------------------------
# acc_df = pd.DataFrame()
# gyr_df = pd.DataFrame()


# acc_set = 1
# gyr_set = 1

# for f in files:
#     split_f = f.split("-")
#     participant = split_f[0].replace(data_path, "")
#     label = split_f[1]
#     category = split_f[2].split("_")[0].rstrip("123")

#     df = pd.read_csv(f)

#     df["participant"] = participant
#     df["label"] = label
#     df["category"] = category

#     if "Gyroscope" in f:
#         df["set"] = gyr_set
#         gyr_set += 1
#         gyr_df = pd.concat([gyr_df, df])

#     if "Accelerometer" in f:
#         df["set"] = acc_set
#         acc_set += 1
#         acc_df = pd.concat([acc_df, df])


# # --------------------------------------------------------------
# # Working with datetimes
# # --------------------------------------------------------------

# acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms")
# gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms")

# acc_df = acc_df.drop(columns=["epoch (ms)", "time (01:00)", "elapsed (s)"])
# gyr_df = gyr_df.drop(columns=["epoch (ms)", "time (01:00)", "elapsed (s)"])
# --------------------------------------------------------------
# Turn into function
# --------------------------------------------------------------
files = glob("../../data/raw/meta_motion_csv_files/*.csv")
data_path = "../../data/raw/meta_motion_csv_files/"


def read_data_from_files(files):
    acc_dfs = []
    gyr_dfs = []

    acc_set = 1
    gyr_set = 1

    for f in files:
        split_f = f.split("-")
        participant = split_f[0].replace(data_path, "")
        label = split_f[1]
        category = split_f[2].split("_")[0].rstrip("123")

        df = pd.read_csv(f)

        df["participant"] = participant
        df["label"] = label
        df["category"] = category

        if "Gyroscope" in f:
            df["set"] = gyr_set
            gyr_set += 1
            gyr_dfs.append(df)

        elif "Accelerometer" in f:
            df["set"] = acc_set
            acc_set += 1
            acc_dfs.append(df)

    acc_df = pd.concat(acc_dfs)
    gyr_df = pd.concat(gyr_dfs)

    acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms")
    gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms")

    acc_df = acc_df.drop(columns=["epoch (ms)", "time (01:00)", "elapsed (s)"])
    gyr_df = gyr_df.drop(columns=["epoch (ms)", "time (01:00)", "elapsed (s)"])

    return acc_df, gyr_df


acc_df, gyr_df = read_data_from_files(files)


# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------
data_merged = pd.concat([acc_df.iloc[:, :3], gyr_df], axis=1)

data_merged.columns = [
    "acc_x",
    "acc_y",
    "acc_z",
    "gyr_x",
    "gyr_y",
    "gyr_z",
    "participant",
    "label",
    "category",
    "set",
]

# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------
sampling = {
    "acc_y": "mean",
    "acc_z": "mean",
    "acc_x": "mean",
    "gyr_x": "mean",
    "gyr_y": "mean",
    "gyr_z": "mean",
    "participant": "last",
    "label": "last",
    "category": "last",
    "set": "last",
}

days = [g for n, g in data_merged.groupby(pd.Grouper(freq="D"))]

data_resampled = pd.concat(
    [df.resample(rule="200ms").apply(sampling).dropna() for df in days]
)

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz


# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------
