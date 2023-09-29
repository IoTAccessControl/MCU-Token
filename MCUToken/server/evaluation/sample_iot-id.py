from sklearnex import patch_sklearn, unpatch_sklearn
patch_sklearn()

import pandas as pd
import numpy as np
import sklearn
import sklearn.ensemble
import random
import argparse

from sklearn.model_selection import train_test_split
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("--repeat_time", dest="repeat_time", type=int, default=100)
args_parser = parser.parse_args()

data = pd.read_csv("./dataset/DAC_ADC.csv")

data = data[data["label"] < 10]
data = data[data["arg1"] == 0]
data = data[data["arg2"] == 0]
data = data[data["arg4"] == 0]
data = data.drop(columns=["task", "arg1", "arg2", "arg4", "0"])

vector_range = range(100, 200)
for i in range(len(set(data["arg3"].values))):
	if i not in vector_range:
		data = data.drop(index=data[data["arg3"] == i].index)
data = data.sort_values(["label", "arg3"])
data = data.reset_index(drop=True)

dataset = []
for label in range(10):
	data_t = data[data["label"] == label]
	dataset_t = pd.DataFrame(data_t[[str(i) for i in range(1, 11)]].values.T)
	dataset_t.insert(0, "label", label)
	dataset.append(dataset_t)
dataset = pd.concat(dataset, ignore_index=True)
data = dataset

# classifier
y = data.iloc[:,0].astype('int')
X = data.iloc[:,1:]
acc = 0
while acc != 1:
	X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.6)
	clf = sklearn.ensemble.RandomForestClassifier()
	clf.fit(X_train.values, y_train)
	y_pred = clf.predict(X_test.values)
	acc = np.sum(y_test == y_pred) / len(y_test)
	print("Accuracy", np.sum(y_test == y_pred) / len(y_test))

# attack: number
attack_sucess = {}
cosine_sim = {}
ratios = range(1, 30)
for ratio in tqdm(ratios):
  # break
  print("number-test", ratio, end=" ")
  results = []
  for _ in range(args_parser.repeat_time):
    y_obtained_set = y_test.sample(n=ratio)
    x_obtained_set = X_test.loc[y_obtained_set.index, :]
    y_obtained_set = y_obtained_set.values
    devices = np.array(list(set(y)))
    attack_model = sklearn.ensemble.RandomForestRegressor(max_features=1.0)
    attack_model.fit(y_obtained_set.reshape(-1, 1), x_obtained_set.values)
    # fake feature for every device
    fake_features = attack_model.predict(devices.reshape(-1, 1))
    # attack_success
    y_pred = clf.predict(fake_features)
    results.append(np.sum(devices == y_pred) / len(devices))
    print("obtain:{}, success: {}".format(len(set(y_obtained_set)), np.sum(devices == y_pred)))
  print(np.mean(results))

# attack: dim
dim_number = len(data.iloc[0, 1:])
devices = np.array(list(set(y)))
ratios = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
for ratio in tqdm(ratios):
  print("dim-test", ratio, end=" ")
  results = []
  for device in devices:
    fake_features = []
    for _ in range(100):
      obtained_dims = random.sample(list(range(dim_number)), ratio)
      obtained_dims = np.array(sorted(obtained_dims))
      data_sample = data[data["label"] == device].sample(frac=1.0).iloc[:, 1:].values
      np.random.shuffle(data_sample)
      fake_feature = np.zeros(dim_number)
      fake_feature[obtained_dims] = data_sample[0, obtained_dims]
      unknow_dims = np.array(list(set(range(dim_number)) - set(obtained_dims))).astype(int)
      other_dims = np.random.choice(data_sample[0, obtained_dims], dim_number-ratio)
      fake_feature[unknow_dims] = other_dims
      fake_features.append(fake_feature)
    y_pred = clf.predict(fake_features)
    results.append(np.sum(device == y_pred) / len(y_pred))
  print(np.mean(results))
