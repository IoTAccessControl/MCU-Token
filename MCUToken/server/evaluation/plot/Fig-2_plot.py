import matplotlib.pyplot as plt
import re
import numpy as np

from matplotlib.pyplot import MultipleLocator

def rgb2hex(rgb):
	rgb = rgb.split(',')
	hexes = '#'
	for i in rgb:
		num = int(i)
		hexes += str(hex(num))[-2:].replace('x','0').upper()
	return hexes

obtains_num_sr = {}
obtains_dim_sr = {}
for l in open("../result/Fig-2_log", "r"):
	line = l.rstrip()
	if "obtain" in line:
		obtain = int(re.search(r"obtain:(\S*)", line).group(1).replace(",", ""))
		success = int(re.search(r"success: (\S*)", line).group(1).replace("", ""))
		if obtain not in obtains_num_sr:
			obtains_num_sr[obtain] = []
		obtains_num_sr[obtain].append(success)
	if "dim-test" in line:
		dim = int(line.split(" ")[1])
		if dim != 1 and dim % 10 != 0 :
			continue
		success = float(line.split(" ")[-1])
		if dim not in obtains_dim_sr:
			obtains_dim_sr[dim] = []
		obtains_dim_sr[dim]= success


plt.rcParams.update({
	"text.usetex": False,
	"font.family": "sans-serif",
	# "font.sans-serif": "Helvetica",
})
font_size = 14
fig = plt.figure(figsize=(3.5, 3), dpi=100)

ax:plt.Axes = plt.axes([0.12, 0.18, 0.8, 0.7])
# titile
# ax.set_title(r"(a) Differnet used_num", y=-0.3, fontdict=dict(size=font_size))
# x
ax.set_xlabel("Obtained Fingerprints", fontsize=font_size-2, labelpad=0.8)	
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
for x_tick_label_temp in ax.get_xticklabels():
	x_tick_label_temp.set_fontsize(font_size-2)
# y
ax.yaxis.set_major_locator(MultipleLocator(1.))
ax.set_ylabel("Success Attack Devices", fontsize=font_size-2, labelpad=0.8)	
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
for y_tick_label_temp in ax.get_yticklabels():
	y_tick_label_temp.set_fontsize(font_size-2)
# grid
ax.grid(which='major',ls='--',alpha=.8,lw=.2)
# boredr
ax.spines['left'].set_linewidth(.5)
ax.spines['bottom'].set_linewidth(.5)
ax.spines['right'].set_linewidth(.5)
ax.spines['top'].set_linewidth(.5)

colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff', '#000000']
x = []
y = []
for num, l in obtains_num_sr.items():
	x.append(num)
	y.append(np.mean(l))

ax.step(x, y, color=colors[0])
plt.savefig("../picture/Fig-2a.pdf",dpi=200, format="pdf", bbox_inches="tight", pad_inches=.02)
plt.show()
plt.close()

plt.rcParams.update({
	"text.usetex": False,
	"font.family": "sans-serif",
	# "font.sans-serif": "Helvetica",
})
font_size = 14
fig = plt.figure(figsize=(3.5, 3), dpi=100)

ax:plt.Axes = plt.axes([0.12, 0.18, 0.8, 0.7])
# titile
# ax.set_title(r"(a) Differnet used_num", y=-0.3, fontdict=dict(size=font_size))
# x
ax.set_xlabel("Obtained Dimension", fontsize=font_size-2, labelpad=0.8)	
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
for x_tick_label_temp in ax.get_xticklabels():
	x_tick_label_temp.set_fontsize(font_size-2)
# y
ax.yaxis.set_major_locator(MultipleLocator(.2))
ax.set_ylabel("Success Rate", fontsize=font_size-2, labelpad=0.8)	
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
for y_tick_label_temp in ax.get_yticklabels():
	y_tick_label_temp.set_fontsize(font_size-2)
# grid
ax.grid(which='major',ls='--',alpha=.8,lw=.2)
# boredr
ax.spines['left'].set_linewidth(.5)
ax.spines['bottom'].set_linewidth(.5)
ax.spines['right'].set_linewidth(.5)
ax.spines['top'].set_linewidth(.5)

x = []
y = []
for num, l in obtains_num_sr.items():
	x.append(num)
	y.append(np.mean(l))

ax.plot(obtains_dim_sr.keys(), obtains_dim_sr.values(), marker="o", color=colors[0])
plt.savefig("../picture/Fig-2b.pdf",dpi=200, format="pdf", bbox_inches="tight", pad_inches=.02)
plt.show()
plt.close()