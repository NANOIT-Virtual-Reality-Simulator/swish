from numpy.ma import sqrt, mean, cumsum

__author__ = 'Nitin'

import pandas as pd
import matplotlib.pyplot as plt

#Given the raw readings in csv from the pebble, we need to isolate the 'swings'
#We do this by taking a threshold based on standard deviations from the median
#Number of standard deviations and filter thresholds may vary by shot type (e.g. a drop will have less accel than a drive)
#This may need some optimisation, e.g. walking until change in direction or setting a minimum valid swing time

shots = ['backhand-drive', 'forehand-drive-volley']
displacement_dfs = []
for shot in shots:
    k = 1.5
    spike_threshold = 3000
    min_time_between_shots = 50

    full_df = pd.read_csv('data/' + shot + 's.csv')

    #IMPORTANT NOTE: The mean is REALLY bad because of the spikes.
    #The spikes are the outliers we want to detect, so we can't be influenced by them.
    #We want the threshold to ignore spikes, so we calculate everything with median, including the std
    x_filtered_df = full_df[abs(full_df.x - full_df.x.median()) > (k * sqrt(mean(abs(full_df.x - full_df.x.median())**2)))]
    y_filtered_df = full_df[abs(full_df.y - full_df.y.median()) > (k * sqrt(mean(abs(full_df.y - full_df.y.median())**2)))]
    z_filtered_df = full_df[abs(full_df.z - full_df.z.median()) > (k * sqrt(mean(abs(full_df.z - full_df.z.median())**2)))]

    filtered_dfs = [x_filtered_df, y_filtered_df, z_filtered_df]
    filtered_df = pd.concat(filtered_dfs)
    final_df = filtered_df.sort_values("time")

    #filtered_df.plot(x='time')
    #plt.show()

    split_dfs = []
    swing_start = 0
    for i in range(len(final_df.index)-2):
        time_now = final_df.iloc[i].time
        time_next = final_df.iloc[i+1].time
        if time_next - time_now > min_time_between_shots:
            split_dfs.append(final_df.iloc[swing_start: i])
            swing_start = i+1

    #FIXME: there's gotta be a better way of doing this...
    shot_dfs = [split_df for split_df in split_dfs
                if len(split_df.index) > 0
                and (split_df.x.values.max() > spike_threshold or split_df.x.values.min < -spike_threshold
                     or split_df.y.values.max() > spike_threshold or split_df.y.values.min() < -spike_threshold
                     or split_df.z.values.max() > spike_threshold or split_df.z.values.min() < -spike_threshold)]

    print len(shot_dfs)
    #for shot_df in shot_dfs:
    #    shot_df.plot(x="time")
    #    plt.show()

    #Now we calculate the displacement on each axis for each shot
    #Assume the initial velocity is 0, then s = 0.5a(dt)^2
    x_displacements = []
    y_displacements = []
    z_displacements = []
    for shot_df in shot_dfs:
        ts = shot_df.time.values
        dts = [j-i for i, j in zip(ts[:-1], ts[1:])]
        i_s = range(len(dts)-1)
        x_s = cumsum([0.5*shot_df.x.values[i]*dts[i]*dts[i] for i in i_s])
        y_s = cumsum([0.5*shot_df.y.values[i]*dts[i]*dts[i] for i in i_s])
        z_s = cumsum([0.5*shot_df.z.values[i]*dts[i]*dts[i] for i in i_s])
        x_displacements.append([i_s, x_s])
        y_displacements.append([i_s, y_s])
        z_displacements.append([i_s, z_s])

    for i_s, x_s in x_displacements:
        plt.scatter(i_s, x_s, c='Red', label='x', alpha=0.5)

    for i_s, y_s in y_displacements:
        plt.scatter(i_s, y_s, c='Blue', label='y', alpha=0.5)

    for i_s, z_s in z_displacements:
        plt.scatter(i_s, z_s, c='Green', label='z', alpha=0.5)

    plt.show()

    displacement_dfs.append(pd.DataFrame({
        'x': x_displacements,
        'y': y_displacements,
        'z': z_displacements,
        'shot': shot
    }))

    # displacement_dfs.append(pd.DataFrame({
    #     'x-'+shot: x_displacements,
    #     'y-'+shot: y_displacements,
    #     'z-'+shot: z_displacements,
    #     'i': range(len(x_displacements))
    # }))


merged_displacement_dfs = pd.concat(displacement_dfs)