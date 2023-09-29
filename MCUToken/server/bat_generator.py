import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--device_type", dest="device_type", type=str, default="STM32")
parser.add_argument('--device_number', nargs='+')
parser.add_argument('--port', nargs='+')
parser.add_argument('--target_file', type=str, default="all_data/")
parser.add_argument('--only_sram', type=int, default=0)
parser.add_argument('--times', type=int, default=11)
args_parser = parser.parse_args()

only_sram = args_parser.only_sram

devices = [
  args_parser.device_type + "_" + number for number in args_parser.device_number
]

coms = args_parser.port

n = args_parser.times
target_file = args_parser.target_file + "/"
if not os.path.exists("raw_data/{}".format(target_file)):
  os.mkdir("raw_data/{}".format(target_file))
for i in range(len(devices)):
  f = open("run_get_dataset_{}.bat".format(coms[i]), "w")
  if not only_sram:
    f.write("python collect_data.py -r 1 -c tasks/task_voltage.yaml -o raw_data/{}/voltage -n {} -d {} -m {}\n".format(target_file, n, devices[i], coms[i]))
    f.write("python collect_data.py -r 1 -c tasks/task_clock.yaml -o raw_data/{}/clock -n {} -d {} -m {}\n".format(target_file, n, devices[i], coms[i]))
    f.write("python collect_data.py -r 1 -c tasks/task_fpu.yaml -o raw_data/{}/fpu -n {} -d {} -m {}\n".format(target_file, n, devices[i], coms[i]))
   
  f.write("python collect_data.py -r 1 -c tasks/task_store.yaml -o raw_data/{}/storage -n 1 -d {} -m {}\n".format(target_file, devices[i], coms[i]))