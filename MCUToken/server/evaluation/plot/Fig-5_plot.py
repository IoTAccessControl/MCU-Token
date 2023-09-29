import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import seaborn as sns

sys.path.append('../') 

# read_all_data(device_types=["esp32"], file_dir="all_data")
def rgb2hex(rgb):
	rgb = rgb.split(',')
	hexes = '#'
	for i in rgb:
		num = int(i)
		hexes += str(hex(num))[-2:].replace('x','0').upper()
	return hexes

df = pd.read_csv("../result/Fig-5_log")
df = df[df["arg1"] == 0]
df = df[df["arg2"] == 0]
df = df.reset_index(drop=True)

df = df[df["arg3"] % 25 == 0]
df = df[df["arg4"] == 0]
device_labels = [0, 1, 25, 3]

plt.rcParams.update({
	"text.usetex": False,
	"font.family": "sans-serif",
	# # "font.sans-serif": "Helvetica",
})
font_size = 14
fig = plt.figure(figsize=(4, 3), dpi=100)

ax:plt.Axes = plt.axes([0.14, 0.18, 0.8, 0.7])

ax.set_xlabel("Theory voltage", fontsize=font_size-4, labelpad=0.8)	
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
for x_tick_label_temp in ax.get_xticklabels():
	x_tick_label_temp.set_fontsize(font_size-2)
# y
ax.set_ylim(-0.01, 8500)
ax.set_ylabel("Read voltage", fontsize=font_size-4, labelpad=0.8)	
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
for y_tick_label_temp in ax.get_yticklabels():
	y_tick_label_temp.set_fontsize(font_size-2)

# boredr
ax.spines['left'].set_linewidth(.5)
ax.spines['bottom'].set_linewidth(.5)
ax.spines['right'].set_linewidth(.5)
ax.spines['top'].set_linewidth(.5)

legend_labels = ["device0", "device1", "", ""]
markers = ["o", "X", "*", "v"]
colors = ['#e6194B', '#3cb44b', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff', '#000000']
for i, label in enumerate(device_labels):
	ax.plot(df[df["label"] == label]["arg3"].values, df[df["label"] == label]["1"].values, label=legend_labels[i], marker=markers[i], markersize=4.0, linewidth=1, color=colors[i])
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2, frameon=False, prop=dict(size=font_size-2), columnspacing=3)
plt.savefig("../picture/Fig-5a.pdf",dpi=200, format="pdf", bbox_inches="tight", pad_inches=.02)
plt.show()


df = pd.read_csv("../result/Fig-5_log")
df = df[df["arg1"] == 0]
df = df[df["arg2"] == 0]
df = df[df["arg3"] == 125]
df = df[df["arg4"] == 0]
df = df.reset_index(drop=True)

device_vector = {}

for i, label in enumerate(device_labels):
  device_vector["device" + str(i)] = df[df["label"] == label][[str(i) for i in range(1, 11)]].values.reshape(-1)
  

plt.rcParams.update({
	"text.usetex": False,
	"font.family": "sans-serif",
	# # "font.sans-serif": "Helvetica",
})
font_size = 14
fig = plt.figure(figsize=(4, 3), dpi=100)

ax:plt.Axes = plt.axes([0.14, 0.18, 0.8, 0.713])

ax.set_xlabel("Output value", fontsize=font_size-4, labelpad=0.8)
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
for x_tick_label_temp in ax.get_xticklabels():
	x_tick_label_temp.set_fontsize(font_size-2)
# y
ax.set_ylim(-0.01, .34)
ax.set_ylabel("Density", fontsize=font_size-4, labelpad=0.8)	
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
for y_tick_label_temp in ax.get_yticklabels():
	y_tick_label_temp.set_fontsize(font_size-2)

# boredr
ax.spines['left'].set_linewidth(.5)
ax.spines['bottom'].set_linewidth(.5)
ax.spines['right'].set_linewidth(.5)
ax.spines['top'].set_linewidth(.5)

# df = pd.DataFrame(device_vector)
legend_labels = ["", "", "device2", "device3"]
for i, label in enumerate(device_labels):
	device_vector["device" + str(i)] = df[df["label"] == label][[str(i) for i in range(1, 11)]].values.reshape(-1)

	sns.kdeplot(ax=ax, data=df[df["label"] == label][[str(i) for i in range(1, 11)]].values.reshape(-1), fill=False, label=legend_labels[i], linewidth=1, marker=markers[i], markersize=4.0, markevery=20, color=colors[i])

ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2, frameon=False, prop=dict(size=font_size-2), columnspacing=3)
plt.savefig("../picture/Fig-5b.pdf",dpi=200, format="pdf", bbox_inches="tight", pad_inches=.02)
plt.show()
