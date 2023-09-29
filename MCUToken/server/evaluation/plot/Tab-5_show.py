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

# plt.rcParams['font.family'] = 'Times New Roman'
font_size = 12
fig = plt.figure(figsize=(12, 3), dpi=100)

method_mapping = {
	"cluster" : "Supervised",
	"train-partly" : "Incremental",
	"train-step" : "Unsupervised",
	"extra-device" : "Extra-device"
}

file_path = "../result/Tab-5_log"
data_identify = {}
for l in open(file_path, "r"):
	line = l.rstrip()
	line = line.split(" ")
	method = line[0]
	if method not in method_mapping:
		continue
	method = method_mapping[method]
	task_name = re.search(r"task_name:(\S*)", l).group(1)
	rate = float(line[-1])
	if task_name == "RTCPha" or task_name == "FPU":
		continue
	if task_name not in data_identify:
		data_identify[task_name] = {}
	if method not in data_identify[task_name]:
		data_identify[task_name][method] = []
	data_identify[task_name][method].append(rate)
print("\t", end="\t")
for task_name in data_identify:
	print(task_name, end="\t")
print("")

for method in ["Unsupervised", "Supervised", "Incremental", "Extra-device"]:
	print(method, end="\t")
	for task_name in data_identify:
		print("{:.4f}".format(np.max(data_identify[task_name][method])), end="\t")
	print()
# break
	