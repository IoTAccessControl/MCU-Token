import matplotlib.pyplot as plt
import re
import numpy as np

def get_TPR_FPR(file_name):
  closed_world_test = {}
  for l in open(file_name, "r"):
    line = l.rstrip()
    name = line.split(" ")[0]
    if name == "closed-world-test":
      task = re.search(r"task:(\S*)", line).group(1).replace(",", "")
      TPR = float(re.search(r"TPR:(\S*)", line).group(1).replace(",", ""))
      FPR = float(re.search(r"FPR:(\S*)", line).group(1).replace(",", ""))
      if task not in closed_world_test:
        closed_world_test[task] = {}
        closed_world_test[task]["TPR"] = []
        closed_world_test[task]["FPR"] = []
      closed_world_test[task]["TPR"].append(TPR)
      closed_world_test[task]["FPR"].append(FPR)
    elif name == "auth-multiple":
      TPR = float(re.search(r"TPR:(\S*)", line).group(1).replace(",", ""))
      FPR = float(re.search(r"FPR:(\S*)", line).group(1).replace(",", ""))
      auth_multiple = [TPR, FPR]
  return closed_world_test, auth_multiple

device_types = ["esp32", "f429", "f103"]
results = {}

for device_type in device_types:
  results[device_type+"_all_single"], results[device_type+"_all_multiple"] = get_TPR_FPR("../result/Tab-3_{}_all_log".format(device_type))
  _, results[device_type+"_part"] = get_TPR_FPR("../result/Tab-3_{}_part_log".format(device_type))

task_names = ["DAC_ADC", "FPU", "PWM", "RTCFre", "RTCPha", "SRAM"]  

print("\t\tesp32\t\tstm32f429\t\tstm32f103")
print("\t\tTPR, FPR \tTPR, FPR\t\tTPR, FPR")
print("-----------------------"*3)
for task_name in task_names:
  print("{}\t\t{:.2f}, {:.2f}\t{:.2f}, {:.2f}\t\t{:.2f}, {:.2f}".format(
    task_name, 
    np.mean(results["esp32_all_single"][task_name]["TPR"]) * 100,
    np.mean(results["esp32_all_single"][task_name]["FPR"]) * 100,
    np.mean(results["f429_all_single"][task_name]["TPR"]) * 100,
    np.mean(results["f429_all_single"][task_name]["FPR"]) * 100,
    np.mean(results["f103_all_single"][task_name]["TPR"]) * 100,
    np.mean(results["f103_all_single"][task_name]["FPR"]) * 100,
  ))

  # print("{}\t\t& \\red{{{:.2f}}}        & \\red{{{:.2f}}}         &  & \\red{{{:.2f}}}         & \\red{{{:.2f}}}         &  & \\red{{{:.2f}}}         & \\red{{{:.2f}}}         \\\\".format(
  #   task_name, 
  #   np.mean(results["esp32_all_single"][task_name]["TPR"]) * 100,
  #   np.mean(results["esp32_all_single"][task_name]["FPR"]) * 100,
  #   np.mean(results["f429_all_single"][task_name]["TPR"]) * 100,
  #   np.mean(results["f429_all_single"][task_name]["FPR"]) * 100,
  #   np.mean(results["f103_all_single"][task_name]["TPR"]) * 100,
  #   np.mean(results["f103_all_single"][task_name]["FPR"]) * 100,
  # ))

print("-----------------------"*3)
print("Ensemble\t{:.2f}, {:.2f}\t{:.2f}, {:.2f}\t\t{:.2f}, {:.2f}".format(
  np.mean(results["esp32_all_multiple"][0]) * 100,
  np.mean(results["esp32_all_multiple"][1]) * 100,
  np.mean(results["f429_all_multiple"][0]) * 100,
  np.mean(results["f429_all_multiple"][1]) * 100,
  np.mean(results["f103_all_multiple"][0]) * 100,
  np.mean(results["f103_all_multiple"][1]) * 100,
))
print("Ensemble*\t{:.2f}, {:.2f}\t{:.2f}, {:.2f}\t\t{:.2f}, {:.2f}".format(
  np.mean(results["esp32_part"][0]) * 100,
  np.mean(results["esp32_part"][1]) * 100,
  np.mean(results["f429_part"][0]) * 100,
  np.mean(results["f429_part"][1]) * 100,
  np.mean(results["f103_part"][0]) * 100,
  np.mean(results["f103_part"][1]) * 100,
))
