# 环境因素
import matplotlib.pyplot as plt
import re
import numpy as np
import pandas as pd

from matplotlib.pyplot import MultipleLocator

def rgb2hex(rgb):
	rgb = rgb.split(',')#将RGB格式划分开来
	hexes = '#'
	for i in rgb:
		num = int(i)
		hexes += str(hex(num))[-2:].replace('x','0').upper()
	return hexes


distance = {}
file_name = "../result/Fig-6_log"
for l in open(file_name, "r"):
	line = l.rstrip()
	name = line.split(" ")[0]
	if "distance" in line:
		if name not in distance:
			distance[name] = {}
		env = re.search(r"env0:(\S*)", line).group(1)
		if env not in distance[name]:
			distance[name][env] = []
		dis = float(re.search(r"distance:(\S*)", line).group(1))
		distance[name][env].append(dis)

# plt.rcParams['font.family'] = 'Times New Roman'
font_size = 12
fig = plt.figure(figsize=(4, 2.5), dpi=100)

ax:plt.Axes = plt.axes([0.14, 0.1, 0.8, 0.7])
ax.set_ylabel("Distance", fontsize=font_size-2, labelpad=0.8)
ax.set_ylim(-0.01, 0.1)

ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
ax.set_xticks([i for i in range(5)])
ax.set_xticklabels(["normal", "dry", "wet", "hot", "frozen"])
for x_tick_label_temp in ax.get_xticklabels():
	x_tick_label_temp.set_fontsize(font_size)

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

colors = ['#e6194B', '#3cb44b', '#911eb4', '#42d4f4', '#4363d8', '#f58231', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff', '#000000']

markers = ["*", "s", "o", "^", "p", "<"]
for k, task_name in enumerate(distance):
	envs = ["normal", "dry", "wet", "hot", "frozen"]
	dis = []
	for env in envs:
		dis.append(np.mean(distance[task_name][env]))
	ax.plot([i for i in range(len(dis))], dis, label=task_name, color=colors[k], marker=markers[k], markerfacecolor="white", alpha = 0.8)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.3), ncol=3, frameon=False, prop=dict(size=10))
plt.savefig("../picture/Fig-6.pdf",dpi=200, format="pdf", bbox_inches="tight", pad_inches=.02)
plt.show()
