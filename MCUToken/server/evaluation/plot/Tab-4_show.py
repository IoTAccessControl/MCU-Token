import matplotlib.pyplot as plt
import re
import numpy as np
import os

from matplotlib.pyplot import MultipleLocator

results = {}
device_mapping = {
	"esp32" : "esp32",
	"stm32" : "f429",
	"stm32f103" : "f103"
}
for file_name in os.listdir("../result/Tab-4_log/"):
	source_device = file_name.split("_")[-2]
	# print(source_device)
	if source_device not in results:
		results[source_device] = {}
	for l in open("../result/Tab-4_log/"+file_name, "r"):
		line = l.rstrip()
		if "hardware-mimic" in line:
			target_device = re.search(r"target_device:(\S*)", line).group(1)
			target_device = device_mapping[target_device]
			FPR = float(re.search(r"FPR:(\S*)", line).group(1))
			if target_device not in results[source_device]:
				results[source_device][target_device] = []
			results[source_device][target_device].append(FPR)
devices = list(results.keys())
for source_device in devices:
	print("\t", source_device, end=" ")
print("")
for source_device in devices:
	print(source_device,end="")
	for target_device in devices:
		print("\t{:.4f}".format(np.mean(results[source_device][target_device])), end=" ")
	print()