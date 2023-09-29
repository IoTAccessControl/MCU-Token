import os 
import pandas as pd
import numpy as np
import argparse

def data_process(repeat, device_types=set(["esp32", "stm32"]), env_dir="all_data", file_number=11):
	# %% DAC_ADC
	name = "DAC_ADC"
	file_dir = "../raw_data/{}/voltage".format(env_dir)
	label_dict = {}
	data_esp32 = pd.DataFrame(columns=["task", "result1", "result2", "label"])
	data_stm32 = pd.DataFrame(columns=["task", "result1", "result2", "label"])
	# i = 0
	# target_index = 1
	for file_name in sorted(os.listdir(file_dir)):
		# if i < target_index and file_number==1:
		# 	i += 1
		# 	continue
		# i += 1
		# if i == target_index + 2 and file_number==1:
		# 	break
		df_t = pd.read_csv(file_dir + "/" + file_name, names=["task", "result1", "result2"])
		# label
		number = int(file_name.split("_")[1])
		if "ESP32_" in file_name and "esp32" in device_types:
			device_label = "ESP32_" + str(number)
			if device_label not in label_dict:
				label_dict[device_label] = len(label_dict)
			df_t["label"] = label_dict[device_label]
			data_esp32 = pd.concat([data_esp32, df_t], ignore_index=True)
		elif "STM32_" in file_name and "stm32" in device_types:
			device_label = "STM32_" + str(number)
			if device_label not in label_dict:
				label_dict[device_label] = len(label_dict)
			df_t["label"] = label_dict[device_label]
			data_stm32 = pd.concat([data_stm32, df_t], ignore_index=True)
	# single file format
	esp32_format = pd.DataFrame(columns=["arg1", "arg2", "arg3", "arg4"])
	arg1 = list(np.array(list([0, 1]))) * len(range(0, 256, 1))
	arg1 += list(range(16, 8016, 16)) * len(range(0, 3, 2)) * len(range(2500, 6000, 2500))
	arg1 += list([0])
	arg1 += list(np.array(list([0, 1]))) * len(range(0, 256, 1))
	arg1 += list(range(16, 8016, 16)) * len(range(0, 3, 2)) * len(range(2500, 6000, 2500))
	esp32_format["arg1"] = arg1
	arg2 = list([0]) * len(list([0, 1])) * len(range(0, 256, 1))
	arg2 += list([0]) * len(range(16, 8016, 16)) * len(range(0, 3, 2)) * len(range(2500, 6000, 2500))
	arg2 += list([0])
	arg2 += list([1]) * len(list([0, 1])) * len(range(0, 256, 1))
	arg2 += list([1]) * len(range(16, 8016, 16)) * len(range(0, 3, 2)) * len(range(2500, 6000, 2500))
	esp32_format["arg2"] = arg2
	arg3 = list(np.array(range(0, 256, 1)).repeat(len(list([0, 1]))))
	arg3 += list(np.array(range(0, 3, 2)).repeat(len(range(16, 8016, 16)))) * len(range(2500, 6000, 2500))
	arg3 += list([0])
	arg3 += list(np.array(range(0, 256, 1)).repeat(len(list([0, 1]))))
	arg3 += list(np.array(range(0, 3, 2)).repeat(len(range(16, 8016, 16)))) * len(range(2500, 6000, 2500))
	esp32_format["arg3"] = arg3
	arg4 = list([0]) * len(list([0, 1])) * len(range(0, 256, 1))
	arg4 += list(np.array(range(2500, 6000, 2500)).repeat(len(range(16, 8016, 16)) * len(range(0, 3, 2))))
	arg4 += list([0])
	arg4 += list([0]) * len(list([0, 1])) * len(range(0, 256, 1))
	arg4 += list(np.array(range(2500, 6000, 2500)).repeat(len(range(16, 8016, 16)) * len(range(0, 3, 2))))
	esp32_format["arg4"] = arg4
	# theory
	theory = list(np.array([[8191/255, 3300/255]]).repeat(len(range(0, 256, 1))))
	theory += list(np.array(range(2500, 6000, 2500)).repeat(len(range(16, 8016, 16)) * len(range(0, 3, 2))))
	theory += list([0])
	theory += list(np.array([[8191/255, 3300/255]]).repeat(len(range(0, 256, 1))))
	theory += list(np.array(range(2500, 6000, 2500)).repeat(len(range(16, 8016, 16)) * len(range(0, 3, 2))))
	data_esp32["theory"] = np.array(theory).reshape(1, -1).repeat(len(set(data_esp32["label"])) * file_number, axis=0).reshape(-1)
	for arg in esp32_format.columns:
		data_esp32[arg] = esp32_format[arg].values.reshape(1, -1).repeat(len(set(data_esp32["label"])) * file_number, axis=0).reshape(-1)
	
	stm32_format = pd.DataFrame(columns=["arg1", "arg2", "arg3", "arg4"])
	# format & duty
	arg1 = list(np.array(list([0, 1]))) * len(range(0, 4096, 128))
	arg1 += list(range(1, 999, 50)) * len(range(0, 1, 1)) * len(range(100, 150, 10))
	arg1 += list([0])
	arg1 += list(np.array(list([0, 1]))) * len(range(0, 4096, 128))
	arg1 += list(range(1, 999, 50)) * len(range(0, 1, 1)) * len(range(100, 150, 10))
	stm32_format["arg1"] = arg1
	# vref
	arg2 = list([0]) * len(list([0, 1])) * len(range(0, 4096, 128))
	arg2 += list([0]) * len(range(1, 999, 50)) * len(range(0, 1, 1)) * len(range(100, 150, 10))
	arg2 += list([0])
	arg2 += list([1]) * len(list([0, 1])) * len(range(0, 4096, 128))
	arg2 += list([1]) * len(range(1, 999, 50)) * len(range(0, 1, 1)) * len(range(100, 150, 10))
	stm32_format["arg2"] = arg2
	# clock_source
	arg3 = list(np.array(range(0, 4096, 128)).repeat(len(list([0, 1]))))
	arg3 += list(np.array(range(0, 1, 1)).repeat(len(range(1, 999, 50)))) * len(range(100, 150, 10))
	arg3 += list([0])
	arg3 += list(np.array(range(0, 4096, 128)).repeat(len(list([0, 1]))))
	arg3 += list(np.array(range(0, 1, 1)).repeat(len(range(1, 999, 50)))) * len(range(100, 150, 10))
	stm32_format["arg3"] = arg3
	# freq
	arg4 = list([0]) * len(list([0, 1])) * len(range(0, 4096, 128))
	arg4 += list(np.array(range(100, 150, 10)).repeat(len(range(1, 999, 50)) * len(range(0, 1, 1))))
	arg4 += list([0])
	arg4 += list([0]) * len(list([0, 1])) * len(range(0, 4096, 128))
	arg4 += list(np.array(range(100, 150, 10)).repeat(len(range(1, 999, 50)) * len(range(0, 1, 1))))
	stm32_format["arg4"] = arg4
	# theory
	theory = list(np.array([[8191/4095, 3300/4095]]).repeat(len(range(0, 4096, 128))))
	theory += list(np.array(range(100, 150, 10)).repeat(len(range(1, 999, 50)) * len(range(0, 1, 1))))
	theory += list([0])
	theory += list(np.array([[8191/4095, 3300/4095]]).repeat(len(range(0, 4096, 128))))
	theory += list(np.array(range(100, 150, 10)).repeat(len(range(1, 999, 50)) * len(range(0, 1, 1))))
	data_stm32["theory"] = np.array(theory).reshape(1, -1).repeat(len(set(data_stm32["label"])) * file_number, axis=0).reshape(-1) 
	for arg in stm32_format.columns:
		data_stm32[arg] = stm32_format[arg].values.reshape(1, -1).repeat(len(set(data_stm32["label"])) * file_number, axis=0).reshape(-1)
	
	data_ = pd.concat([data_esp32, data_stm32], ignore_index=True)
	data_ = data_[data_["task"] == 3002].copy()
	# args add
	o2 = data_["result1"].values & 0xFFFF
	o1 = data_["result1"].values >> 16
	data_["arg4"] = 0
	data_["result"] = abs(o1 - data_["theory"])
	data_t = data_.copy()
	for i in range(3):
		data_t["arg4"] = i + 1
		if i == 0:
			data_t["result"] = abs(o2 - data_["theory"])
		elif i == 1:
			data_t["result"] = abs(o1 / (o2 + 1e-4))
		elif i == 2:
			data_t["result"] = abs(o1)
		data_ = pd.concat([data_, data_t], ignore_index=True)
	# filter
	# train-test split
	data_ = data_.drop(columns=["result1", "result2", "theory"])
	args_with_label = [args for args in data_.columns if "arg" in args]
	args_with_label.append("label")
	data_ = data_.sort_values(by=args_with_label)
	data_ = data_.reset_index(drop=True)
	# data_ = data_.sample(n=len(data_))
	testset = data_.drop_duplicates(subset=args_with_label, keep="last").copy()
	trainset = data_.loc[data_.drop(index=testset.index).index, :].copy()
	args_len = 10
	while args_len % repeat != 0:
		drop_index = trainset.drop_duplicates(subset=args_with_label, keep="last").index
		testset = pd.concat([testset, trainset.loc[drop_index, :].copy()])
		trainset = trainset.drop(index=drop_index)
		args_len -= 1
	trainset = trainset.sort_values(args_with_label)
	result_values = trainset["result"].values
	result_values = result_values.reshape(-1, repeat)
	result_values = result_values.repeat(repeat, axis=0)
	result_values = np.sort(result_values)
	for i in range(repeat):
		trainset[i] = result_values[:, i]
	trainset = trainset.iloc[[i for i in range(0,len(trainset), repeat)]]
	trainset = trainset.drop(columns=["result"])
	valset = trainset.drop_duplicates(subset=args_with_label, keep="last").copy()
	trainset = trainset.drop(valset.index)
	testset["0"] = testset["result"].values
	testset = testset.drop(columns=["result"])
	trainset.to_csv("./dataset/split_set/{}_train.csv".format(name), index=False)
	valset.to_csv("./dataset/split_set/{}_val.csv".format(name), index=False)
	testset.to_csv("./dataset/split_set/{}_test.csv".format(name), index=False)
	# %% PWM
	name = "PWM"
	data_ = pd.concat([data_esp32, data_stm32], ignore_index=True)
	data_ = data_[data_["task"] == 3004].copy()
	# train-test split
	data_["result"] = data_["result1"]
	data_ = data_.drop(columns=["result1", "result2"])
	args_with_label = [args for args in data_.columns if "arg" in args]
	args_with_label.append("label")
	data_ = data_.sort_values(by=args_with_label)
	data_ = data_.reset_index(drop=True)
	# data_ = data_.sample(n=len(data_))
	testset = data_.drop_duplicates(subset=args_with_label, keep="last").copy()
	trainset = data_.loc[data_.drop(index=testset.index).index, :].copy()
	args_len = 10
	while args_len % repeat != 0:
		drop_index = trainset.drop_duplicates(subset=args_with_label, keep="last").index
		testset = pd.concat([testset, trainset.loc[drop_index, :].copy()])
		trainset = trainset.drop(index=drop_index)
		args_len -= 1
	trainset = trainset.sort_values(args_with_label)
	result_values = trainset["result"].values
	result_values = result_values.reshape(-1, repeat)
	result_values = result_values.repeat(repeat, axis=0)
	result_values = np.sort(result_values)
	for i in range(repeat):
		trainset[i] = result_values[:, i]
	trainset = trainset.iloc[[i for i in range(0,len(trainset), repeat)]]
	trainset = trainset.drop(columns=["result"])
	valset = trainset.drop_duplicates(subset=args_with_label, keep="last").copy()
	trainset = trainset.drop(valset.index)
	testset["0"] = testset["result"].values
	testset = testset.drop(columns=["result"])
	trainset.to_csv("./dataset/split_set/{}_train.csv".format(name), index=False)
	valset.to_csv("./dataset/split_set/{}_val.csv".format(name), index=False)
	testset.to_csv("./dataset/split_set/{}_test.csv".format(name), index=False)

	# %% RTCFre
	name = "RTCFre"
	file_dir = "../raw_data/{}/clock".format(env_dir)
	label_dict = {}
	data_esp32 = pd.DataFrame(columns=["task", "result1", "result2", "label"])
	data_stm32 = pd.DataFrame(columns=["task", "result1", "result2", "label"])
	for file_name in sorted(os.listdir(file_dir)):
		df_t = pd.read_csv(file_dir + "/" + file_name, names=["task", "result1", "result2"])
		# label
		number = int(file_name.split("_")[1])
		if "ESP32_" in file_name and "esp32" in device_types:
			device_label = "ESP32_" + str(number)
			if device_label not in label_dict:
				label_dict[device_label] = len(label_dict)
			df_t["label"] = label_dict[device_label]
			data_esp32 = pd.concat([data_esp32, df_t], ignore_index=True)
		elif "STM32_" in file_name and "stm32" in device_types:
			device_label = "STM32_" + str(number)
			if device_label not in label_dict:
				label_dict[device_label] = len(label_dict)
			df_t["label"] = label_dict[device_label]
			data_stm32 = pd.concat([data_stm32, df_t], ignore_index=True)
	# single file format
	esp32_format = pd.DataFrame(columns=["arg1", "arg2", "arg3", "arg4"])
	arg1 = list(range(0, 256, 2)) * len(range(0, 4)) * len(range(0, 2)) * len(range(50, 250, 50))
	arg1 += list(range(100, 40000, 400)) * len(range(0, 4)) * len(range(0, 2)) * len(range(50, 250, 50))
	esp32_format["arg1"] = arg1
	arg2 = list(np.array(list(range(0, 4))).repeat(len(range(0, 256, 2)))) * len(range(0, 2)) * len(range(50, 250, 50))
	arg2 += list(np.array(list(range(0, 4))).repeat(len(range(100, 40000, 400)))) * len(range(0, 2)) * len(range(50, 250, 50))
	esp32_format["arg2"] = arg2
	arg3 = list(np.array(list(range(0, 2))).repeat(len(range(0, 256, 2)) * len(range(0, 4)))) * len(range(50, 250, 50))
	arg3 += list(np.array(list(range(0, 2))).repeat(len(range(100, 40000, 400)) * len(range(0, 4)))) * len(range(50, 250, 50))
	esp32_format["arg3"] = arg3
	arg4 = list(np.array(list(range(50, 250, 50))).repeat(len(range(0, 256, 2)) * len(range(0, 4)) * len(range(0, 2))))
	arg4 += list(np.array(list(range(50, 250, 50))).repeat(len(range(100, 40000, 400)) * len(range(0, 4)) * len(range(0, 2))))
	esp32_format["arg4"] = arg4
	for arg in esp32_format.columns:
		data_esp32[arg] = esp32_format[arg].values.reshape(1, -1).repeat(len(set(data_esp32["label"])) * file_number, axis=0).reshape(-1)
	
	stm32_format = pd.DataFrame(columns=["arg1", "arg2", "arg3", "arg4"])
	arg1 = list(range(50, 250, 50)) * len(range(1, 3, 1)) * len(range(1, 3, 1)) * len(range(0, 1, 1))
	arg1 += list(range(10000, 50000, 2000)) * len(range(1, 3, 1)) * len(range(0, 1, 1)) * len(range(50, 250, 50))
	stm32_format["arg1"] = arg1
	arg2 = list(np.array(list(range(1, 3, 1))).repeat(len(range(50, 250, 50)))) * len(range(1, 3, 1)) * len(range(0, 1, 1))
	arg2 += list(np.array(list(range(1, 3, 1))).repeat(len(range(10000, 50000, 2000)))) * len(range(0, 1, 1)) * len(range(50, 250, 50))
	stm32_format["arg2"] = arg2
	arg3 = list(np.array(list(range(1, 3, 1))).repeat(len(range(50, 250, 50)) * len(range(1, 3, 1)))) * len(range(0, 1, 1))
	arg3 += list(np.array(list(range(0, 1, 1))).repeat(len(range(10000, 50000, 2000)) * len(range(1, 3, 1)))) * len(range(50, 250, 50))
	stm32_format["arg3"] = arg3
	arg4 = list(np.array(list(range(0, 1, 1))).repeat(len(range(50, 250, 50)) * len(range(1, 3, 1)) * len(range(1, 3, 1))))
	arg4 += list(np.array(list(range(50, 250, 50))).repeat(len(range(10000, 50000, 2000)) * len(range(1, 3, 1)) * len(range(0, 1, 1))))
	stm32_format["arg4"] = arg4
	for arg in stm32_format.columns:
		data_stm32[arg] = stm32_format[arg].values.reshape(1, -1).repeat(len(set(data_stm32["label"])) * file_number, axis=0).reshape(-1)
	
	data_ = pd.concat([data_esp32, data_stm32], ignore_index=True)
	data_ = data_[data_["task"] == 4000].copy()
	# filter
	# train-test split
	data_["result"] = data_["result1"]
	data_ = data_.drop(columns=["result1", "result2"])
	args_with_label = [args for args in data_.columns if "arg" in args]
	args_with_label.append("label")
	data_ = data_.sort_values(by=args_with_label)
	data_ = data_.reset_index(drop=True)
	data_ = data_.sample(n=len(data_))
	testset = data_.drop_duplicates(subset=args_with_label, keep="last").copy()
	trainset = data_.loc[data_.drop(index=testset.index).index, :].copy()
	args_len = 10
	while args_len % repeat != 0:
		drop_index = trainset.drop_duplicates(subset=args_with_label, keep="last").index
		testset = pd.concat([testset, trainset.loc[drop_index, :].copy()])
		trainset = trainset.drop(index=drop_index)
		args_len -= 1
	trainset = trainset.sort_values(args_with_label)
	result_values = trainset["result"].values
	result_values = result_values.reshape(-1, repeat)
	result_values = result_values.repeat(repeat, axis=0)
	result_values = np.sort(result_values)
	for i in range(repeat):
		trainset[i] = result_values[:, i]
	trainset = trainset.iloc[[i for i in range(0,len(trainset), repeat)]]
	trainset = trainset.drop(columns=["result"])
	valset = trainset.drop_duplicates(subset=args_with_label, keep="last").copy()
	trainset = trainset.drop(valset.index)
	testset["0"] = testset["result"].values
	testset = testset.drop(columns=["result"])
	trainset.to_csv("./dataset/split_set/{}_train.csv".format(name), index=False)
	valset.to_csv("./dataset/split_set/{}_val.csv".format(name), index=False)
	testset.to_csv("./dataset/split_set/{}_test.csv".format(name), index=False)
	# %% RTCPha
	name = "RTCPha"
	data_ = pd.concat([data_esp32, data_stm32], ignore_index=True)
	data_ = data_[data_["task"] == 4003].copy()
	# filter
	# train-test split
	data_["result"] = data_["result1"]
	data_ = data_.drop(columns=["result1", "result2"])
	args_with_label = [args for args in data_.columns if "arg" in args]
	args_with_label.append("label")
	data_ = data_.sort_values(by=args_with_label)
	data_ = data_.reset_index(drop=True)
	# data_ = data_.sample(n=len(data_))
	testset = data_.drop_duplicates(subset=args_with_label, keep="last").copy()
	trainset = data_.loc[data_.drop(index=testset.index).index, :].copy()
	args_len = 10
	while args_len % repeat != 0:
		drop_index = trainset.drop_duplicates(subset=args_with_label, keep="last").index
		testset = pd.concat([testset, trainset.loc[drop_index, :].copy()])
		trainset = trainset.drop(index=drop_index)
		args_len -= 1
	trainset = trainset.sort_values(args_with_label)
	result_values = trainset["result"].values
	result_values = result_values.reshape(-1, repeat)
	result_values = result_values.repeat(repeat, axis=0)
	result_values = np.sort(result_values)
	for i in range(repeat):
		trainset[i] = result_values[:, i]
	trainset = trainset.iloc[[i for i in range(0,len(trainset), repeat)]]
	trainset = trainset.drop(columns=["result"])
	valset = trainset.drop_duplicates(subset=args_with_label, keep="last").copy()
	trainset = trainset.drop(valset.index)
	testset["0"] = testset["result"].values
	testset = testset.drop(columns=["result"])
	trainset.to_csv("./dataset/split_set/{}_train.csv".format(name), index=False)
	valset.to_csv("./dataset/split_set/{}_val.csv".format(name), index=False)
	testset.to_csv("./dataset/split_set/{}_test.csv".format(name), index=False)
	# %% FPU
	name = "FPU"
	file_dir = "../raw_data/{}/fpu".format(env_dir)
	label_dict = {}
	data_esp32 = pd.DataFrame(columns=["task", "result1", "result2", "label"])
	data_stm32 = pd.DataFrame(columns=["task", "result1", "result2", "label"])
	for file_name in sorted(os.listdir(file_dir)):
		df_t = pd.read_csv(file_dir + "/" + file_name, names=["task", "result1", "result2"])
		# label
		number = int(file_name.split("_")[1])
		if "ESP32_" in file_name and "esp32" in device_types:
			device_label = "ESP32_" + str(number)
			if device_label not in label_dict:
				label_dict[device_label] = len(label_dict)
			df_t["label"] = label_dict[device_label]
			data_esp32 = pd.concat([data_esp32, df_t], ignore_index=True)
		elif "STM32_" in file_name and "stm32" in device_types:
			device_label = "STM32_" + str(number)
			if device_label not in label_dict:
				label_dict[device_label] = len(label_dict)
			df_t["label"] = label_dict[device_label]
			data_stm32 = pd.concat([data_stm32, df_t], ignore_index=True)
	# single file format
	esp32_format = pd.DataFrame(columns=["arg1", "arg2", "arg3"])
	arg1 = list(range(1, 89, 3)) * len(range(1, 89, 3)) * 2
	esp32_format["arg1"] = arg1
	arg2 = list(np.array(list(range(1, 89, 3))).repeat(len(range(1, 89, 3)))) * 2
	esp32_format["arg2"] = arg2
	arg3 = list(np.array(list([0, 1])).repeat(len(range(1, 89, 3)) * len(range(1, 89, 3))))
	esp32_format["arg3"] = arg3
	for arg in esp32_format.columns:
		data_esp32[arg] = esp32_format[arg].values.reshape(1, -1).repeat(len(set(data_esp32["label"])) * file_number, axis=0).reshape(-1)

	stm32_format = esp32_format.copy()
	for arg in stm32_format.columns:
		data_stm32[arg] = stm32_format[arg].values.reshape(1, -1).repeat(len(set(data_stm32["label"])) * file_number, axis=0).reshape(-1)

	data_ = pd.concat([data_esp32, data_stm32], ignore_index=True).copy()
	# train-test split
	data_["result"] = data_["result1"]
	data_ = data_.drop(columns=["result1", "result2"])
	args_with_label = [args for args in data_.columns if "arg" in args]
	args_with_label.append("label")
	data_ = data_.sort_values(by=args_with_label)
	data_ = data_.reset_index(drop=True)
	# data_ = data_.sample(n=len(data_))
	testset = data_.drop_duplicates(subset=args_with_label, keep="last").copy()
	trainset = data_.loc[data_.drop(index=testset.index).index, :].copy()
	args_len = 10
	while args_len % repeat != 0:
		drop_index = trainset.drop_duplicates(subset=args_with_label, keep="last").index
		testset = pd.concat([testset, trainset.loc[drop_index, :].copy()])
		trainset = trainset.drop(index=drop_index)
		args_len -= 1
	trainset = trainset.sort_values(args_with_label)
	result_values = trainset["result"].values
	result_values = result_values.reshape(-1, repeat)
	result_values = result_values.repeat(repeat, axis=0)
	result_values = np.sort(result_values)
	for i in range(repeat):
		trainset[i] = result_values[:, i]
	trainset = trainset.iloc[[i for i in range(0,len(trainset), repeat)]]
	trainset = trainset.drop(columns=["result"])
	valset = trainset.drop_duplicates(subset=args_with_label, keep="last").copy()
	trainset = trainset.drop(valset.index)
	testset["0"] = testset["result"].values
	testset = testset.drop(columns=["result"])
	trainset.to_csv("./dataset/split_set/{}_train.csv".format(name), index=False)
	valset.to_csv("./dataset/split_set/{}_val.csv".format(name), index=False)
	testset.to_csv("./dataset/split_set/{}_test.csv".format(name), index=False)
	# %% SRAM
	name = "SRAM"
	file_dir = "../raw_data/{}/storage".format(env_dir)
	label_dict = {}
	data_esp32 = pd.DataFrame(columns=["task", "result1", "result2", "label"])
	data_stm32 = pd.DataFrame(columns=["task", "result1", "result2", "label"])
	for file_name in sorted(os.listdir(file_dir)):
		df_t = pd.read_csv(file_dir + "/" + file_name, names=["task", "result1", "result2"])
		# label
		number = int(file_name.split("_")[1])
		if "ESP32_" in file_name and "esp32" in device_types:
			device_label = "ESP32_" + str(number)
			if device_label not in label_dict:
				label_dict[device_label] = len(label_dict)
			df_t["label"] = label_dict[device_label]
			data_esp32 = pd.concat([data_esp32, df_t], ignore_index=True)
		elif "STM32_" in file_name and "stm32" in device_types:
			device_label = "STM32_" + str(number)
			if device_label not in label_dict:
				label_dict[device_label] = len(label_dict)
			df_t["label"] = label_dict[device_label]
			data_stm32 = pd.concat([data_stm32, df_t], ignore_index=True)
	# single file format
	esp32_format = pd.DataFrame(columns=["arg1", "arg2"])
	arg1 = data_esp32["result1"].values - 0x3FFD0000
	esp32_format["arg1"] = arg1
	arg2 = 4
	esp32_format["arg2"] = arg2
	for arg in esp32_format.columns:
		data_esp32[arg] = esp32_format[arg].values

	stm32_format = pd.DataFrame(columns=["arg1", "arg2"])
	arg1 = data_stm32["result1"].values - 0x20000000
	stm32_format["arg1"] = arg1
	arg2 = 4
	stm32_format["arg2"] = arg2
	for arg in stm32_format.columns:
		data_stm32[arg] = stm32_format[arg].values

	data_ = pd.concat([data_esp32, data_stm32], ignore_index=True)
	data_ = data_[data_["task"] == 5000].copy()
	# train-test split
	data_["0"] = data_["result2"]
	data_ = data_.drop(columns=["result1", "result2"])
	args_with_label = [args for args in data_.columns if "arg" in args]
	args_with_label.append("label")
	data_ = data_.sort_values(by=args_with_label)
	data_ = data_.reset_index(drop=True)
	# data_ = data_.sample(n=len(data_))
	testset = data_.drop_duplicates(subset=args_with_label, keep="last").copy()
	trainset = data_.loc[data_.drop(index=testset.index).index, :].copy()
	valset = trainset.drop_duplicates(subset=args_with_label, keep="last").copy()
	trainset = trainset.drop(valset.index)
	trainset.to_csv("./dataset/split_set/{}_train.csv".format(name), index=False)
	valset.to_csv("./dataset/split_set/{}_val.csv".format(name), index=False)
	testset.to_csv("./dataset/split_set/{}_test.csv".format(name), index=False)
	# %%

def save_dataset(data_, repeat, name):
	file_number = 3 if name == "SRAM" else 11
	args_with_label = [args for args in data_.columns if "arg" in args]
	# args_with_label.insert(-1, "label")
	args_with_label.append("label")
	data_ = data_.sort_values(by=args_with_label)
	data_ = data_.reset_index(drop=True)
	result_values = data_["result"].values
	result_values = result_values.reshape(-1, file_number)
	result_values = result_values.repeat(file_number, axis=0)
	# result_values = np.sort(result_values)
	for i in range(file_number):
		data_[i] = result_values[:, i]
	data_ = data_.drop(columns=["result"])
	data_ = data_.drop_duplicates(args_with_label)
	data_.to_csv("./dataset/{}.csv".format(name), index=False)
	# print("Read {} data".format(name))

def data_read(repeat, device_types, data_format, env_dir="all_data", task_name="voltage", reduction=False):
	file_dir = "../raw_data/{}/{}".format(env_dir, task_name)
	label_dict = {}
	data_raw = []
	# file read
	for device_type in device_types:
		data_list = []
		for file_name in sorted(os.listdir(file_dir)):
			if device_type + "_" not in file_name.lower():
				continue
			number = int(file_name.split("_")[1])
			device_label = device_type + "_" + str(number)
			# print(task_name, file_name, device_label)
			if device_label not in label_dict:
				label_dict[device_label] = len(label_dict)
			df_t = pd.read_csv(file_dir + "/" + file_name, names=["task", "result1", "result2"])
			df_t["label"] = label_dict[device_label]
			data_list.append(df_t)
		data_ = pd.concat(data_list, ignore_index=True)
		# args-result generate
		for col in data_format[device_type].columns:
			data_[col] = data_format[device_type][col].values.reshape(1, -1).repeat(len(data_list), axis=0).reshape(-1)
		data_raw.append(data_)
	data_raw = pd.concat(data_raw, ignore_index=True)
	
	if task_name == "voltage":
		# DAC_ADC
		name = "DAC_ADC"
		data_ = data_raw[data_raw["task"] == 3002].copy()
		# args add
		o2 = data_["result1"].values & 0xFFFF
		o1 = data_["result1"].values >> 16
		data_["arg4"] = 0
		data_["result"] = abs(o1 - data_["theory"])
		data_t = [data_.copy() for _ in range(4)]
		for i in range(4):
			data_t[i]["arg4"] = i
			if i == 1:
				data_t[i]["result"] = abs(o2 - data_["theory"])
			elif i == 2:
				data_t[i]["result"] = abs(o1 / (o2 + 1e-4))
			elif i == 3:
				data_t[i]["result"] = abs(o1)
		data_ = pd.concat(data_t, ignore_index=True)
		data_ = data_.drop(columns=["result1", "result2", "theory"])
		# filter
		if "esp32" in device_types and reduction and len(device_types) == 1:
			data_ = data_[data_["arg3"] % 16 == 0]
			data_ = data_.reset_index(drop=True)
		elif "stm32f103" in device_types and len(device_types) == 1:
			data_ = data_[data_["arg3"] % 1024 == 0]
		save_dataset(data_, repeat, name)

		# PWM
		name = "PWM"
		data_ = data_raw[data_raw["task"] == 3004].copy()
		data_["result"] = data_["result1"]
		data_ = data_.drop(columns=["result1", "result2", "theory"])
		# filter
		if "esp32" in device_types and reduction:
			data_ = data_[data_["arg1"] % 256 == 0]
			data_ = data_.reset_index(drop=True)
		save_dataset(data_, repeat, name)
	elif task_name == "clock":
		# RTCFre
		name = "RTCFre"
		data_ = data_raw[data_raw["task"] == 4000].copy()
		data_["result"] = data_["result1"]
		data_ = data_.drop(columns=["result1", "result2"])
		# filter
		if "esp32" in device_types and reduction:
			data_ = data_[data_["arg1"] % 32 == 0]
			data_ = data_.reset_index(drop=True)
		save_dataset(data_, repeat, name)
		# RTCPha
		name = "RTCPha"
		data_ = data_raw[data_raw["task"] == 4003].copy()
		data_["result"] = data_["result1"]
		data_ = data_.drop(columns=["result1", "result2"])
		# filter
		if "esp32" in device_types and reduction:
			data_ = data_[(data_["arg1"] - 100) % 6400 == 0]
			data_ = data_.reset_index(drop=True)
		save_dataset(data_, repeat, name)
	elif task_name == "fpu":
		name = "FPU"
		data_ = data_raw.copy()
		data_["result"] = data_["result1"]
		data_ = data_.drop(columns=["result1", "result2"])
		# filter
		if "esp32" in device_types and reduction:
			data_ = data_[(data_["arg2"] % 8 == 0)]
			data_ = data_.reset_index(drop=True)
		save_dataset(data_, repeat, name)
	elif task_name == "storage":
		name = "SRAM"
		data_ = data_raw.copy()
		data_["arg1"] = data_["result1"].values + data_["arg1"].values
		data_["result"] = data_["result2"]
		# filter
		if "esp32" not in device_types:
			data_ = data_[data_["arg1"] >= 9000]
			# data_ = data_[data_["arg1"] <= 5000]
			data_["arg1"] = data_["arg1"].values - 9000
			data_ = data_.drop(columns=["result1", "result2"])
		# filter
		if "esp32" in device_types and reduction:
			data_ = data_[data_["arg1"] <= 7200]
			data_ = data_[data_["arg1"] >= 3600]
			data_["arg1"] = data_["arg1"] - 3600
			data_ = data_.reset_index(drop=True)
		save_dataset(data_, repeat, name)

def read_all_data(device_types, file_dir, reduction=False):
	# single file format
	esp32_format = pd.DataFrame(columns=["arg1", "arg2", "arg3", "arg4"])
	arg1 = list(np.array(list([0, 1]))) * len(range(0, 256, 1))
	arg1 += list(range(16, 8016, 16)) * len(range(0, 3, 2)) * len(range(2500, 6000, 2500))
	arg1 += list([0])
	arg1 += list(np.array(list([0, 1]))) * len(range(0, 256, 1))
	arg1 += list(range(16, 8016, 16)) * len(range(0, 3, 2)) * len(range(2500, 6000, 2500))
	esp32_format["arg1"] = arg1
	arg2 = list([0]) * len(list([0, 1])) * len(range(0, 256, 1))
	arg2 += list([0]) * len(range(16, 8016, 16)) * len(range(0, 3, 2)) * len(range(2500, 6000, 2500))
	arg2 += list([0])
	arg2 += list([1]) * len(list([0, 1])) * len(range(0, 256, 1))
	arg2 += list([1]) * len(range(16, 8016, 16)) * len(range(0, 3, 2)) * len(range(2500, 6000, 2500))
	esp32_format["arg2"] = arg2
	arg3 = list(np.array(range(0, 256, 1)).repeat(len(list([0, 1]))))
	arg3 += list(np.array(range(0, 3, 2)).repeat(len(range(16, 8016, 16)))) * len(range(2500, 6000, 2500))
	arg3 += list([0])
	arg3 += list(np.array(range(0, 256, 1)).repeat(len(list([0, 1]))))
	arg3 += list(np.array(range(0, 3, 2)).repeat(len(range(16, 8016, 16)))) * len(range(2500, 6000, 2500))
	esp32_format["arg3"] = arg3
	arg4 = list([0]) * len(list([0, 1])) * len(range(0, 256, 1))
	arg4 += list(np.array(range(2500, 6000, 2500)).repeat(len(range(16, 8016, 16)) * len(range(0, 3, 2))))
	arg4 += list([0])
	arg4 += list([0]) * len(list([0, 1])) * len(range(0, 256, 1))
	arg4 += list(np.array(range(2500, 6000, 2500)).repeat(len(range(16, 8016, 16)) * len(range(0, 3, 2))))
	esp32_format["arg4"] = arg4
	theory = list(np.array([[8191/255, 3300/255]]).repeat(len(range(0, 256, 1))))
	theory += list(np.array(range(2500, 6000, 2500)).repeat(len(range(16, 8016, 16)) * len(range(0, 3, 2))))
	theory += list([0])
	theory += list(np.array([[8191/255, 3300/255]]).repeat(len(range(0, 256, 1))))
	theory += list(np.array(range(2500, 6000, 2500)).repeat(len(range(16, 8016, 16)) * len(range(0, 3, 2))))
	esp32_format["theory"] = theory

	stm32_format = pd.DataFrame(columns=["arg1", "arg2", "arg3", "arg4"])
	# format & duty
	arg1 = list(np.array(list([0, 1]))) * len(range(0, 4096, 128))
	arg1 += list(range(1, 999, 50)) * len(range(0, 1, 1)) * len(range(100, 150, 10))
	stm32_format["arg1"] = arg1
	# vref
	arg2 = list([0]) * len(list([0, 1])) * len(range(0, 4096, 128))
	arg2 += list([0]) * len(range(1, 999, 50)) * len(range(0, 1, 1)) * len(range(100, 150, 10))
	stm32_format["arg2"] = arg2
	# clock_source
	arg3 = list(np.array(range(0, 4096, 128)).repeat(len(list([0, 1]))))
	arg3 += list(np.array(range(0, 1, 1)).repeat(len(range(1, 999, 50)))) * len(range(100, 150, 10))
	stm32_format["arg3"] = arg3
	# freq
	arg4 = list([0]) * len(list([0, 1])) * len(range(0, 4096, 128))
	arg4 += list(np.array(range(100, 150, 10)).repeat(len(range(1, 999, 50)) * len(range(0, 1, 1))))
	stm32_format["arg4"] = arg4
	# theory
	theory = list(np.array([[8191/4095, 3300/4095]]).repeat(len(range(0, 4096, 128))))
	theory += list(np.array(range(100, 150, 10)).repeat(len(range(1, 999, 50)) * len(range(0, 1, 1))))
	stm32_format["theory"] = theory

	stm32f103_format = pd.DataFrame(columns=["arg1", "arg2", "arg3", "arg4"])
	# format & duty
	arg1 = list(np.array(list([0, 1]))) * len(range(0, 4096, 128))
	arg1 += list(range(1, 999, 50)) * len(range(0, 1, 1)) * len(range(80, 130, 10))
	stm32f103_format["arg1"] = arg1
	# vref
	arg2 = list([0]) * len(list([0, 1])) * len(range(0, 4096, 128))
	arg2 += list([0]) * len(range(1, 999, 50)) * len(range(0, 1, 1)) * len(range(80, 130, 10))
	stm32f103_format["arg2"] = arg2
	# clock_source
	arg3 = list(np.array(range(0, 4096, 128)).repeat(len(list([0, 1]))))
	arg3 += list(np.array(range(0, 1, 1)).repeat(len(range(1, 999, 50)))) * len(range(80, 130, 10))
	stm32f103_format["arg3"] = arg3
	# freq
	arg4 = list([0]) * len(list([0, 1])) * len(range(0, 4096, 128))
	arg4 += list(np.array(range(80, 130, 10)).repeat(len(range(1, 999, 50)) * len(range(0, 1, 1))))
	stm32f103_format["arg4"] = arg4
	# theory
	theory = list(np.array([[8191/4095, 3300/4095]]).repeat(len(range(0, 4096, 128))))
	theory += list(np.array(range(80, 130, 10)).repeat(len(range(1, 999, 50)) * len(range(0, 1, 1))))
	stm32f103_format["theory"] = theory

	data_read(
		repeat=5,
		device_types=device_types,
		data_format={
			"esp32": esp32_format,
			"stm32": stm32_format,
			"stm32f103": stm32f103_format,
		},
		env_dir=file_dir,
		reduction=reduction
	)

	# single file format
	esp32_format = pd.DataFrame(columns=["arg1", "arg2", "arg3", "arg4"])
	arg1 = list(range(0, 256, 2)) * len(range(0, 4)) * len(range(0, 2)) * len(range(50, 250, 50))
	arg1 += list(range(100, 40000, 400)) * len(range(0, 4)) * len(range(0, 2)) * len(range(50, 250, 50))
	esp32_format["arg1"] = arg1
	arg2 = list(np.array(list(range(0, 4))).repeat(len(range(0, 256, 2)))) * len(range(0, 2)) * len(range(50, 250, 50))
	arg2 += list(np.array(list(range(0, 4))).repeat(len(range(100, 40000, 400)))) * len(range(0, 2)) * len(range(50, 250, 50))
	esp32_format["arg2"] = arg2
	arg3 = list(np.array(list(range(0, 2))).repeat(len(range(0, 256, 2)) * len(range(0, 4)))) * len(range(50, 250, 50))
	arg3 += list(np.array(list(range(0, 2))).repeat(len(range(100, 40000, 400)) * len(range(0, 4)))) * len(range(50, 250, 50))
	esp32_format["arg3"] = arg3
	arg4 = list(np.array(list(range(50, 250, 50))).repeat(len(range(0, 256, 2)) * len(range(0, 4)) * len(range(0, 2))))
	arg4 += list(np.array(list(range(50, 250, 50))).repeat(len(range(100, 40000, 400)) * len(range(0, 4)) * len(range(0, 2))))
	esp32_format["arg4"] = arg4
	
	stm32_format = pd.DataFrame(columns=["arg1", "arg2", "arg3", "arg4"])
	arg1 = list(range(20, 120, 5)) * len(range(1, 3, 1)) * len(range(1, 3, 1)) * len(range(0, 1, 1))
	arg1 += list(range(10000, 50000, 2000)) * len(range(1, 3, 1)) * len(range(0, 1, 1)) * len(range(50, 70, 10))
	stm32_format["arg1"] = arg1
	arg2 = list(np.array(list(range(1, 3, 1))).repeat(len(range(20, 120, 5)))) * len(range(1, 3, 1)) * len(range(0, 1, 1))
	arg2 += list(np.array(list(range(1, 3, 1))).repeat(len(range(10000, 50000, 2000)))) * len(range(0, 1, 1)) * len(range(50, 70, 10))
	stm32_format["arg2"] = arg2
	arg3 = list(np.array(list(range(1, 3, 1))).repeat(len(range(20, 120, 5)) * len(range(1, 3, 1)))) * len(range(0, 1, 1))
	arg3 += list(np.array(list(range(0, 1, 1))).repeat(len(range(10000, 50000, 2000)) * len(range(1, 3, 1)))) * len(range(50, 70, 10))
	stm32_format["arg3"] = arg3
	arg4 = list(np.array(list(range(0, 1, 1))).repeat(len(range(20, 120, 5)) * len(range(1, 3, 1)) * len(range(1, 3, 1))))
	arg4 += list(np.array(list(range(50, 70, 10))).repeat(len(range(10000, 50000, 2000)) * len(range(1, 3, 1)) * len(range(0, 1, 1))))
	stm32_format["arg4"] = arg4

	stm32f103_format = stm32_format.copy()

	data_read(
		repeat=5,
		device_types=device_types,
		data_format={
			"esp32": esp32_format,
			"stm32": stm32_format,
			"stm32f103": stm32f103_format,
		},
		task_name="clock",
		env_dir=file_dir,
		reduction=reduction
	)

	esp32_format = pd.DataFrame(columns=["arg1", "arg2", "arg3"])
	arg1 = list(range(1, 89, 3)) * len(range(1, 89, 3)) * 2
	esp32_format["arg1"] = arg1
	arg2 = list(np.array(list(range(1, 89, 3))).repeat(len(range(1, 89, 3)))) * 2
	esp32_format["arg2"] = arg2
	arg3 = list(np.array(list([0, 1])).repeat(len(range(1, 89, 3)) * len(range(1, 89, 3))))
	esp32_format["arg3"] = arg3

	stm32_format = pd.DataFrame(columns=["arg1", "arg2", "arg3"])
	arg1 = list(range(1, 21, 2)) * len(range(1, 21, 2))
	arg1 += list(range(1, 21, 2)) * len(range(1, 21, 2))
	stm32_format["arg1"] = arg1
	arg2 = list(np.array(list(range(1, 21, 2))).repeat(len(range(1, 21, 2))))
	arg2 += list(np.array(list(range(1, 21, 2))).repeat(len(range(1, 21, 2))))
	stm32_format["arg2"] = arg2
	arg3 = list(np.array(list([0])).repeat(len(range(1, 21, 2)) * len(range(1, 21, 2))))
	arg3 += list(np.array(list([1])).repeat(len(range(1, 21, 2)) * len(range(1, 21, 2))))
	stm32_format["arg3"] = arg3

	stm32f103_format = pd.DataFrame(columns=["arg1", "arg2", "arg3"])
	arg1 = list(range(1, 21, 2)) * len(range(1, 21, 2))
	arg1 += list(range(1, 21, 2)) * len(range(1, 21, 2))
	stm32f103_format["arg1"] = arg1
	arg2 = list(np.array(list(range(1, 21, 2))).repeat(len(range(1, 21, 2))))
	arg2 += list(np.array(list(range(1, 21, 2))).repeat(len(range(1, 21, 2))))
	stm32f103_format["arg2"] = arg2
	arg3 = list(np.array(list([0])).repeat(len(range(1, 21, 2)) * len(range(1, 21, 2))))
	arg3 += list(np.array(list([1])).repeat(len(range(1, 21, 2)) * len(range(1, 21, 2))))
	stm32f103_format["arg3"] = arg3

	data_read(
		repeat=5,
		device_types=device_types,
		data_format={
			"esp32": esp32_format,
			"stm32": stm32_format,
			"stm32f103": stm32f103_format,
		},
		task_name="fpu",
		env_dir=file_dir,
		reduction=reduction
	)

	esp32_format = pd.DataFrame(columns=["arg1", "arg2"])
	arg1 = [- 0x3FFD0000 for _ in range(5001)]
	esp32_format["arg1"] = arg1
	arg2 = 4
	esp32_format["arg2"] = arg2
	
	stm32_format = pd.DataFrame(columns=["arg1", "arg2"])
	arg1 = [- 0x20000000 for _ in range(2501)]
	stm32_format["arg1"] = arg1
	arg2 = [4 for _ in range(2501)]
	stm32_format["arg2"] = arg2

	stm32f103_format = pd.DataFrame(columns=["arg1", "arg2"])
	arg1 = [- 0x20000000 for _ in range(2501)]
	stm32f103_format["arg1"] = arg1
	arg2 = [4 for _ in range(2501)]
	stm32f103_format["arg2"] = arg2

	data_read(
		repeat=1,
		device_types=device_types,
		data_format={
			"esp32": esp32_format,
			"stm32": stm32_format,
			"stm32f103": stm32f103_format,
		},
		task_name="storage",
		env_dir=file_dir,
		reduction=reduction
	)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--device_type", dest="device_type", type=str, default="esp32")
	parser.add_argument("--reduction", dest="reduction", type=int, default=0)
	args_parser = parser.parse_args()
	read_all_data([args_parser.device_type], "all_data", args_parser.reduction)
	# read_all_data(["esp32"], "all_data")