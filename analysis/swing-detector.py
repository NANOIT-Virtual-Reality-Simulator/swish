from numpy.ma import sqrt, mean

__author__ = 'Nitin'

import pandas as pd
import matplotlib.pyplot as plt

#Given the raw readings in csv from the pebble, we need to isolate the 'swings'
#We do this by taking a threshold based on standard deviations from the median
#Number of standard deviations and filter thresholds vary by shot type (e.g a drop will have less accel than a drive)
#This may need some optimisation, e.g. walking until change in direction or setting a minimum valid swing time

k = 1
spike_threshold = 3000

#full_df = pd.read_csv('data/backhand-drives.csv')
full_df = pd.read_csv('data/forehand-drive-volleys.csv')

#NOTE: The mean is really bad because of the spikes.
#We want the threshold to ignore spikes, so we calculate everything with median, including the std
x_filtered_df = full_df[abs(full_df.x - full_df.x.median()) > (k * sqrt(mean(abs(full_df.x - full_df.x.median())**2)))]
y_filtered_df = full_df[abs(full_df.y - full_df.y.median()) > (k * sqrt(mean(abs(full_df.x - full_df.x.median())**2)))]
z_filtered_df = full_df[abs(full_df.z - full_df.z.median()) > (k * sqrt(mean(abs(full_df.x - full_df.x.median())**2)))]

filtered_dfs = [x_filtered_df, y_filtered_df, z_filtered_df]
filtered_df = pd.concat(filtered_dfs)
final_df = filtered_df.sort_values("time")

filtered_df.plot(x='time')
plt.show()

split_dfs = []
start = 0
for i in range(len(final_df.index)-2):
    time_now = final_df.iloc[i].time
    time_next = final_df.iloc[i+1].time
    if time_next - time_now > 50:
        split_dfs.append(final_df.iloc[start: i])
        start = i+1

print len(split_dfs)
shot_dfs = [split_df for split_df in split_dfs
            if len(split_df.index) > 0
            and (split_df.x.values.max() > spike_threshold or split_df.x.values.min < -spike_threshold
                 or split_df.y.values.max() > spike_threshold or split_df.y.values.min() < -spike_threshold
                 or split_df.z.values.max() > spike_threshold or split_df.z.values.min() < -spike_threshold)]
print len(shot_dfs)

for shot_df in shot_dfs:
    shot_df.plot(x="time")
    plt.show()


