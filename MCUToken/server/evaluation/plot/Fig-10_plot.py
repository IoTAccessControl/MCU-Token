# 单特征的攻击
import matplotlib.pyplot as plt
import re
import numpy as np
import os

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

# unprotected
file_name = "../result/Fig-10a_log"
single_attack = {}

for l in open(file_name, "r"):
	line = l.rstrip()
	name = line.split(" ")[0]
	if name == "single-attack":
		task = re.search(r"task:(\S*)", line).group(1)
		rate = float(re.search(r"rate:(\S*)", line).group(1))
		SR = float(re.search(r"SR:(\S*)", line).group(1))
		if task not in single_attack:
			single_attack[task] = {}
			single_attack[task]["rate"] = []
			single_attack[task]["SR"] = []
		single_attack[task]["rate"].append(rate)
		single_attack[task]["SR"].append(SR)

ax:plt.Axes = plt.axes([0.2, 0.13, 0.6, 0.7])
# titile
# ax.set_title(r"(a) Attack without protection", y=-0.3, fontdict=dict(size=font_size))
# x
ax.set_xlabel("Ratio of used pairs", fontsize=font_size-2, labelpad=0.1)
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
for x_tick_label_temp in ax.get_xticklabels():
	x_tick_label_temp.set_fontsize(font_size)
# y
ax.set_ylim(-0.01, 0.92)
ax.yaxis.set_major_locator(MultipleLocator(.2))
ax.set_ylabel("Success Rate (SR)", fontsize=font_size-2, labelpad=0.8)
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
labels = [list(single_attack.keys())[i] if i == 0 else "" for i in range(len(single_attack))]
for i, task in enumerate(single_attack):
	rate = single_attack[task]["rate"]
	x_len = len(np.unique(rate))
	rate = np.array(rate).reshape(-1, x_len)
	rate = np.mean(rate, axis=0)
	SR = single_attack[task]["SR"]
	SR = np.array(SR).reshape(-1, x_len)
	SR = np.mean(SR, axis=0)
	ax.plot(rate, SR, label=labels[i], color=colors[i], linewidth=1.2, markersize=6.0, marker=markers[i], markerfacecolor="white", alpha = 0.8)
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=2, frameon=False, prop=dict(size=10))
ax.legend(loc='upper center', bbox_to_anchor=(0.7, 1.18), ncol=1, frameon=False, prop=dict(size=font_size))
plt.savefig("../picture/Fig-10a.pdf",dpi=200, format="pdf", bbox_inches="tight", pad_inches=.02)
plt.show()
plt.close()

# 有保护的
plt.rcParams.update({
	"text.usetex": False,
	"font.family": "sans-serif",
	# "font.sans-serif": "Helvetica",
})
font_size = 14
fig = plt.figure(figsize=(4.5, 3), dpi=100)

SR_degenerate = {}
file_name = "../result/Fig-10b_log"
for l in open(file_name, "r"):
	line = l.rstrip()
	name = line.split(" ")[0]
	if name == "attack-multiple" and "method" in line:
		method = re.search(r"method:(\S*)", line).group(1)
	elif name == "attack-multiple" and "SR_degenerate" in line:
		task = re.search(r"task:(\S*)", line).group(1)
		if task not in SR_degenerate:
			SR_degenerate[task] = {}
			SR_degenerate[task]["method"] = []
			SR_degenerate[task]["use_rate"] = []
			SR_degenerate[task]["SR"] = []
		SR_degenerate[task]["method"].append(method)
		SR = float(re.search(r"SR_degenerate:(\S*)", line).group(1))
		SR_degenerate[task]["SR"].append(SR)
		SR_degenerate[task]["use_rate"].append(use_rate)
	elif "use_rate" in line:
		use_rate = round(float(re.search(r"use_rate:(\S*)", line).group(1)), 1)
		
			
ax:plt.Axes = plt.axes([0.2, 0.13, 0.6, 0.7])	
# titile
# ax.set_title(r"(b) Attack with protection", y=-0.3, fontdict=dict(size=font_size))
# x
ax.set_xlabel("Ratio of used pairs", fontsize=font_size-2, labelpad=0.1)
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
for x_tick_label_temp in ax.get_xticklabels():
	x_tick_label_temp.set_fontsize(font_size)
# y
ax.set_ylim(-0.01, .92)
ax.yaxis.set_major_locator(MultipleLocator(.2))
ax.set_ylabel("Success Rate (SR)", fontsize=font_size-2, labelpad=0.8)
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

labels = [list(single_attack.keys())[i] if i == 1 else "" for i in range(len(single_attack))]
for i, task in enumerate(SR_degenerate):
	method = SR_degenerate[task]["method"]
	x_len = len(np.unique(method))
	method = np.array(method).reshape(-1, x_len)
	use_rate = SR_degenerate[task]["use_rate"]
	use_rate = np.array(use_rate).reshape(-1, x_len)
	SR = SR_degenerate[task]["SR"]
	SR = np.array(SR).reshape(-1, x_len)
	use_rate = np.mean(use_rate, axis=1)
	SR = np.max(SR, axis=1)
	x_len = len(set(use_rate))
	use_rate = use_rate.reshape(-1, x_len)
	use_rate = np.mean(use_rate, axis=0)
	SR = SR.reshape(-1, x_len)
	SR = np.mean(SR, axis=0)
	ax.plot(use_rate, SR, label=labels[i], color=colors[i], linewidth=1.2, markersize=6.0, marker=markers[i], markerfacecolor="white", alpha = 0.8)
ax.legend(loc='upper center', bbox_to_anchor=(0.6, 1.18), ncol=1, frameon=False, prop=dict(size=font_size))
plt.savefig("../picture/Fig-10b.pdf",dpi=200, format="pdf", bbox_inches="tight", pad_inches=.02)
plt.show()
plt.close()

plt.rcParams.update({
	"text.usetex": False,
	"font.family": "sans-serif",
	# "font.sans-serif": "Helvetica",
})
font_size = 14
fig = plt.figure(figsize=(4.5, 3), dpi=100)
file_name = "../result/Fig-10c_log"
SR_degenerate = {}
for l in open(file_name, "r"):
	line = l.rstrip()
	name = line.split(" ")[0]
	if name == "attack-multiple" and "method" in line:
		method = re.search(r"method:(\S*)", line).group(1)
		used_task_number = int(re.search(r"used_task_number:(\S*)", line).group(1))
	elif name == "attack-multiple" and "SR_degenerate" in line:
		task = re.search(r"task:(\S*)", line).group(1)
		if task not in SR_degenerate:
			SR_degenerate[task] = {}
			SR_degenerate[task]["method"] = []
			SR_degenerate[task]["use_rate"] = []
			SR_degenerate[task]["SR"] = []
			SR_degenerate[task]["used_task_number"] = []
		SR_degenerate[task]["method"].append(method)
		SR_degenerate[task]["used_task_number"].append(used_task_number)
		SR = float(re.search(r"SR_degenerate:(\S*)", line).group(1))
		SR_degenerate[task]["SR"].append(SR)
		SR_degenerate[task]["use_rate"].append(use_rate)
	elif "--rate_control" in line:
		use_rate = float(re.search(r"--rate_control (\S*)", line).group(1))

ax:plt.Axes = plt.axes([0.2, 0.13, 0.6, 0.7])	
# titile
# ax.set_title(r"(c) Attack with different N", y=-0.3, fontdict=dict(size=font_size))
# x
ax.set_xlabel("$used\_num$", fontsize=font_size-2, labelpad=0.1)
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
for x_tick_label_temp in ax.get_xticklabels():
	x_tick_label_temp.set_fontsize(font_size)
# y
ax.set_ylim(-0.01, .92)
ax.yaxis.set_major_locator(MultipleLocator(.2))
ax.set_ylabel("Success Rate (SR)", fontsize=font_size-2, labelpad=0.8)
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

labels = [list(single_attack.keys())[i] if i == 2 else "" for i in range(len(single_attack))]
for i, task in enumerate(SR_degenerate):
	method = SR_degenerate[task]["method"]
	x_len = len(np.unique(method))
	method = np.array(method).reshape(-1, x_len)
	used_task_number = SR_degenerate[task]["used_task_number"]
	used_task_number = np.array(used_task_number).reshape(-1, x_len)
	SR = SR_degenerate[task]["SR"]
	SR = np.array(SR).reshape(-1, x_len)
	used_task_number = np.mean(used_task_number, axis=1)
	SR = np.max(SR, axis=1)
	ax.plot(used_task_number, SR, label=labels[i], color=colors[i], linewidth=1.2, markersize=6.0, marker=markers[i], markerfacecolor="white", alpha = 0.8)
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=2, frameon=False, prop=dict(size=10))
ax.legend(loc='upper center', bbox_to_anchor=(0.4, 1.18), ncol=1, frameon=False, prop=dict(size=font_size))
plt.savefig("../picture/Fig-10c.pdf",dpi=200, format="pdf", bbox_inches="tight", pad_inches=.02)
plt.show()
plt.close()

# 不同的K
plt.rcParams.update({
	"text.usetex": False,
	"font.family": "sans-serif",
	# "font.sans-serif": "Helvetica",
})
font_size = 14
fig = plt.figure(figsize=(4.5, 3), dpi=100)
SR_degenerate = {}
file_name = "../result/Fig-10d_log"
for l in open(file_name, "r"):
	line = l.rstrip()
	name = line.split(" ")[0]
	if name == "attack-multiple" and "method" in line:
		method = re.search(r"method:(\S*)", line).group(1)
		accept_low_bound = int(re.search(r"accept_low_bound:(\S*)", line).group(1))
	elif name == "attack-multiple" and "SR_degenerate" in line:
		task = re.search(r"task:(\S*)", line).group(1)
		if task not in SR_degenerate:
			SR_degenerate[task] = {}
			SR_degenerate[task]["method"] = []
			SR_degenerate[task]["use_rate"] = []
			SR_degenerate[task]["SR"] = []
			SR_degenerate[task]["accept_low_bound"] = []
		SR_degenerate[task]["method"].append(method)
		SR_degenerate[task]["accept_low_bound"].append(accept_low_bound)
		SR = float(re.search(r"SR_degenerate:(\S*)", line).group(1))
		SR_degenerate[task]["SR"].append(SR)
		SR_degenerate[task]["use_rate"].append(use_rate)
	elif "--rate_control" in line:
		use_rate = float(re.search(r"--rate_control (\S*)", line).group(1))

ax:plt.Axes = plt.axes([0.2, 0.13, 0.6, 0.7])

# ax.set_title(r"(d) Attack with different K", y=-0.3, fontdict=dict(size=font_size))
# x
ax.set_xlabel("$accept\_nun$", fontsize=font_size-2, labelpad=0.1)
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
for x_tick_label_temp in ax.get_xticklabels():
	x_tick_label_temp.set_fontsize(font_size)
# y
ax.set_ylim(-0.01, .92)
ax.yaxis.set_major_locator(MultipleLocator(.2))
ax.set_ylabel("Success Rate (SR)", fontsize=font_size-2, labelpad=0.8)
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

labels = [list(single_attack.keys())[i] if i == 3 else "" for i in range(len(single_attack))]
for i, task in enumerate(SR_degenerate):
	method = SR_degenerate[task]["method"]
	x_len = len(np.unique(method))
	method = np.array(method).reshape(-1, x_len)
	accept_low_bound = SR_degenerate[task]["accept_low_bound"]
	accept_low_bound = np.array(accept_low_bound).reshape(-1, x_len)
	SR = SR_degenerate[task]["SR"]
	SR = np.array(SR).reshape(-1, x_len)
	accept_low_bound = np.mean(accept_low_bound, axis=1)
	SR = np.max(SR, axis=1)
	x_len = len(set(accept_low_bound))
	accept_low_bound = accept_low_bound.reshape(-1, x_len)
	accept_low_bound = np.mean(accept_low_bound, axis=0)
	SR = SR.reshape(-1, x_len)
	SR = np.mean(SR, axis=0)
	ax.plot(accept_low_bound, SR, label=labels[i], color=colors[i], linewidth=1.2, markersize=6.0, marker=markers[i], markerfacecolor="white", alpha = 0.8)
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=2, frameon=False, prop=dict(size=10))
lines, labels = ax.get_legend_handles_labels()
ax.legend(loc='upper center', bbox_to_anchor=(0.2, 1.18), ncol=1, frameon=False, prop=dict(size=font_size))
plt.savefig("../picture/Fig-10d.pdf",dpi=200, format="pdf", bbox_inches="tight", pad_inches=.02)
plt.show()
plt.close()
