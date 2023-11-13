import argparse
import pandas as pd
import numpy as np

from tqdm import tqdm
from auth_unit import AuthenticationUnitNormal, AuthenticationSRAM

parser = argparse.ArgumentParser()
parser.add_argument("--device_label", dest="device_label", type=int, default=0)
parser.add_argument("--device_number", dest="device_number", type=int, default=18)
parser.add_argument("--device_sample_number", dest="device_sample_number", type=int, default=10)
parser.add_argument("--used_task_number", dest="used_task_number", type=int, default=5)
parser.add_argument("--repeat_time", dest="repeat_time", type=int, default=400)
parser.add_argument("--accept_low_bound", dest="accept_low_bound", type=int, default=3)
parser.add_argument("--all_data", dest="all_data", type=int, default=1)
parser.add_argument("--multiple_only", dest="multiple_only", type=int, default=1)
parser.add_argument("--device_type", dest="device_type", type=str, default="esp32")
parser.add_argument("--repeat", dest="repeat", type=int, default=5)
parser.add_argument("--test_set", dest="test_set", type=int, default=1)
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
elif args_parser.device_type == "esp32":
	task_list = [
		"DAC_ADC",
		"RTCFre",
		# "FPU",
		# "RTCPha",
		"SRAM",
		"PWM",
	]
elif args_parser.device_type == "stm32f429":
	task_list = [
		"DAC_ADC",
		"RTCFre",
		"FPU",
		# "RTCPha",
		"SRAM",
		# "PWM",
	]
elif args_parser.device_type == "stm32f103":
	task_list = [
		# "DAC_ADC",
		"RTCFre",
		# "FPU",
		"RTCPha",
		"SRAM",
		# "PWM",
	]

# data split -- random split
repeat = args_parser.repeat
for task_name in task_list:
	file_number = 3 if task_name == "SRAM" else 11
	data_ = pd.read_csv("dataset/{}.csv".format(task_name))
	result_values = data_[[str(i) for i in range(file_number)]].values
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
	
	trainset.to_csv("dataset/split_set/{}_train.csv".format(task_name))
	valset.to_csv("dataset/split_set/{}_val.csv".format(task_name))
	testset.to_csv("dataset/split_set/{}_test.csv".format(task_name))

# Authentication general: total task_number*device_number
print("Training")
authentications = {}
device_labels = range(args_parser.device_label, args_parser.device_label + args_parser.device_number)
TPR_Train, FPR_Train = {}, {}
for task_name in task_list:
	TPR_Train[task_name] = []
	FPR_Train[task_name] = []
for label in tqdm(device_labels):
	authentications[label] = {}
	for task_name in task_list:
		trainset_path = "dataset/split_set/{}_train.csv".format(task_name)
		valset_path = "./dataset/split_set/{}_val.csv".format(task_name)
		if task_name == "SRAM":
			auth = AuthenticationSRAM(
				task_name=task_name,
				target_label=label,
			)
		else:
			auth = AuthenticationUnitNormal(
				task_name=task_name,
				target_label=label,
				repeat=repeat
			)
		auth.train_predictor(
			pd.concat([pd.read_csv(trainset_path), pd.read_csv(valset_path)], ignore_index=True)
			# data=pd.read_csv(trainset_path),
		)
		authentications[label][task_name] = auth
	for task_name in task_list:
		trainset_path = "dataset/split_set/{}_train.csv".format(task_name)
		valset_path = "./dataset/split_set/{}_val.csv".format(task_name)
		auth:AuthenticationUnitNormal = authentications[label][task_name]
		auth.train_classifier(
			data=pd.concat([pd.read_csv(trainset_path), pd.read_csv(valset_path)], ignore_index=True),
			device_labels=device_labels,
			device_sample_number=args_parser.device_sample_number
		)
		TPR_Train[task_name].append(auth.TPR)
		FPR_Train[task_name].append(auth.FPR)
	# print(task_name, np.mean(TPR_Train[task_name]), np.mean(FPR_Train[task_name]))
print("Training OK")

if args_parser.multiple_only == 0:
	# test in closed-world for single task
	print("Test in closed-world")
	TP, TN, FP, FN = {}, {}, {}, {}
	for task_name in task_list:
		TP[task_name] = []
		TN[task_name] = []
		FP[task_name] = []
		FN[task_name] = []

		testset_path = "dataset/split_set/{}_test.csv".format(task_name)

		testset = pd.read_csv(testset_path)
		testset = testset.reset_index(drop=True)

		for label in tqdm(device_labels):
			auth:AuthenticationUnitNormal = authentications[label][task_name]
			_, predict_prob, (TP_i, TN_i, FP_i, FN_i) = auth.get_result(testset)
			TP[task_name].append(TP_i)
			TN[task_name].append(TN_i)
			FP[task_name].append(FP_i)
			FN[task_name].append(FN_i)

		args_number = len(testset.drop_duplicates([args for args in testset.columns if "arg" in args]))
		print(
			"closed-world-test",
			"task:{} TP:{} TN:{} FP:{}, FN:{} arg_number:{}, TPR:{}, FPR:{}, Pre:{}".format(task_name, np.sum(TP[task_name]), np.sum(TN[task_name]), np.sum(FP[task_name]), np.sum(FN[task_name]), args_number, (np.sum(TP[task_name])) / (np.sum(TP[task_name]) + np.sum(FN[task_name])), (np.sum(FP[task_name])) / (np.sum(TN[task_name]) + np.sum(FP[task_name])), (np.sum(TP[task_name])) / (np.sum(TP[task_name]) + np.sum(FP[task_name])))
		)
	print("Finish test in closed-world")

	# task with noise
	noises = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
	print("Test with noise")
	for task_name in task_list:
		testset_path = "dataset/split_set/{}_test.csv".format(task_name)

		for noise in noises:
			TP, TN, FP, FN = {}, {}, {}, {}
			TP[task_name] = []
			TN[task_name] = []
			FP[task_name] = []
			FN[task_name] = []

			testset = pd.read_csv(testset_path)
			testset = testset.reset_index(drop=True)

			# add noise
			if task_name != "SRAM":
				testset["0"] = (testset["0"] + 1) * (noise + 1)
			else:
				flip_number = 1
				for _ in range(32):
					if np.random.rand() > 1 - noise - 0.5:
						testset["0"] ^= flip_number
					flip_number <<= 1

			for label in device_labels:
				auth:AuthenticationUnitNormal = authentications[label][task_name]
				data_ = testset[testset["label"] == label]
				_, predict_prob, (TP_i, TN_i, FP_i, FN_i) = auth.get_result(data_)
				TP[task_name].append(TP_i)
				TN[task_name].append(TN_i)
				FP[task_name].append(FP_i)
				FN[task_name].append(FN_i)
			print("noise-test noise:{} task:{} TP:{} TN:{}, FP:{}, FN:{}".format(noise, task_name, np.sum(TP[task_name]), np.sum(TN[task_name]), np.sum(FP[task_name]), np.sum(FN[task_name])))
	print("Finish test with noise")

# test with multi task and fake args-result
used_task_number = args_parser.used_task_number
total_task_number = 10
min_pass_task_number = args_parser.accept_low_bound if args_parser.accept_low_bound != 0 else (args_parser.used_task_number + 1) // 2
repeat_time = args_parser.repeat_time
noise_range = [0.08, 0.2]
TP = []
FP = []
TN = []
FN = []
config_info = "auth-multiple used_task_number:{} repeat_time:{} accept_low_bound:{}".format(used_task_number, repeat_time, min_pass_task_number)
for label in tqdm(device_labels, position=0, desc="label", leave=True, colour='green'):
	negative_labels = list(device_labels)
	negative_labels.remove(label)
	np.random.shuffle(negative_labels)
	negative_labels = negative_labels[:args_parser.device_sample_number]
	negative_labels.append(label)
	negative_labels = sorted(negative_labels)
	for target_label in negative_labels:
		data_test = {}
		task_dict = {}
		have_used_dict = {}
		have_passed_dict = {}
		test_list = [] # [[(task_name, index) * total_task_number]...]
		for task_name in task_list:
			testset_path = "dataset/split_set/{}_test.csv".format(task_name)
			task_dict[task_name] = pd.read_csv(testset_path)
			task_dict[task_name] = task_dict[task_name][task_dict[task_name]["label"] == target_label]
			data_test[task_name] = pd.DataFrame(columns=task_dict[task_name].columns)
			data_test[task_name]["if_fake"] = []
			have_used_dict[task_name] = set()
			have_passed_dict[task_name] = set()
		p_value = np.array([len(task_dict[task_name]) for task_name in task_list]) / np.sum([len(task_dict[task_name]) for task_name in task_list])
		for _ in tqdm(range(repeat_time), position=1, desc="target_label", leave=False, colour='red'):
			args_results = []
			for index in range(total_task_number):
				task_name = np.random.choice(task_list, 1)[0]
				# task_name = np.random.choice(task_list, 1, p=p_value)[0]
				args_result = task_dict[task_name].sample(n=1).copy() # random choice
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
			# noise add
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
			havenot_passed_result = np.array([int(data_test[task_name].iloc[index, :]["prev_index"]) not in have_passed_dict[task_name] for task_name, index in task_pair_list])
			if np.sum(predict_result) != 0:
				positive_pairs = np.array(task_pair_list)[predict_result == 1].tolist()
				positive_pairs = list(map(tuple, positive_pairs))
				for task_name, index in positive_pairs:
					index = int(index)
					have_passed_dict[task_name].add(int(data_test[task_name].iloc[index, :]["prev_index"]))
			task_index_name = np.array([str(task_name) + str(data_test[task_name].iloc[index, :]["prev_index"]) for task_name, index in task_pair_list])
			predict_result = predict_result * havenot_passed_result
			task_index_name = task_index_name[predict_result == 1]
			task_index_name = np.unique(task_index_name)
			auth_result = (len(task_index_name) >= min_pass_task_number) and (len(task_index_name) <= used_task_number)
			if label == target_label:
				TP.append(auth_result == 1)
				FN.append(auth_result == 0)
			else:
				TN.append(auth_result == 0)
				FP.append(auth_result == 1)
TP = np.sum(TP)
FN = np.sum(FN)
TN = np.sum(TN)
FP = np.sum(FP)
TPR = TP / (TP + FN) if (TP + FN) != 0 else 0
Precision = TP / (TP + FP) if (TP + FP) != 0 else 0
FPR = FP / (TN + FP) if (TN + FP) != 0 else 0
print(config_info, "TP:{}, FN:{}, TN:{}, FP:{}, TPR:{} Pre:{} FPR:{}".format(TP, FN, TN, FP, TPR, Precision, FPR))