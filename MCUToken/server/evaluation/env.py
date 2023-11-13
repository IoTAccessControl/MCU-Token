import argparse
import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from tqdm import tqdm
from auth_unit import AuthenticationUnitNormal, AuthenticationSRAM
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("--device_label", dest="device_label", type=int, default=0)
parser.add_argument("--device_number", dest="device_number", type=int, default=18)
parser.add_argument("--device_sample_number", dest="device_sample_number", type=int, default=10)
parser.add_argument("--used_task_number", dest="used_task_number", type=int, default=5)
parser.add_argument("--repeat_time", dest="repeat_time", type=int, default=1000)
parser.add_argument("--accept_low_bound", dest="accept_low_bound", type=int, default=3)
parser.add_argument("--all_data", dest="all_data", type=int, default=1)
parser.add_argument("--multiple_only", dest="multiple_only", type=int, default=1)
parser.add_argument("--device_type", dest="device_type", type=str, default="esp32")
args_parser = parser.parse_args()

if args_parser.all_data == 1:
	task_list = [
		"DAC_ADC",
		"RTCFre",
		"FPU",
		"RTCPha",
		"SRAM",
		"PWM",
	]
else:
	task_list = [
		"DAC_ADC",
		# "RTCFre",
		# "FPU",
		# "RTCPha",
		# "SRAM",
		"PWM",
	]


# # data split -- random split
from dataProcess import *

print("data split")
device_type = args_parser.device_type
if device_type == "all":
	data_process(repeat=1)
elif device_type == "esp32":
	read_all_data(["esp32"], "all_data")
elif device_type == "stm32":
	data_process(repeat=1, device_types=["stm32"])
print("data set split ok")

# 保存之前的数据
prev_testset = {}
for task_name in task_list:
	testset_path = "dataset/{}.csv".format(task_name)
	testset = pd.read_csv(testset_path)

	prev_testset[task_name] = testset

target_label = 8

# read env data
env_dict = {}
for env in os.listdir("../raw_data/env"):
	print(env)
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

# repeat = 5
# print("data split")
# device_type = args_parser.device_type
# if device_type == "all":
# 	data_process(repeat)
# elif device_type == "esp32":
# 	data_process(repeat, device_types=["esp32"])
# elif device_type == "stm32":
# 	data_process(repeat, device_types=["stm32"])
# print("data set split ok")

# # device_labels = range(args_parser.device_label, args_parser.device_label + args_parser.device_number)
# # Authentication general: total task_number*device_number
# print("Training")
# authentications = {}
# device_labels = range(args_parser.device_label, args_parser.device_label + args_parser.device_number)

# for task_name in task_list:
# 	distance = []
# 	for label in device_labels:
# 		set1 = prev_testset[task_name][prev_testset[task_name]["label"] == target_label]
# 		args = [args for args in set1.columns if "arg" in args]
# 		if label == target_label:
# 			continue
# 		set0 = prev_testset[task_name][prev_testset[task_name]["label"] == label]
# 		set0 = set0.reset_index(drop=True)
# 		set1 = set1.reset_index(drop=True)
# 		set0 = set0.sort_values(by=args)
# 		set1 = set1.sort_values(by=args)

# 		if task_name == "SRAM":
# 			while len(set0) != 0:
# 				t = set0.drop_duplicates(subset=args, keep="first").copy()
# 				set0 = set0.drop(index=t.index)
# 				prevoius_result = set1["0"].values
# 				t = t["0"].values
# 				t = t.repeat(3)
# 				t = t.astype(np.uint32)
# 				prevoius_result = prevoius_result.astype(np.uint32)
# 				same_bit_number = np.array([0 for _ in range(len(prevoius_result))])
# 				for _ in range(32):
# 					same_bit_number += (prevoius_result & 1) == (t & 1)
# 					prevoius_result >>= 1
# 					t >>= 1
# 				assert(np.sum(prevoius_result == 0) == len(prevoius_result))
# 				assert(np.sum(t == 0) == len(t))
# 				distance.append(np.mean(1. - same_bit_number / 32))
# 		else:
# 			t = set1.drop_duplicates(subset=args, keep="first").copy()
# 			set1 = set1.drop(index=t.index)
# 			t = set0.drop_duplicates(subset=args, keep="first").copy()
# 			set0 = set0.drop(index=t.index)
# 			while len(set0) != 0:
# 				t = set0.drop_duplicates(subset=args, keep="first").copy()
# 				set0 = set0.drop(index=t.index)
# 				prevoius_result = set1["0"].values
# 				t = t["0"].values
# 				t = t.repeat(10)
# 				distance.append(np.mean(abs(t - prevoius_result) / (prevoius_result + 1e-4)))
# 	print(task_name, "other devices", "max:{} min:{} mean:{}".format(np.max(distance), np.min(distance), np.mean(distance)))

# TPR_Train, FPR_Train = {}, {}
# for task_name in task_list:
# 	TPR_Train[task_name] = []
# 	FPR_Train[task_name] = []
# for label in tqdm(device_labels):
# # for label in device_labels:
# 	authentications[label] = {}
# 	for task_name in task_list:
# 		trainset_path = "dataset/split_set/{}_train.csv".format(task_name)
# 		valset_path = "./dataset/split_set/{}_val.csv".format(task_name)
# 		if task_name == "SRAM":
# 			auth = AuthenticationSRAM(
# 				task_name=task_name,
# 				target_label=label,
# 			)
# 		else:
# 			auth = AuthenticationUnitNormal(
# 				task_name=task_name,
# 				target_label=label,
# 				repeat=repeat
# 			)
# 		auth.train_predictor(
# 			pd.concat([pd.read_csv(trainset_path), pd.read_csv(valset_path)], ignore_index=True)
# 			# data=pd.read_csv(trainset_path),
# 		)
# 		authentications[label][task_name] = auth
# 	for task_name in task_list:
# 		trainset_path = "dataset/split_set/{}_train.csv".format(task_name)
# 		valset_path = "./dataset/split_set/{}_val.csv".format(task_name)
# 		auth:AuthenticationUnitNormal = authentications[label][task_name]
# 		auth.train_classifier(
# 			# data=pd.read_csv(valset_path),
# 			data=pd.concat([pd.read_csv(trainset_path), pd.read_csv(valset_path)], ignore_index=True),
# 			device_labels=device_labels,
# 			device_sample_number=args_parser.device_sample_number
# 		)
# 		TPR_Train[task_name].append(auth.TPR)
# 		FPR_Train[task_name].append(auth.FPR)
# 	# print(task_name, np.mean(TPR_Train[task_name]), np.mean(FPR_Train[task_name]))
# print("Training OK")


# 统计各个环境下任务的距离
for task_name in task_list:
	# 先考虑previous数据间的距离
	set1 = prev_testset[task_name][prev_testset[task_name]["label"] == target_label]
	args = [args for args in set1.columns if "arg" in args]
	set1 = set1.reset_index(drop=True)
	set0 = set1.drop_duplicates(subset=args, keep="last").copy()
	set1 = set1.drop(index=set0.index)
	set0 = set0.reset_index(drop=True)
	set1 = set1.reset_index(drop=True)
	set0 = set0.sort_values(by=args)
	set1 = set1.sort_values(by=args)
	
	# if task_name == "SRAM":
	# 	distance = []
	# 	set0["label"] = target_label
	# 	# auth:AuthenticationUnitNormal = authentications[target_label][task_name]
	# 	# _, predict_prob, (TP_i, TN_i, FP_i, FN_i) = auth.get_result(set0)
	# 	# TPR = TP_i / (TP_i + FN_i)
	# 	while len(set0) != 0:
	# 		t = set0.drop_duplicates(subset=args, keep="first").copy()
	# 		set0 = set0.drop(index=t.index)
	# 		prevoius_result = set1["0"].values
	# 		t = t["0"].values
	# 		t = t.repeat(2)
	# 		t = t.astype(np.uint32)
	# 		prevoius_result = prevoius_result.astype(np.uint32)
	# 		same_bit_number = np.array([0 for _ in range(len(prevoius_result))])
	# 		for _ in range(32):
	# 			same_bit_number += (prevoius_result & 1) == (t & 1)
	# 			prevoius_result >>= 1
	# 			t >>= 1
	# 		assert(np.sum(prevoius_result == 0) == len(prevoius_result))
	# 		assert(np.sum(t == 0) == len(t))
	# 		distance.append(np.mean(1. - same_bit_number / 32))
	# else:
	# 	distance = []
	# 	t = set1.drop_duplicates(subset=args, keep="first").copy()
	# 	set1 = set1.drop(index=t.index)
	# 	# 只识别前两组
	# 	index0 = set1.drop_duplicates(subset=args, keep="first").copy()
	# 	index1 = set1.drop_duplicates(subset=args, keep="first").copy().drop_duplicates(subset=args, keep="first").copy()
	# 	set0 = pd.concat([index0, index1], ignore_index=True)
	# 	# auth:AuthenticationUnitNormal = authentications[target_label][task_name]
	# 	# _, predict_prob, (TP_i, TN_i, FP_i, FN_i) = auth.get_result(set0)
	# 	# TPR = TP_i / (TP_i + FN_i)
	# 	while len(set0) != 0:
	# 		t = set0.drop_duplicates(subset=args, keep="first").copy()
	# 		set0 = set0.drop(index=t.index)
	# 		prevoius_result = set1["0"].values
	# 		t = t["0"].values
	# 		t = t.repeat(9)
	# 		distance.append(np.mean(abs(t - prevoius_result) / (prevoius_result + 1e-4)))
	# TPR = 0
	# print(task_name, "env0:{} env1:{}".format("previous", "previous"), "distance:{}".format(np.mean(distance)), "TPR:{}".format(TPR))
	# 各个环境和之前数据间的距离
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
			# auth:AuthenticationUnitNormal = authentications[target_label][task_name]
			# _, predict_prob, (TP_i, TN_i, FP_i, FN_i) = auth.get_result(set0)
			# TPR = TP_i / (TP_i + FN_i)
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
			# t = set1.drop_duplicates(subset=args, keep="first").copy()
			# set1 = set1.drop(index=t.index)
			# print(set1)
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
				# print(len(prevoius_result))
				# print(len(t))
				distance.append(np.mean(abs(t - prevoius_result) / (prevoius_result + 1e-4)))
		TPR = 0
		print(task_name, "env0:{} env1:{}".format(env0, "previous"), "distance:{}".format(np.mean(distance)), "TPR:{}".format(TPR))