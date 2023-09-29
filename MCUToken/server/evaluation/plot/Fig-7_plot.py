# 多任务 不同的超参数
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

plt.rcParams.update({
	"text.usetex": False,
	"font.family": "sans-serif",
	# "font.sans-serif": "Helvetica",
})
font_size = 14
fig = plt.figure(figsize=(3.5, 3), dpi=100)

# 不同N
file_name = "../result/Fig-7a_log"
auth_multiple = {}
for l in open(file_name, "r"):
	line = l.rstrip()
	name = line.split(" ")[0]
	if name == "auth-multiple":
		used_task_number = int(re.search(r"used_task_number:(\S*)", line).group(1))
		TPR = float(re.search(r"TPR:(\S*)", line).group(1))
		Precision = float(re.search(r"Pre:(\S*)", line).group(1))
		FPR = float(re.search(r"FPR:(\S*)", line).group(1))
		if "used_task_number" not in auth_multiple:
			auth_multiple["used_task_number"] = []
			auth_multiple["TPR"] = []
			auth_multiple["Precision"] = []
			auth_multiple["FPR"] = []
		auth_multiple["used_task_number"].append(used_task_number)
		auth_multiple["TPR"].append(TPR)
		auth_multiple["Precision"].append(Precision)
		auth_multiple["FPR"].append(FPR)

colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff', '#000000']

ax:plt.Axes = plt.axes([0.08, 0.18, 0.8, 0.7])
# titile
# ax.set_title(r"(a) Differnet used_num", y=-0.3, fontdict=dict(size=font_size))
# x
ax.set_xlabel("$used\_num$", fontsize=font_size-2, labelpad=0.8)	
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
for x_tick_label_temp in ax.get_xticklabels():
	x_tick_label_temp.set_fontsize(font_size-2)
# y
ax.set_ylim(-0.05, 1.05)
ax.yaxis.set_major_locator(MultipleLocator(.2))
# ax.set_ylabel("", fontsize=6, labelpad=0.8)
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

used_task_number = auth_multiple["used_task_number"]
TPR = auth_multiple["TPR"]
FPR = auth_multiple["FPR"]
Precision = auth_multiple["Precision"]
x_len = len(np.unique(used_task_number))
used_task_number = np.array(used_task_number).reshape(-1, x_len)
used_task_number = np.mean(used_task_number, axis=0)
TPR = np.array(TPR).reshape(-1, x_len)
TPR = np.mean(TPR, axis=0)
FPR = np.array(FPR).reshape(-1, x_len)
FPR = np.mean(FPR, axis=0)
Precision = np.array(Precision).reshape(-1, x_len)
Precision = np.mean(Precision, axis=0)

ax.plot(used_task_number, TPR, label="TPR", marker="*", markerfacecolor="white", alpha = 0.8, linewidth=1.2, markersize=6.0,  color=colors[0])
ax.plot(used_task_number, FPR, label="", marker=".", markerfacecolor="white", alpha = 0.8, linewidth=1.2, markersize=6.0,  color=colors[3])
ax.legend(loc='upper center', bbox_to_anchor=(0.8, 1.18), ncol=1, frameon=False, prop=dict(size=font_size))
plt.savefig("../picture/Fig-7a.pdf",dpi=200, format="pdf", bbox_inches="tight", pad_inches=.02)
plt.show()
plt.close()

plt.rcParams.update({
	"text.usetex": False,
	"font.family": "sans-serif",
	# "font.sans-serif": "Helvetica",
})
font_size = 14
fig = plt.figure(figsize=(3.5, 3), dpi=100)

file_name = "../result/Fig-7b_log"
auth_multiple = {}
for l in open(file_name, "r"):
	line = l.rstrip()
	name = line.split(" ")[0]
	if name == "auth-multiple":
		accept_low_bound = int(re.search(r"accept_low_bound:(\S*)", line).group(1))
		TPR = float(re.search(r"TPR:(\S*)", line).group(1))
		Precision = float(re.search(r"Pre:(\S*)", line).group(1))
		FPR = float(re.search(r"FPR:(\S*)", line).group(1))
		if "accept_low_bound" not in auth_multiple:
			auth_multiple["accept_low_bound"] = []
			auth_multiple["TPR"] = []
			auth_multiple["Precision"] = []
			auth_multiple["FPR"] = []
		auth_multiple["accept_low_bound"].append(accept_low_bound)
		auth_multiple["TPR"].append(TPR)
		auth_multiple["Precision"].append(Precision)
		auth_multiple["FPR"].append(FPR)

ax:plt.Axes = plt.axes([0.08, 0.18, 0.8, 0.7])
# titile
# ax.set_title(r"(b) Authenticating with differnet K", y=-0.3, fontdict=dict(size=font_size))
# x
ax.set_xlabel("$accpect\_num$", fontsize=font_size-2, labelpad=0.8)
ax.tick_params(which='major', length=1.2, width=0.2, direction='out', pad=0.8)
for x_tick_label_temp in ax.get_xticklabels():
	x_tick_label_temp.set_fontsize(font_size-2)
# y
ax.set_ylim(-0.05, 1.05)
ax.yaxis.set_major_locator(MultipleLocator(.2))
# ax.set_ylabel("", fontsize=6, labelpad=0.8)
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


accept_low_bound = auth_multiple["accept_low_bound"]
TPR = auth_multiple["TPR"]
FPR = auth_multiple["FPR"]
Precision = auth_multiple["Precision"]
x_len = len(np.unique(accept_low_bound))
accept_low_bound = np.array(accept_low_bound).reshape(-1, x_len)
accept_low_bound = np.mean(accept_low_bound, axis=0)
TPR = np.array(TPR).reshape(-1, x_len)
TPR = np.mean(TPR, axis=0)
FPR = np.array(FPR).reshape(-1, x_len)
FPR = np.mean(FPR, axis=0)
Precision = np.array(Precision).reshape(-1, x_len)
Precision = np.mean(Precision, axis=0)

ax.plot(accept_low_bound, TPR, label="", marker="*", markerfacecolor="white", alpha = 0.8, linewidth=1.2, markersize=6.0, color=colors[0])
ax.plot(accept_low_bound, FPR, label="FPR", marker=".", markerfacecolor="white", alpha = 0.8, linewidth=1.2, markersize=6.0, color=colors[3])
# plt.plot(accept_low_bound, Precision, label="Precision")
#legend
# ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=2, frameon=False, prop=dict(size=font_size))

ax.legend(loc='upper center', bbox_to_anchor=(0.2, 1.18), ncol=1, frameon=False, prop=dict(size=font_size))
plt.savefig("../picture/Fig-7b.pdf",dpi=200, format="pdf", bbox_inches="tight", pad_inches=.02)
plt.show()
plt.close()

# 带有噪声的单任务识别准确率
# import matplotlib.pyplot as plt
# import re
# import numpy as np
# import pandas as pd

# file_name = "../result/auth/esp32_default_well"
# noise_test = {}
# for l in open(file_name, "r"):
# 	line = l.rstrip()
# 	name = line.split(" ")[0]
# 	if name == "noise-test":
# 		task = re.search(r"task:(\S*)", line).group(1).replace(",", "")
# 		TP = float(re.search(r"TP:(\S*)", line).group(1).replace(",", ""))
# 		FN = float(re.search(r"FN:(\S*)", line).group(1).replace(",", ""))
# 		noise = float(re.search(r"noise:(\S*)", line).group(1).replace(",", ""))
# 		if task not in noise_test:
# 			noise_test[task] = {}
# 			noise_test[task]["TP"] = []
# 			noise_test[task]["FN"] = []
# 			noise_test[task]["noise"] = []
# 		noise_test[task]["TP"].append(TP)
# 		noise_test[task]["FN"].append(FN)
# 		noise_test[task]["noise"].append(noise)

# plt.subplot(133)
# plt.title("Different noise")
# for task in noise_test:
# 	TP = noise_test[task]["TP"]
# 	FN = noise_test[task]["FN"]
# 	noise = noise_test[task]["noise"]
# 	x_len = len(np.unique(noise))
# 	noise = np.array(noise).reshape(-1, x_len)
# 	noise = np.mean(noise, axis=0)
# 	TP = np.array(TP).reshape(-1, x_len)
# 	TP = np.mean(TP, axis=0)
# 	FN = np.array(FN).reshape(-1, x_len)
# 	FN = np.mean(FN, axis=0)
# 	plt.plot(noise, TP / (TP + FN), label=task)
# plt.legend(loc='upper right')