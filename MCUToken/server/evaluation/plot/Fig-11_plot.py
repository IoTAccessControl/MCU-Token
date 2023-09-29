import matplotlib.pyplot as plt
import re
import numpy as np
import os

from matplotlib.pyplot import MultipleLocator

def rgb2hex(rgb):
	rgb = rgb.split(',')#将RGB格式划分开来
	hexes = '#'
	for i in rgb:
		num = int(i)
		hexes += str(hex(num))[-2:].replace('x','0').upper()
	return hexes

success_rates = {}
for file_name in os.listdir("../result/Fig-11_log"):
	if "result" in file_name:
		if "100_" in file_name or "500_" in file_name:
			continue
		output_len = int(file_name.split("_")[1])
		method_name = file_name.split("_")[2]
		results = []
		for l in open("../result/Fig-11_log/" + file_name, "r"):
			if "Success" in l or "Fail" in l:
				l = l.rstrip()
				results.append(int(l.split(" ")[-1].replace("\n","")))
		results = np.array(results)
		success_rate = np.sum(results != 1048576) / len(results)
		succes_number = np.sum(results) / np.sum(results != 1048576) if np.sum(results != 1048576) !=0 else 1048576 * len(results)
		if method_name not in success_rates:
			success_rates[method_name] = {}
			success_rates[method_name]["output_len"] = []
			success_rates[method_name]["success_rate"] = []
			success_rates[method_name]["succes_number"] = []
		success_rates[method_name]["output_len"].append(output_len)
		success_rates[method_name]["success_rate"].append(success_rate)
		success_rates[method_name]["succes_number"].append(succes_number)

plt.rcParams.update({
	"text.usetex": False,
	"font.family": "sans-serif",
	# "font.sans-serif": "Helvetica",
})
font_size = 14
fig = plt.figure(figsize=(4, 3.43), dpi=100)

ax:plt.Axes = plt.axes([0.14, 0.15, 0.8, 0.7])
ax.set_ylabel("success average times", fontsize=font_size-2, labelpad=0.8)
ax.set_xlabel("output size", fontsize=font_size-2, labelpad=0.8)

x_label = sorted(success_rates[list(success_rates.keys())[0]]["output_len"])
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
ax.set_xticks([i for i in range(5)])
ax.set_xticklabels(x_label)
for x_tick_label_temp in ax.get_xticklabels():
	x_tick_label_temp.set_fontsize(font_size-4)

ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
ax.set_yticks([i for i in range(2,8)])
ax.set_yticklabels(["$10^"+str(i)+"$" for i in range(2,8)])
for y_tick_label_temp in ax.get_yticklabels():
	y_tick_label_temp.set_fontsize(font_size-4)

ax.grid(which='major',ls='--',alpha=.8,lw=.2)
ax.spines['left'].set_linewidth(.5)
ax.spines['bottom'].set_linewidth(.5)
ax.spines['right'].set_linewidth(.5)
ax.spines['top'].set_linewidth(.5)

methods = ["1", "3", "12", "123"]
colors = ['#f032e6', '#000075', '#469990', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#bfef45', '#a9a9a9', '#ffffff', '#000000']
colors = ['#e6194B', '#3cb44b', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff', '#000000']
markers = ["*", "o", "s", "^", "p", "<"]
labels = ["", "", "$h_1\ h_2$", "$h_1\ h_2\ h_3$"]
for k, method_name in enumerate(methods):
	if method_name not in success_rates:
		continue
	success_rate = []
	succes_number = []
	for i in np.argsort(success_rates[method_name]["output_len"]):
		success_rate.append(success_rates[method_name]["success_rate"][i])
		succes_number.append(success_rates[method_name]["succes_number"][i])
	ax.plot([i for i in range(len(success_rate))], np.log10(succes_number), label=labels[k], color=colors[k], marker=markers[k], markerfacecolor="white", alpha = 0.8)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), columnspacing=3, ncol=2, frameon=False, prop=dict(size=14))
plt.savefig("../picture/Fig-11b.pdf",dpi=200, format="pdf", bbox_inches="tight", pad_inches=.02)
plt.show()
plt.close()

plt.rcParams.update({
	"text.usetex": False,
	"font.family": "sans-serif",
	# "font.sans-serif": "Helvetica",
})
font_size = 14
fig = plt.figure(figsize=(4, 3.43), dpi=100)

ax:plt.Axes = plt.axes([0.14, 0.15, 0.8, 0.7])
ax.set_ylabel("success rate", fontsize=font_size-2, labelpad=0.8)
ax.set_xlabel("output size", fontsize=font_size-2, labelpad=0.8)

x_label = sorted(success_rates[list(success_rates.keys())[0]]["output_len"])
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
ax.set_xticks([i for i in range(5)])
ax.set_xticklabels(x_label)
for x_tick_label_temp in ax.get_xticklabels():
	x_tick_label_temp.set_fontsize(font_size-4)

ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
# ax.set_yticks([i for i in range(2,8)])
# ax.set_yticklabels(["$10^"+str(i)+"$" for i in range(2,8)])
for y_tick_label_temp in ax.get_yticklabels():
	y_tick_label_temp.set_fontsize(font_size-4)

ax.grid(which='major',ls='--',alpha=.8,lw=.2)
ax.spines['left'].set_linewidth(.5)
ax.spines['bottom'].set_linewidth(.5)
ax.spines['right'].set_linewidth(.5)
ax.spines['top'].set_linewidth(.5)

markers = ["*", "o", "s", "^", "p", "<"]
labels = ["only $h_1$", "only $h_3$", "", ""]
for k, method_name in enumerate(methods):
	if method_name not in success_rates:
		continue
	success_rate = []
	succes_number = []
	for i in np.argsort(success_rates[method_name]["output_len"]):
		success_rate.append(success_rates[method_name]["success_rate"][i])
		succes_number.append(success_rates[method_name]["succes_number"][i])
	ax.plot([i for i in range(len(success_rate))], success_rate, label=labels[k], color=colors[k], marker=markers[k], markerfacecolor="white", alpha = 0.8)
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), columnspacing=3., ncol=2, frameon=False, prop=dict(size=14))
plt.savefig("../picture/Fig-11a.pdf",dpi=200, format="pdf", bbox_inches="tight", pad_inches=.02)
plt.show()
plt.close()

