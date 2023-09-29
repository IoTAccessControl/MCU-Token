# 多特征的攻击
import matplotlib.pyplot as plt
import re
import numpy as np
import pandas as pd

from matplotlib.pyplot import MultipleLocator

def rgb2hex(rgb):
	rgb = rgb.split(',')
	hexes = '#'
	for i in rgb:
		num = int(i)
		hexes += str(hex(num))[-2:].replace('x','0').upper()
	return hexes

plt.rcParams.update({
	"text.usetex": False,
	"font.family": "sans-serif",
	# "font.sans-serif": "Helvetica",
})
font_size = 14
fig = plt.figure(figsize=(4.5, 3), dpi=100)

file_name = "../result/Fig-9a_log"
attack_multiple = {}
for l in open(file_name, "r"):
	line = l.rstrip()
	name = line.split(" ")[0]
	if name == "attack-multiple" and "method" in line:
		used_task_number = int(re.search(r"used_task_number:(\S*)", line).group(1))
		method = re.search(r"method:(\S*)", line).group(1)
		SR = float(re.search(r"SR:(\S*)", line).group(1))
		train_time = float(re.search(r"train_time:(\S*)", line).group(1))
		if method not in attack_multiple:
			attack_multiple[method] = {}
			attack_multiple[method]["used_task_number"] = []
			attack_multiple[method]["SR"] = []
			attack_multiple[method]["train_time"] = []
		attack_multiple[method]["used_task_number"].append(used_task_number)
		attack_multiple[method]["SR"].append(SR)
		attack_multiple[method]["train_time"].append(train_time)

ax:plt.Axes = plt.axes([0.2, 0.13, 0.6, 0.7])
# titile
ax.set_xlabel("$used\_num$", fontsize=font_size, labelpad=0.1)
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
for x_tick_label_temp in ax.get_xticklabels():
	x_tick_label_temp.set_fontsize(font_size)
# y
ax.set_ylim(-0.01, .4)
ax.yaxis.set_major_locator(MultipleLocator(.2))
ax.set_ylabel("Success Rate (SR)", fontsize=font_size, labelpad=0.8)
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

colors = ['#f032e6', '#000075', '#469990', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#bfef45', '#a9a9a9', '#ffffff', '#000000']
colors = ['#e6194B', '#3cb44b', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff', '#000000']
markers = ["H", "X", "D", "v"]
labels = ["none", "", "", ""]
for i, method in enumerate(attack_multiple):
	used_task_number = attack_multiple[method]["used_task_number"]
	SR = attack_multiple[method]["SR"]
	x_len = len(np.unique(used_task_number))
	used_task_number = np.array(used_task_number).reshape(-1, x_len)
	used_task_number = np.mean(used_task_number, axis=0)
	SR = np.array(SR).reshape(-1, x_len)
	SR = np.mean(SR, axis=0)
	ax.plot(used_task_number, SR, label=labels[i], color=colors[i], linewidth=1.2, markersize=6.0, marker=markers[i], markerfacecolor="white", alpha = 0.8)
ax.legend(loc='upper center', bbox_to_anchor=(0.7, 1.18), ncol=1, frameon=False, prop=dict(size=font_size))
plt.savefig("../picture/Fig-9a.pdf",dpi=200, format="pdf", bbox_inches="tight", pad_inches=.02)
plt.show()
plt.close()

# accept_num
plt.rcParams.update({
	"text.usetex": False,
	"font.family": "sans-serif",
	# "font.sans-serif": "Helvetica",
})
font_size = 14
fig = plt.figure(figsize=(4.5, 3), dpi=100)

file_name = "../result/Fig-9b_log"
attack_multiple = {}
for l in open(file_name, "r"):
	line = l.rstrip()
	name = line.split(" ")[0]
	if name == "attack-multiple" and "method" in line:
		accept_low_bound = int(re.search(r"accept_low_bound:(\S*)", line).group(1))
		method = re.search(r"method:(\S*)", line).group(1)
		SR = float(re.search(r"SR:(\S*)", line).group(1))
		train_time = float(re.search(r"train_time:(\S*)", line).group(1))
		if method not in attack_multiple:
			attack_multiple[method] = {}
			attack_multiple[method]["accept_low_bound"] = []
			attack_multiple[method]["SR"] = []
			attack_multiple[method]["train_time"] = []
		attack_multiple[method]["accept_low_bound"].append(accept_low_bound)
		attack_multiple[method]["SR"].append(SR)
		attack_multiple[method]["train_time"].append(train_time)

ax:plt.Axes = plt.axes([0.2, 0.13, 0.6, 0.7])
# titile
# ax.set_title(r"(b) Attack with differnet K", y=-0.3, fontdict=dict(size=font_size))
# x
ax.set_xlabel("$accept\_num$", fontsize=font_size, labelpad=0.1)
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
for x_tick_label_temp in ax.get_xticklabels():
	x_tick_label_temp.set_fontsize(font_size)
# y
ax.set_ylim(-0.01, .45)
ax.yaxis.set_major_locator(MultipleLocator(.2))
ax.set_ylabel("Success Rate (SR)", fontsize=font_size, labelpad=0.8)
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

labels = ["", "filter", "correct", ""]
for i, method in enumerate(attack_multiple):
	accept_low_bound = attack_multiple[method]["accept_low_bound"]
	SR = attack_multiple[method]["SR"]
	x_len = len(np.unique(accept_low_bound))
	accept_low_bound = np.array(accept_low_bound).reshape(-1, x_len)
	accept_low_bound = np.mean(accept_low_bound, axis=0)
	SR = np.array(SR).reshape(-1, x_len)
	SR = np.mean(SR, axis=0)
	ax.plot(accept_low_bound, SR, label=labels[i], color=colors[i], linewidth=1.2, markersize=6.0, marker=markers[i], markerfacecolor="white", alpha = 0.8)
ax.legend(columnspacing=4, loc='upper center', bbox_to_anchor=(0.4, 1.18), ncol=2, frameon=False, prop=dict(size=font_size))
plt.savefig("../picture/Fig-9b.pdf",dpi=200, format="pdf", bbox_inches="tight", pad_inches=.02)
plt.show()
plt.close()

# ratio
plt.rcParams.update({
	"text.usetex": False,
	"font.family": "sans-serif",
	# "font.sans-serif": "Helvetica",
})
font_size = 14
fig = plt.figure(figsize=(4.5, 3), dpi=100)

file_name = "../result/Fig-9c_log"
attack_multiple = {}
for l in open(file_name, "r"):
	line = l.rstrip()
	name = line.split(" ")[0]
	if name == "attack-multiple" and "method" in line:
		method = re.search(r"method:(\S*)", line).group(1)
		SR = float(re.search(r"SR:(\S*)", line).group(1))
		if method not in attack_multiple:
			attack_multiple[method] = {}
			attack_multiple[method]["SR"] = []
			attack_multiple[method]["use_rate"] = []
		attack_multiple[method]["SR"].append(SR)
		attack_multiple[method]["use_rate"].append(use_rate)
	elif "Training OK" in line:
		try:
			t = use_rate + 1
		except:
			use_rate = 0
		use_rate = 0.1 + use_rate
			
ax:plt.Axes = plt.axes([0.2, 0.13, 0.6, 0.7])
# titile
# ax.set_title(r"(c) Attack with different ratio", y=-0.3, fontdict=dict(size=font_size))
# x
ax.set_xlabel("Ratio of used pairs", fontsize=font_size, labelpad=0.1)
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
for x_tick_label_temp in ax.get_xticklabels():
	x_tick_label_temp.set_fontsize(font_size)
# y
ax.set_ylim(-0.01, .45)
ax.yaxis.set_major_locator(MultipleLocator(.2))
ax.set_ylabel("Success Rate (SR)", fontsize=font_size, labelpad=0.8)
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

labels = ["", "", "", "filter + correct"]
for i, method in enumerate(attack_multiple):
	use_rate = attack_multiple[method]["use_rate"]
	SR = attack_multiple[method]["SR"]
	x_len = len(np.unique(use_rate))
	use_rate = np.array(use_rate).reshape(-1, x_len)
	use_rate = np.mean(use_rate, axis=0)
	SR = np.array(SR).reshape(-1, x_len)
	SR = np.mean(SR, axis=0)
	ax.plot(use_rate, SR, label=labels[i], color=colors[i], linewidth=1.2, markersize=6.0, marker=markers[i], markerfacecolor="white", alpha = 0.8)
ax.legend(loc='upper center', bbox_to_anchor=(0.2, 1.18), ncol=2, frameon=False, prop=dict(size=font_size))
lines, labels = ax.get_legend_handles_labels()
plt.savefig("../picture/Fig-9c.pdf",dpi=200, format="pdf", bbox_inches="tight", pad_inches=.02)
plt.show()
plt.close()