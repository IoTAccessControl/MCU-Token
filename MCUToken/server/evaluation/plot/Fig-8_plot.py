import matplotlib.pyplot as plt
import re
import numpy as np
import pandas as pd

from matplotlib.pyplot import MultipleLocator

plt.rcParams.update({
	"text.usetex": False,
	"font.family": "sans-serif",
	# "font.sans-serif": "Helvetica",
})
font_size = 14
fig = plt.figure(figsize=(4.5, 3), dpi=100)

file_name = "../result/Fig-8_log"
noise_test = {}
for l in open(file_name, "r"):
	line = l.rstrip()
	name = line.split(" ")[0]
	if name == "noise-test":
		task = re.search(r"task:(\S*)", line).group(1).replace(",", "")
		TP = float(re.search(r"TP:(\S*)", line).group(1).replace(",", ""))
		FN = float(re.search(r"FN:(\S*)", line).group(1).replace(",", ""))
		noise = float(re.search(r"noise:(\S*)", line).group(1).replace(",", ""))
		if task not in noise_test:
			noise_test[task] = {}
			noise_test[task]["TP"] = []
			noise_test[task]["FN"] = []
			noise_test[task]["noise"] = []
		noise_test[task]["TP"].append(TP)
		noise_test[task]["FN"].append(FN)
		noise_test[task]["noise"].append(noise)
	elif name == "closed-world-test":
		task = re.search(r"task:(\S*)", line).group(1).replace(",", "")
		TP = float(re.search(r"TP:(\S*)", line).group(1).replace(",", ""))
		FN = float(re.search(r"FN:(\S*)", line).group(1).replace(",", ""))
		noise = 0
		if task not in noise_test:
			noise_test[task] = {}
			noise_test[task]["TP"] = []
			noise_test[task]["FN"] = []
			noise_test[task]["noise"] = []
		noise_test[task]["TP"].append(TP)
		noise_test[task]["FN"].append(FN)
		noise_test[task]["noise"].append(noise)

ax:plt.Axes = plt.axes([0.2, 0.13, 0.6, 0.71])
# titile
# ax.set_title(r"(d) Authenticating with poisonous pairs", y=-0.3, fontdict=dict(size=font_size))
# x
ax.set_xlabel("Noise", fontsize=font_size, labelpad=0.1)
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
for x_tick_label_temp in ax.get_xticklabels():
	x_tick_label_temp.set_fontsize(font_size)
# y
ax.set_ylim(-0.01, 1.05)
ax.yaxis.set_major_locator(MultipleLocator(.2))
ax.xaxis.set_major_locator(MultipleLocator(.02))
ax.set_ylabel("TPR", fontsize=font_size, labelpad=0.8)
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
for y_tick_label_temp in ax.get_yticklabels():
	y_tick_label_temp.set_fontsize(font_size)
# grid
ax.grid(which='major',ls='--',alpha=.8,lw=.2)
# boredr
ax.spines['left'].set_linewidth(.5)
ax.spines['bottom'].set_linewidth(.5)
ax.spines['right'].set_linewidth(.5)
ax.spines['top'].set_linewidth(.5)

colors = ['#e6194B', '#3cb44b', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff', '#000000']


markers = ["*", "s", "p", "<"]
for i, task in enumerate(noise_test):
	TP = noise_test[task]["TP"]
	FN = noise_test[task]["FN"]
	noise = noise_test[task]["noise"]
	x_len = len(np.unique(noise))
	noise = np.array(noise).reshape(-1, x_len)
	noise = np.mean(noise, axis=0)
	TP = np.array(TP).reshape(-1, x_len)
	TP = np.mean(TP, axis=0)
	FN = np.array(FN).reshape(-1, x_len)
	FN = np.mean(FN, axis=0)
	ax.plot(noise, TP / (TP + FN), label=task, color=colors[i], linewidth=1.2, markersize=6.0, marker=markers[i], markerfacecolor="white", alpha = 0.8)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.26), ncol=2, frameon=False, prop=dict(size=font_size-2))
plt.savefig("../picture/Fig-8.pdf",dpi=800, format="pdf", bbox_inches="tight", pad_inches=.01)
plt.show()