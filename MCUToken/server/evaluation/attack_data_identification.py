import pandas as pd
import numpy as np

import argparse
import sklearn.ensemble
import sklearn.tree
import sklearn.cluster
import sklearn.preprocessing

from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("--noise", dest="noise", type=float, default=0.01)
args_parser = parser.parse_args()

task_list = [
  "DAC_ADC",
  "RTCFre",
  "FPU",
  # "RTCPha",
  "SRAM",
  "PWM",
]

target_label = 0

for task_name in task_list:
  # data read
  data_raw = pd.read_csv("dataset/{}.csv".format(task_name))
  data_ = data_raw[data_raw["label"] == target_label].reset_index(drop=True) 
  data_["previous"] = data_["1"]
  file_number = 3 if task_name == "SRAM" else 11
  data_ = data_.drop(columns=[str(i) for i in range(0, file_number)])

  # data modified
  # data_["modify"] = data_["previous"] * 1.1
  noise = args_parser.noise
  if noise > 0:
    data_["modify"] = data_["previous"] * (1+noise)
  else:
    noise = 0.08
    data_["modify"] = data_["previous"] * (1+np.random.uniform(noise, 0.2)) + 1.0
  data_["label"] = np.random.randint(0,2,len(data_))
  data_.loc[data_["label"] == 0, "X"] = data_[data_["label"] == 0]["previous"].values
  data_.loc[data_["label"] == 1, "X"] = data_[data_["label"] == 1]["modify"].values

  # label predict: cluster
  scaler = sklearn.preprocessing.MinMaxScaler()
  X = [args for args in data_.columns if "arg" in args]
  X.append("X")
  X = data_[X].values

  # predict_label = sklearn.cluster.MiniBatchKMeans(n_clusters=2, n_init="auto").fit_predict(X)
  predict_label = sklearn.cluster.AgglomerativeClustering(n_clusters=2).fit_predict(X)
  # predict_label = sklearn.cluster.KMeans(n_clusters=2, n_init="auto").fit_predict(X)
  # predict_label = sklearn.cluster.BisectingKMeans(n_clusters=2).fit_predict(X)
  # predict_label = sklearn.ensemble.IsolationForest().fit_predict(X)
  # predict_label = predict_label == -1

  result = np.sum(predict_label == data_["label"].values) / len(predict_label)
  result = result if result > 0.5 else 1 - result
  print("cluster", "task_name:{}".format(task_name), result)

  # predictor
  data_ = data_.copy()
  repeat = 20
  
  for trainset_frac in [0.01, 0.05, 0.1, 0.2, 0.3, 0.5]:
    results = []
    for _ in range(repeat):
      data_ = data_.sample(frac=1.0)
      traindata = data_.iloc[0:int(len(data_)*trainset_frac), :]
      testdata = data_.iloc[int(len(data_)*trainset_frac):, ]
      predictor = sklearn.ensemble.ExtraTreesRegressor()
      predictor.fit(traindata[[args for args in data_.columns if "arg" in args]], traindata["X"].values)
      data_ref = predictor.predict(data_[[args for args in data_.columns if "arg" in args]])
      data_real = data_["X"].values
      dis = np.abs(data_ref - data_real) / (data_real + 1e-4)
      predict_label = (dis >= noise).reshape(-1)
      result = np.sum(predict_label == data_["label"].values) / len(predict_label)
      results.append(result)
    print("train-partly {}".format(trainset_frac), "task_name:{}".format(task_name), np.mean(results))

  # continuous learning
  for train_step in [2, 5, 10, 20, 30]:
    results = []
    for _ in range(2):
      data_ = data_.sample(frac=1.0)
      predictor = sklearn.ensemble.ExtraTreesRegressor()
      traindata = data_.iloc[0:train_step, :]
      for i in tqdm(range(train_step, len(data_), train_step), leave=False, colour="YELLOW"):
        data_t = data_.iloc[i:min(i+train_step, len(data_)), :].copy()
        predictor.fit(traindata[[args for args in data_.columns if "arg" in args]], traindata["X"].values)
        data_ref = predictor.predict(data_t[[args for args in data_.columns if "arg" in args]])
        data_real = data_t["X"].values
        dis = np.abs(data_ref - data_real) / (data_real + 1e-4)
        predict_label = (dis >= noise).reshape(-1)
        data_t["label"] = predict_label.astype(int)
        traindata = pd.concat([traindata, data_t[data_t["label"] == 0]], ignore_index=True)
      data_ref = predictor.predict(data_[[args for args in data_.columns if "arg" in args]])
      data_real = data_["X"].values
      dis = np.abs(data_ref - data_real) / (data_real + 1e-4)
      predict_label = (dis >= noise).reshape(-1)
      result = np.sum(predict_label == data_["label"].values) / len(predict_label)
      results.append(result)
    print("train-step {}".format(train_step), "task_name:{}".format(task_name), np.mean(results))

  # with help with another device
  data_ = data_.sort_index()
  results = []
  for other_label in range(18):
    if other_label == target_label:
      continue
    data_addition = data_raw[data_raw["label"] == other_label].reset_index(drop=True) 
    data_ref = data_addition["1"].values
    data_real = data_["X"].values
    dis = np.abs(data_ref - data_real) / (data_real + 1e-4)
    predict_label = (dis >= noise).reshape(-1)
    result = np.sum(predict_label == data_["label"].values) / len(predict_label)
    results.append(result)
  print("extra-device", "task_name:{}".format(task_name), np.mean(results))
    