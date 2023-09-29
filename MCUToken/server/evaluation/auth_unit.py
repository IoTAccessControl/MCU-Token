import sklearn.ensemble
import sklearn.cluster
import pandas as pd
import numpy as np
import pickle

class AuthenticationUnitNormal:
	def __init__(self, task_name, target_label, repeat):
		self.task_name = task_name
		self.target_label = target_label
		self.repeat = repeat
	
	def train_predictor(self, data):
		data = data.copy()
		data = data[data["label"] == self.target_label]
		data = data.reset_index(drop=True)
		data = data.sample(n=len(data))
		y_train = data[[str(i) for i in range(self.repeat)]].values
		X_train = data[[args for args in data.columns if "arg" in args]].values

		# model can be changed here
		model = sklearn.ensemble.ExtraTreesRegressor()
		if y_train.shape[1] == 1:
			y_train = y_train.ravel()
		model.fit(X_train, y_train)
		self.predictor = model

	def get_classfier_input(self, data, movement):
		result_len = self.repeat if movement == "train" else 1

		result_list = self.predictor.predict(data[[args for args in data.columns if "arg" in args]].values)
		result_list = result_list.repeat(result_len, axis=0)

		data_real = data[[str(i) for i in range(result_len)]].values
		data_real = np.array(data_real).reshape(-1,1)
		if self.repeat == 1:
			result_list = result_list.reshape(-1, 1)
		classfier_input = np.concatenate([
			np.min(abs(result_list - data_real + 1e-4) / (data_real + 1e-4), axis=1).reshape(-1, 1),
			np.mean(abs(result_list - data_real + 1e-4) / (data_real + 1e-4), axis=1).reshape(-1, 1),
			np.max(abs(result_list - data_real + 1e-4) / (data_real + 1e-4), axis=1).reshape(-1, 1),
		], axis=1)
		classfier_input = pd.DataFrame(classfier_input)
		return classfier_input

	def train_classifier(self, data, device_labels, device_sample_number):
		data_raw = data.copy()
		data = data.copy()
		data = data.reset_index(drop=True)

		negative_labels = list(device_labels)
		negative_labels.remove(self.target_label)
		np.random.shuffle(negative_labels)
		negative_labels = list(negative_labels)

		for label in negative_labels[device_sample_number : ]:
			data = data.drop(index=data[data["label"] == label].index)
			
		result_len = self.repeat
		labels = (data["label"].values == self.target_label).astype(float).repeat(result_len)
		classfier_input = self.get_classfier_input(data, "train")
		classfier_input["label"] = labels

		classfier_input_pos_index = np.array(classfier_input[classfier_input["label"] == 1.0].index)
		classfier_input_pos = np.array(classfier_input[classfier_input["label"] == 1.0].iloc[:, 0].values)
		classfier_input_pos_index = classfier_input_pos_index[np.argsort(classfier_input_pos)]
		classfier_input_pos = np.array(sorted(classfier_input_pos))

		classfier_input_neg_index = np.array(classfier_input[classfier_input["label"] == 0.0].index)
		classfier_input_neg = np.array(classfier_input[classfier_input["label"] == 0.0].iloc[:, 0].values)
		classfier_input_neg_index = classfier_input_neg_index[np.argsort(classfier_input_neg)]
		classfier_input_neg = np.array(sorted(classfier_input_neg))

		pos_remain_rate = 0.85
		if self.task_name == "RTCFre":
			pos_remain_rate = 0.95
		classfier_input_pos_index = classfier_input_pos_index[ : int(pos_remain_rate*len(classfier_input_pos_index))]
		classfier_input_pos = classfier_input_pos[ : int(pos_remain_rate*len(classfier_input_pos))]

		t = classfier_input_neg[classfier_input_neg > np.max(classfier_input_pos)]
		neg_rate = 0.9
		while len(t) == 0:
			t = classfier_input_neg[classfier_input_neg > np.max(classfier_input_pos) * neg_rate]
			neg_rate = neg_rate*0.9
		classfier_input_neg_index = classfier_input_neg_index[classfier_input_neg > np.max(classfier_input_pos) * neg_rate]
		classfier_input_neg = t
		
		classfier_input = classfier_input.iloc[np.concatenate([classfier_input_pos_index, classfier_input_neg_index]), :]
		classfier_input = classfier_input.reset_index(drop=True)
		data = classfier_input
		
		data = data.sample(n=len(data))
		# model can be changed here
		classifier = sklearn.ensemble.RandomForestClassifier()
		classifier.fit(data[data.columns[:-1]].values, data["label"].values)
		self.classifier = classifier

		data_array = np.array(data_raw[[str(i) for i in range(self.repeat)]])
		data_array = data_array.T
		np.random.shuffle(data_array)
		data_array = pd.DataFrame(data_array.T)
		data_raw["0"] = data_array[0].values
		_, _, (TP, TN, FP, FN) = self.get_result(data_raw)
		self.TPR = TP / (TP + FN) if (TP + FN) != 0 else 0
		self.FPR = FP / (TN + FP) if (TN + FP) != 0 else 0
		
	def get_result(self, data):
		data = data.copy()
		data = data.reset_index(drop=True)

		result_len = 1
		labels = (data["label"].values == self.target_label).astype(float).repeat(result_len)
		classfier_input = self.get_classfier_input(data, "test")
		classfier_input["label"] = labels
		data = classfier_input
		
		classifier = self.classifier
		predict_result = classifier.predict(data[data.columns[:-1]].values)
		predict_result_prob = classifier.predict_proba(data[data.columns[:-1]].values)[:, 1]

		TP = np.sum(np.logical_and(data["label"] == 1, predict_result == data["label"].values))
		TN = np.sum(np.logical_and(data["label"] == 0, predict_result == data["label"].values))
		FP = np.sum(np.logical_and(data["label"] == 0, predict_result != data["label"].values))
		FN = np.sum(np.logical_and(data["label"] == 1, predict_result != data["label"].values))
		return predict_result, predict_result_prob, (TP, TN, FP, FN)
	
	def load_trained_model(self, predictor_path, classifier_path):
		self.predictor = pickle.load(open(predictor_path, "rb"))
		self.classifier = pickle.load(open(classifier_path, "rb"))

	def save_trained_model(self, predictor_path, classifier_path):
		pickle.dump(self.predictor, open(predictor_path, "wb"))
		pickle.dump(self.classifier , open(classifier_path, "wb"))

	def get_ref_result(self, data):
		result_len = 1
		result_list = self.predictor.predict(data[[args for args in data.columns if "arg" in args]].values)
		result_list = result_list.repeat(result_len, axis=0)
		return result_list

class AuthenticationSRAM:
	def __init__(self, task_name, target_label, _="unuse"):
		self.task_name = task_name
		self.target_label = target_label
		self.repeat = 1

	def train_predictor(self, data):
		data = data.copy()
		data = data[data["label"] == self.target_label]
		data = data.reset_index(drop=True)
		data = data.drop_duplicates(["arg1"])
		data = data.sort_values(by=["arg1"])
		self.device_sram_dict = data[[str(i) for i in range(self.repeat)]].values.ravel()

	def get_classfier_input(self, data, _="unuse"):
		stored_sram = self.device_sram_dict[(data["arg1"].values // 4).astype(np.int32)]
		true_sram = data["0"].values.astype(np.int64)
		same_bit_number = np.array([0 for _ in range(len(true_sram))])
		for _ in range(32):
			same_bit_number += (stored_sram & 1) == (true_sram & 1)
			stored_sram >>= 1
			true_sram >>= 1
		assert(np.sum(stored_sram == 0) == len(stored_sram))
		assert(np.sum(true_sram == 0) == len(true_sram))
		classfier_input = pd.DataFrame()
		classfier_input["0"] = 1. - same_bit_number / 32
		return classfier_input
	
	def train_classifier(self, data, device_labels, device_sample_number):
		data_raw = data.copy()
		data = data.drop_duplicates(["label", "arg1"], keep="last") # 特殊化处理 special
		data_sample = [i for i in device_labels]
		np.random.shuffle(data_sample)
		for i in data_sample[device_sample_number: ]:
			if i == self.target_label:
				continue
			data = data.drop(data[data["label"] == i].index)

		labels = (data["label"].values == self.target_label).astype(float)
		classfier_input = self.get_classfier_input(data)
		classfier_input["label"] = labels

		classfier_input_pos_index = np.array(classfier_input[classfier_input["label"] == 1.0].index)
		classfier_input_pos = np.array(classfier_input[classfier_input["label"] == 1.0].iloc[:, 0].values)
		classfier_input_pos_index = classfier_input_pos_index[np.argsort(classfier_input_pos)]
		classfier_input_pos = np.array(sorted(classfier_input_pos))

		classfier_input_neg_index = np.array(classfier_input[classfier_input["label"] == 0.0].index)
		classfier_input_neg = np.array(classfier_input[classfier_input["label"] == 0.0].iloc[:, 0].values)
		classfier_input_neg_index = classfier_input_neg_index[np.argsort(classfier_input_neg)]
		classfier_input_neg = np.array(sorted(classfier_input_neg))

		pos_remain_rate = 0.9
		classfier_input_pos_index = classfier_input_pos_index[ : int(pos_remain_rate*len(classfier_input_pos_index))]
		classfier_input_pos = classfier_input_pos[ : int(pos_remain_rate*len(classfier_input_pos))]
		classfier_input_neg_index = classfier_input_neg_index[classfier_input_neg > np.max(classfier_input_pos)]
		classfier_input_neg = classfier_input_neg[classfier_input_neg > np.max(classfier_input_pos)]

		classfier_input = classfier_input.iloc[np.concatenate([classfier_input_pos_index, classfier_input_neg_index]), :]
		classfier_input = classfier_input.reset_index(drop=True)
		data = classfier_input

		classifier = sklearn.ensemble.RandomForestClassifier()
		classifier.fit(data[["0"]].values, data["label"].values)
		self.classifier = classifier
		
		_, _, (TP, TN, FP, FN) = self.get_result(data_raw)
		self.TPR = TP / (TP + FN) if (TP + FN) != 0 else 0
		self.FPR = FP / (TN + FP) if (TN + FP) != 0 else 0

	def get_result(self, data):
		labels = (data["label"].values == self.target_label).astype(float)
		data = self.get_classfier_input(data)
		data["label"] = labels
		classifier = self.classifier
		predict_result = classifier.predict(data[["0"]].values)
		predict_result_prob = classifier.predict_proba(data[["0"]].values)[:, 1]

		TP = np.sum(np.logical_and(data["label"] == 1, predict_result == data["label"].values))
		TN = np.sum(np.logical_and(data["label"] == 0, predict_result == data["label"].values))
		FP = np.sum(np.logical_and(data["label"] == 0, predict_result != data["label"].values))
		FN = np.sum(np.logical_and(data["label"] == 1, predict_result != data["label"].values))
		return predict_result, predict_result_prob, (TP, TN, FP, FN)
	
	def get_ref_result(self, data):
		stored_sram = self.device_sram_dict[data["arg1"].values // 4]
		return stored_sram