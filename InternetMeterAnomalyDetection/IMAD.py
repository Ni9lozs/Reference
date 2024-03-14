import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ipywidgets import interact

df = pd.read_csv('C:/Users/bmikk/Desktop/rpi_data_processed.csv')

df_rates = df.drop(['Ping (ms)', 'Date', 'Time'], axis=1)

lookup = {'Download (Mbit/s)': 'download_rate',
          'Upload (Mbit/s)': 'upload_rate'}
df_rates = df_rates.rename(columns = lookup)

ping_rate = 1. / df['Ping (ms)']

ping_rate = 1000. * ping_rate

df_rates['ping_rate'] = ping_rate

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(df_rates['download_rate'], df_rates['upload_rate'], df_rates['ping_rate'], s=20, alpha=0.6)

ax.set_xlabel('Download Rate')
ax.set_ylabel('Upload Rate')
ax.set_zlabel('Ping Rate')

plt.show()

def scatter_view(x, y, z, azim, elev):
    fig = plt.figure(figsize=(8, 8))
    ax = Axes3D(fig)

    ax.scatter(x, y, z)
    ax.set_xlabel('D rate (Mbit/s)', fontsize=16)
    ax.set_ylabel('U rate (Mbit/s)', fontsize=16)
    ax.set_zlabel('P rate (1/s)', fontsize=16)

    ax.azim = azim
    ax.elev = elev

xi = df_rates['download_rate']
yi = df_rates['upload_rate']
zi = df_rates['ping_rate']
interact(lambda azim, elev: scatter_view(xi, yi, zi, azim, elev),
         azim=(0, 90), elev=(0, 90))
plt.show()

mu = df_rates.mean()

euclid_sq = np.square(df_rates - mu).sum(axis=1)
euclid = np.sqrt(euclid_sq)

fig = plt.figure(figsize=(7, 7))
distances = np.linalg.norm(df_rates - mu, axis=1)

fig = plt.figure(figsize=(7, 7))
plt.hist(distances, bins=25, edgecolor='black', alpha=0.7)

plt.xlabel('Euclidean distance', fontsize=16)
plt.ylabel('Relative frequency', fontsize=16)

max_euclid = distances.max()
nmd_euclid = distances / max_euclid

ecl_alarm_rate = []
nmd_range = np.linspace(0, 1, 400)
for nmd_decision in nmd_range:
    num_fail = np.sum(nmd_euclid > nmd_decision)
    alarm_rate = num_fail / len(df_rates)
    ecl_alarm_rate.append(alarm_rate)

fig = plt.figure(figsize=(7, 7))
plt.plot(nmd_range, ecl_alarm_rate, linewidth=2)
plt.xlabel('Normalized distance (Euclidean)', fontsize=16)
plt.ylabel('Alarm rate', fontsize=16)
plt.show()

threshold = 0.1
index, ecl_threshold = next(tpl for tpl in enumerate(ecl_alarm_rate) if tpl[1] < threshold)
ecl_decision = nmd_range[index]

fig = plt.figure(figsize=(7, 7))
plt.plot(nmd_range, ecl_alarm_rate, linewidth=2, label='Alarm Rate')
plt.plot(ecl_decision, ecl_threshold, 'bo', markersize=11, label='Decision Boundary')

plt.xlabel('Normalized distance (Euclidean)', fontsize=16)
plt.ylabel('Alarm rate', fontsize=16)

radius = ecl_decision * max_euclid
phi = np.linspace(0, 2 * np.pi, 300)
theta = np.linspace(0, 2 * np.pi, 300)

xs = radius * np.outer(np.sin(theta), np.cos(phi))
ys = radius * np.outer(np.sin(theta), np.sin(phi))
zs = radius * np.outer(np.cos(theta), np.ones(np.size(phi)))

ecl_xd = xs + df_rates['download_rate'].mean()
ecl_yd = ys + df_rates['upload_rate'].mean()
ecl_zd = zs + df_rates['ping_rate'].mean()

fig = plt.figure(figsize=(7, 7))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(df_rates['download_rate'],
           df_rates['upload_rate'],
           df_rates['ping_rate'])

ax.plot_surface(ecl_xd, ecl_yd, ecl_zd,
                linewidth=0, alpha=0.25)

ax.set_xlabel('D rate (Mbit/s)', fontsize=16)
ax.set_ylabel('U rate (Mbit/s)', fontsize=16)
ax.set_zlabel('P rate (1/s)', fontsize=16)

extremes = [
    [df_rates['download_rate'].min(), df_rates['download_rate'].max()],
    [df_rates['upload_rate'].min(), df_rates['upload_rate'].max()],
    [df_rates['ping_rate'].min(), df_rates['ping_rate'].max()]
]
hwidths = [(row[1] - row[0]) / 2.0 for row in extremes]
midpts = [(row[1] + row[0]) / 2.0 for row in extremes]

left_ends = midpts - np.max(hwidths)
right_ends = midpts + np.max(hwidths)
ax.set_xlim([left_ends[0], right_ends[0]])
ax.set_ylim([left_ends[1], right_ends[1]])
ax.set_zlim([left_ends[2], right_ends[2]])

plt.show()
