import pandas as pd
import numpy as np
import os

task_list = [
	"DAC_ADC",
	"RTCFre",
	"FPU",
	"RTCPha",
	"SRAM",
	"PWM",
]

from dataProcess import *

print("data split")
read_all_data(["esp32"], "all_data")

prev_testset = {}
for task_name in task_list:
	testset_path = "dataset/{}.csv".format(task_name)
	testset = pd.read_csv(testset_path)

	prev_testset[task_name] = testset

target_label = 8

# read env data
env_dict = {}
for env in os.listdir("../raw_data/env"):
	print("read data in", env)
	if env not in env_dict:
		env_dict[env] = {}
	if "normal4" in env and env != "normal4":
		file_name = 2
	else:
		file_name = 3
	data_process(repeat=1, device_types=["esp32"], env_dir="env/{}".format(env), file_number=file_name)
	# test in closed-world for single task
	for task_name in task_list:
		if task_name not in env_dict[env]:
			env_dict[env][task_name] = []

		testset_path = "dataset/split_set/{}_test.csv".format(task_name)
		trainset_path = "dataset/split_set/{}_train.csv".format(task_name)
		valset_path = "dataset/split_set/{}_val.csv".format(task_name)

		testset = pd.concat([pd.read_csv(trainset_path), pd.read_csv(valset_path), pd.read_csv(testset_path)], ignore_index=True)
		testset = testset.reset_index(drop=True)
		env_dict[env][task_name] = testset

for task_name in task_list:
	set1 = prev_testset[task_name][prev_testset[task_name]["label"] == target_label]
	args = [args for args in set1.columns if "arg" in args]
	set1 = set1.reset_index(drop=True)
	set0 = set1.drop_duplicates(subset=args, keep="last").copy()
	set1 = set1.drop(index=set0.index)
	set0 = set0.reset_index(drop=True)
	set1 = set1.reset_index(drop=True)
	set0 = set0.sort_values(by=args)
	set1 = set1.sort_values(by=args)
	
	for env0 in env_dict:
		set0 = env_dict[env0][task_name]
		set1 = prev_testset[task_name][prev_testset[task_name]["label"] == target_label]
		set0 = set0.reset_index(drop=True)
		set1 = set1.reset_index(drop=True)
		set0 = set0.sort_values(by=args)
		set1 = set1.sort_values(by=args)
		if task_name == "SRAM":
			distance = []
			set0["label"] = target_label
			while len(set0) != 0:
				t = set0.drop_duplicates(subset=args, keep="first").copy()
				set0 = set0.drop(index=t.index)
				prevoius_result = set1[["0","1","2"]].values.reshape(-1)
				t = t["0"].values
				t = t.repeat(3)
				t = t.astype(np.uint32)
				prevoius_result = prevoius_result.astype(np.uint32)
				same_bit_number = np.array([0 for _ in range(len(prevoius_result))])
				for _ in range(32):
					same_bit_number += (prevoius_result & 1) == (t & 1)
					prevoius_result >>= 1
					t >>= 1
				assert(np.sum(prevoius_result == 0) == len(prevoius_result))
				assert(np.sum(t == 0) == len(t))
				distance.append(np.mean(1. - same_bit_number / 32))
		else:
			set1["0"] = set1["0"].values
			t = set0.drop_duplicates(subset=args, keep="first").copy()
			set0 = set0.drop(index=t.index)
			set0["label"] = target_label
			distance = []
			while len(set0) != 0:
				t = set0.drop_duplicates(subset=args, keep="first").copy()
				set0 = set0.drop(index=t.index)
				prevoius_result = set1[[str(i) for i in range(1, 11)]].values.reshape(-1)
				t = t["0"].values
				t = t.repeat(10)
				distance.append(np.mean(abs(t - prevoius_result) / (prevoius_result + 1e-4)))
		print(task_name, "env0:{} env1:{}".format(env0, "previous"), "distance:{}".format(np.mean(distance)))