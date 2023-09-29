from sklearnex import patch_sklearn, unpatch_sklearn
patch_sklearn()

import argparse
import pandas as pd
import numpy as np
import sklearn
import sklearn.ensemble
import random

from tqdm import tqdm
from auth_unit import AuthenticationUnitNormal, AuthenticationSRAM

def mape(y_true, y_pred):
	return 2.0 * np.mean(np.abs((y_pred - y_true) / (np.abs(y_pred) + np.abs(y_true)))) * 100

parser = argparse.ArgumentParser()
parser.add_argument("--device_label", dest="device_label", type=int, default=0)
parser.add_argument("--device_number", dest="device_number", type=int, default=18)
parser.add_argument("--device_sample_number", dest="device_sample_number", type=int, default=10)
parser.add_argument("--used_task_number", dest="used_task_number", type=int, default=5)
parser.add_argument("--train_time", dest="train_time", type=int, default=100)
parser.add_argument("--rate_control", dest="rate_control", type=float, default=0.)
parser.add_argument("--accept_low_bound", dest="accept_low_bound", type=int, default=3)
parser.add_argument("--all_data", dest="all_data", type=int, default=1)
parser.add_argument("--multiple_only", dest="multiple_only", type=int, default=1)
parser.add_argument("--device_type", dest="device_type", type=str, default="esp32")
parser.add_argument("--shuffle_test", dest="shuffle_test", type=int, default=0)
parser.add_argument("--test_set", dest="test_set", type=int, default=1)
parser.add_argument("--test_time", dest="test_time", type=int, default=1000)
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
		"RTCFre",
		# "FPU",
		# "RTCPha",
		"SRAM",
		"PWM",
	]

# data split -- random split
repeat = 5
for task_name in task_list:
	file_number = 3 if task_name == "SRAM" else 11
	data_ = pd.read_csv("dataset/{}.csv".format(task_name))
	result_values = data_[[str(i) for i in range(file_number)]].values
	if args_parser.shuffle_test == 1:
		result_values = result_values.T
		np.random.shuffle(result_values)
		result_values = result_values.T
	for i in range(file_number):
		data_[str(i)] = result_values[:, i]
	# testset
	testset_list = []
	test_len = 1 if task_name == "SRAM" else args_parser.test_set
	for i in range(test_len):
		testset = data_.copy()
		testset = testset.drop(columns=[str(i) for i in range(file_number)])
		testset[str(0)] = data_[str(file_number - 1 - i)]
		testset_list.append(testset)
	data_ = data_.drop(columns=[str(file_number - 1 - i) for i in range(test_len)])
	testset = pd.concat(testset_list, ignore_index=True)
	# trainset && valset (only trainset is used)
	trainset_list = []
	trainset_len = 2 if task_name == "SRAM" else args_parser.test_set
	repeat_number = 1 if task_name == "SRAM" else repeat
	for i in range(file_number - test_len):
		data_[str(i)] = result_values[:, i]
	for i in range(0, file_number - test_len, repeat_number):
		trainset = data_.copy()
		trainset = trainset.drop(columns=[str(i) for i in range(file_number-test_len)])
		for k in range(repeat_number):
			trainset[str(k)] = data_[str(min(i+k, file_number-test_len-1))]
		trainset_list.append(trainset)
	trainset = pd.concat(trainset_list, ignore_index=True)
	valset = trainset.copy()

	valset = valset.drop(index=valset.index)
	
	trainset.to_csv("dataset/split_set/attack_{}_train.csv".format(task_name))
	valset.to_csv("dataset/split_set/attack_{}_val.csv".format(task_name))
	testset.to_csv("dataset/split_set/attack_{}_test.csv".format(task_name))

# Authentication general: total task_number*device_number
print("Training")
authentications = {}
device_labels = range(args_parser.device_label, args_parser.device_label + args_parser.device_number)
for label in tqdm(device_labels):
# for label in device_labels:
	authentications[label] = {}
	for task_name in task_list:
		trainset_path = "dataset/split_set/attack_{}_train.csv".format(task_name)
		valset_path = "./dataset/split_set/attack_{}_val.csv".format(task_name)
		if task_name == "SRAM":
			auth = AuthenticationSRAM(
				task_name=task_name,
				target_label=label,
			)
		else:
			auth = AuthenticationUnitNormal(
				task_name=task_name,
				target_label=label,
				repeat=5
			)
		auth.train_predictor(
			pd.concat([pd.read_csv(trainset_path), pd.read_csv(valset_path)], ignore_index=True)
		)
		authentications[label][task_name] = auth
	for task_name in task_list:
		trainset_path = "dataset/split_set/attack_{}_train.csv".format(task_name)
		valset_path = "./dataset/split_set/attack_{}_val.csv".format(task_name)
		auth:AuthenticationUnitNormal = authentications[label][task_name]
		auth.train_classifier(
			data=pd.concat([pd.read_csv(trainset_path), pd.read_csv(valset_path)], ignore_index=True),
			device_labels=device_labels,
			device_sample_number=args_parser.device_sample_number
		)
print("Training OK")

# attack test -- single task
if args_parser.multiple_only == 0:
	print("Attack test")
	attack_size_rates = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
	# attack_size_rates = [0.99]
	for task_name in task_list:
		data = pd.read_csv("./dataset/split_set/attack_{}_test.csv".format(task_name))
		for attack_size_rate in attack_size_rates:
			SR = []
			MAPE = []
			for target_label in device_labels:
				auth = authentications[target_label][task_name]

				attack_train = data[data["label"] == target_label].copy()

				attack_train = attack_train.sample(n=int(attack_size_rate * len(attack_train)))
				attack_model = sklearn.ensemble.ExtraTreesRegressor()

				args = [args for args in data.columns if "arg" in args]
				args.insert(0, "task")

				attack_model.fit(attack_train[args].values, attack_train["0"].values)
				
				attack_test = data[data["label"] == target_label].copy()
				attack_test = attack_test.drop(index=attack_train.index)

				fake_result = attack_model.predict(attack_test[args].values)
				real_result = attack_test["0"].values
				attack_test["0"] = fake_result

				MAPE.append(mape(real_result, fake_result))
				predict_result, _, (_) = auth.get_result(attack_test)
				SR.append(np.sum(predict_result == 1) / len(predict_result))
			print("single-attack task:{} rate:{} SR:{} SMAPE:{} total:{}".format(
				task_name, attack_size_rate, np.mean(SR), np.mean(MAPE), len(data) // len(set(data["label"]))
			))
	print("Finish attack test")

# %% attack test -- multiple task
used_task_number = args_parser.used_task_number
total_task_number = 10
min_pass_task_number = args_parser.accept_low_bound if args_parser.accept_low_bound != 0 else (args_parser.used_task_number + 1) // 2
train_time = args_parser.train_time
if args_parser.rate_control != 0:
	train_time = 1000000000
test_time = args_parser.test_time
noise_range = [0.08, 0.2]
config_info = "attack-multiple used_task_number:{} train_time:{} accept_low_bound:{}".format(used_task_number, train_time, min_pass_task_number)
for method in ["M1", "M2", "M3", "M4"]:
	used_rate = {} 
	SR = [] 
	SR_degenerate = {}
	for task_name in task_list:
		used_rate[task_name] = []
		SR_degenerate[task_name] = []
	for label in tqdm(device_labels, position=0, desc="label", leave=True, colour='green'):
		target_label = label 
		data_test = {} 
		task_dict = {} 
		have_used_dict = {} 
		have_passed_dict = {} 
		test_list = [] 
		for task_name in task_list:
			testset_path = "dataset/split_set/attack_{}_test.csv".format(task_name)
			task_dict[task_name] = pd.read_csv(testset_path)
			task_dict[task_name] = task_dict[task_name][task_dict[task_name]["label"] == target_label]
			data_test[task_name] = pd.DataFrame(columns=task_dict[task_name].columns)
			data_test[task_name]["if_fake"] = []
			have_used_dict[task_name] = set()
			have_passed_dict[task_name] = set()
		p_value = np.array([len(task_dict[task_name]) for task_name in task_list]) / np.sum([len(task_dict[task_name]) for task_name in task_list])
		for _ in tqdm(range(train_time), position=1, desc="target_label", leave=False, colour='red'):
			if args_parser.rate_control != 0 and np.mean([len(have_used_dict[task_name]) / len(task_dict[task_name]) for task_name in task_list]) > args_parser.rate_control:
				break
			args_results = []
			for index in range(total_task_number):
				# task_name = np.random.choice(task_list, 1)[0]
				task_name = np.random.choice(task_list, 1, p=p_value)[0]
				args_result = task_dict[task_name].sample(n=1).copy()
				args_results.append((task_name, args_result))
			if_used = [str(-i-1) for i in range(len(args_results))]
			for index in range(len(args_results)):
				task_name, args_result = args_results[index]
				if args_result.index[0] not in have_used_dict[task_name]:
					if_used[index] = str(task_name) + str(args_result.index[0])
			if_used = np.array(if_used)
			_, unique_indexes = np.unique(if_used, return_index=True)
			signature_array = np.array(["" for _ in range(len(args_results))])
			signature_array[unique_indexes] = "+"
			if_used = np.char.add(if_used, signature_array)
			if np.sum(np.logical_and(np.char.count(if_used, "+") == 1, np.char.count(if_used, "-") == 0)) < used_task_number:
				continue
			total_index = np.array([i for i in range(total_task_number)])
			total_index = total_index[np.logical_and(np.char.count(if_used, "+") == 1, np.char.count(if_used, "-") == 0)]
			used_task_ids = np.random.choice(total_index, used_task_number, replace=False)
			test_list_t = []
			for index, (task_name, args_result) in enumerate(args_results):
				noise = np.random.uniform(noise_range[0], noise_range[1])
				args_result["if_fake"] = 0
				if index not in used_task_ids:
					args_result["if_fake"] = 1
					if task_name != "SRAM":
						args_result["0"] = (args_result["0"] + 1) * (noise + 1)
					else:
						flip_number = 1
						for _ in range(32):
							if np.random.rand() > 1 - noise - 0.5:
								args_result["0"] ^= flip_number
							flip_number <<= 1
				else:
					assert((args_result.index[0] in have_used_dict[task_name]) == False)
					have_used_dict[task_name].add(args_result.index[0])
				test_list_t.append((task_name, len(data_test[task_name])))
				args_result["prev_index"] = int(args_result.index[0])
				data_test[task_name] = pd.concat([data_test[task_name], args_result])
			test_list.append(test_list_t)
		for task_name in task_list:
			if len(data_test[task_name]) <= 0:
				continue
			auth:AuthenticationUnitNormal = authentications[label][task_name]
			predict_result, predict_prob, (_) = auth.get_result(data_test[task_name]) 
			data_test[task_name]["predict_result"] = predict_result
			data_test[task_name]["predict_prob"] = predict_prob
		for task_pair_list in test_list:
			assert(np.sum(np.array([data_test[task_name].iloc[index, :]["if_fake"] for task_name, index in task_pair_list]) == 0) == used_task_number)
			predict_result = np.array([data_test[task_name].iloc[index, :]["predict_result"] for task_name, index in task_pair_list])
			if np.sum(predict_result) != 0:
				positive_pairs = np.array(task_pair_list)[predict_result == 1].tolist()
				positive_pairs = list(map(tuple, positive_pairs))
				for task_name, index in positive_pairs:
					index = int(index)
					have_passed_dict[task_name].add(int(data_test[task_name].iloc[index, :]["prev_index"]))
		for task_name in task_list:
			used_rate[task_name].append(len(have_used_dict[task_name]) / len(task_dict[task_name]))
		# Method1
		if method == "M1" or method == "M3":
			attack_model = {}
			data_train = dict(data_test)
		# Method2
		elif method == "M2" or method == "M4":
			attack_model = {}
			data_train = {}
			for task_name in task_list:
				data_train[task_name] = pd.DataFrame(columns=data_test[task_name].columns)
			for task_pair_list in test_list:
				sample_pair = random.sample(task_pair_list, used_task_number)
				for task_name, index in sample_pair:
					data_train[task_name] = pd.concat([data_train[task_name], data_test[task_name].iloc[[index], :]], ignore_index=True)
		# Method3
		for task_name in task_list:
			attack_model[task_name] = sklearn.ensemble.ExtraTreesRegressor()
			if method == "M1" or method == "M2":
				attack_model[task_name].fit(data_train[task_name].loc[:, [args for args in data_train[task_name].columns if "arg" in args]], data_train[task_name]["0"])
			elif method == "M3" or method == "M4":
				data_train[task_name]["max"] = data_train[task_name]["0"].values / (noise_range[0] + 1) - 1
				data_train[task_name]["min"] = data_train[task_name]["0"].values / (noise_range[1] + 1) - 1
				attack_model[task_name].fit(data_train[task_name].loc[:, [args for args in data_train[task_name].columns if "arg" in args]], data_train[task_name][["min", "max", "0"]])
	
		data_test = {}
		test_list = [] 
		for task_name in task_list:
			data_test[task_name] = pd.DataFrame(columns=task_dict[task_name].columns)
		for _ in  tqdm(range(test_time), position=1, desc="target_label", leave=False, colour='red'):
			test_list_t = []
			for index in range(total_task_number):
				task_name = np.random.choice(task_list, 1)[0]
				args_result = task_dict[task_name].sample(n=1).copy()
				args_result["prev_index"] = int(args_result.index[0])
				test_list_t.append((task_name, len(data_test[task_name])))
				data_test[task_name] = pd.concat([data_test[task_name], args_result])
			test_list.append(test_list_t)
		for task_name in task_list:
			if len(data_test[task_name]) <= 0:
				continue
			auth:AuthenticationUnitNormal = authentications[label][task_name]
			if method == "M1" or method == "M2":
				fake_result = attack_model[task_name].predict(data_test[task_name].loc[:, [args for args in data_test[task_name].columns if "arg" in args]])
			elif method == "M3" or method == "M4":
				fake_result_range = attack_model[task_name].predict(data_test[task_name].loc[:, [args for args in data_test[task_name].columns if "arg" in args]])
				fake_result = np.random.uniform(0, 1, len(fake_result_range))
				fake_result_min = fake_result_range[:, 0]
				fake_result_max = fake_result_range[:, 1]
				fake_result_correct = fake_result_range[:, 2]
				if np.random.uniform(0, 1) < used_task_number / total_task_number:
					fake_result = fake_result_correct
				else:
					fake_result = fake_result_min + (fake_result_max - fake_result_min) * fake_result
			data_test[task_name]["0"] = fake_result
			predict_result, predict_prob, (_) = auth.get_result(data_test[task_name]) 
			data_test[task_name]["predict_result"] = predict_result
			data_test[task_name]["predict_prob"] = predict_prob
		for task_pair_list in test_list:
			predict_result = np.array([data_test[task_name].iloc[index, :]["predict_result"] for task_name, index in task_pair_list])
			havenot_passed_result = np.array([int(data_test[task_name].iloc[index, :]["prev_index"]) not in have_passed_dict[task_name] for task_name, index in task_pair_list])
			task_index_name = np.array([str(task_name) + str(data_test[task_name].iloc[index, :]["prev_index"]) for task_name, index in task_pair_list])
			predict_result = predict_result * havenot_passed_result
			task_index_name = task_index_name[predict_result == 1]
			task_index_name = np.unique(task_index_name)
			SR.append((len(task_index_name) >= min_pass_task_number))
		for task_name in task_list:
			auth:AuthenticationUnitNormal = authentications[label][task_name]
			remain_set = task_dict[task_name].drop(index=list(have_used_dict[task_name]))
			if method == "M1" or method == "M2":
				fake_result = attack_model[task_name].predict(remain_set.loc[:, [args for args in remain_set.columns if "arg" in args]])
			elif method == "M3" or method == "M4":
				fake_result_range = attack_model[task_name].predict(remain_set.loc[:, [args for args in remain_set.columns if "arg" in args]])
				fake_result = np.random.uniform(0, 1, len(fake_result_range))
				fake_result_min = fake_result_range[:, 0]
				fake_result_max = fake_result_range[:, 1]
				fake_result_correct = fake_result_range[:, 2]
				if np.random.uniform(0, 1) < used_task_number / total_task_number:
					fake_result = fake_result_correct
				else:
					fake_result = fake_result_min + (fake_result_max - fake_result_min) * fake_result
			remain_set["fake_result"] = fake_result
			# print(remain_set)
			remain_set["0"] = fake_result
			predict_result, predict_prob, (_) = auth.get_result(remain_set) 
			SR_degenerate[task_name].append(np.sum(predict_result == 1) / len(predict_result))
		# break
	print(config_info, "method:{} SR:{}".format(method, np.sum(SR) / len(SR)))
	for task_name in task_list:
		print(config_info, "task:{} use_rate:{}".format(task_name, np.mean(used_rate[task_name])))
		print(config_info, "task:{} SR_degenerate:{}".format(task_name, np.mean(SR_degenerate[task_name])))