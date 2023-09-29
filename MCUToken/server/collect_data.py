# coding: utf-8
import sys
import io
import os
import json
import logging
import codecs
import ctypes
import struct
import random
import signal
from time import sleep
from typing import Dict
import datetime
import argparse
import serial
from omegaconf import OmegaConf
from serial.tools import list_ports
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('iDevFi-Tool')

ctlr_c_exit = False


class PacketType:
	PKT_LOG = 1
	PKT_DATA = 2


class Event(ctypes.Structure):
	_pack_ = 1
	_fields_ = [
		("eid", ctypes.c_uint32),
		('ti', ctypes.c_uint32),
		('val', ctypes.c_uint32),
	]

	@staticmethod
	def init_from_bytes(bys):
		return Event(*struct.unpack("<III", bys))


class MySerial:

	def __init__(self, ser):
		self.serial = ser
		self.rx_decoder = codecs.getincrementaldecoder("UTF-8")("replace")
		self.tx_encoder = codecs.getincrementalencoder("UTF-8")("replace")
		self.out_fp = None
		self.conf = None

		# 用于中途退出重制种子使用
		self.skip_number = 0

		# 用于收集同一参数的不同结果
		self.repeat_time = 10

	def run_data_collect_tasks(self, conf):
		print("\n============================================")
		logger.info(f"Start new Task -> {conf['File']}")
		# open files
		if self.skip_number <= 0:
			self.out_fp = self.create_csv(conf)
		plat = conf["Platform"]
		tasks = conf["Task"]
		for task in tasks:
			argc = int(task["argc"])
			task_cmd = f"fp_gen {plat}"
			for i in range(argc):
				task_cmd += " " + str(task["arg" + str(i)])
			task_cmd += "\n"
			self.out_task_cmd = task_cmd.replace("\n", " ").replace(" ", ", ")
			for _ in range(self.repeat_time):
				self.collect_one_task(task_cmd)
		if self.skip_number != 0:
			return
		self.save_and_close()
		logger.info(f"End the Task. Save log in path: {conf['Save']} for dev: {conf['Dev']} on platform: {plat}")
		print("============================================\n")
		sleep(0.2)

	def collect_one_task(self, task_cmd):
		print("--------------------------------------------")
		logger.info(f"Start to run task: {task_cmd.strip()}")
		self.write(task_cmd)
		# ignore the possible noisy data before transfer
		callback = self.wait_for_reset()
		while callback == "REDO":
			logger.info(f"Rerun task: {task_cmd.strip()}")
			sleep(0.2)
			self.write(task_cmd)
			callback = self.wait_for_reset()
		task_finish = False

		while not ctlr_c_exit:
			c = self.serial.read(1)
			if c == b'':
				if task_finish:
					logger.info("Finish Data Collection...")
					break
				else:
					continue

			pkt_type = ord(c)
			if pkt_type == PacketType.PKT_DATA:
				pkt_len = ord(self.serial.read(1))
				data = self.serial.read(pkt_len)
				if len(data) == ctypes.sizeof(Event):
					ev = Event.init_from_bytes(data)
					self.save(ev)

			elif pkt_type == PacketType.PKT_LOG: # other buffer
				pkt_len = ord(self.serial.read(1))
				data = self.serial.read(pkt_len)
				log = self.rx_decoder.decode(data)
				if "Finish Task" in log:
					task_finish = True
				elif "Task Failed" in log:
					task_finish = True
				print("[LOG]", log.strip())
				# if "RESULT" in log:
				# 	res_log = log
			else:
				# ignore zero reset bytes
				# print(f"Wait for Command: {pkt_type}", c)
				pass
		print("--------------------------------------------\n")

	def wait_for_reset(self):
		# before rest all input are regard as log
		zero_num_need = 10
		reset_char_num = 0
		waiting_time = 0
		while not ctlr_c_exit:
			c = self.serial.read(1)
			# logger.info(f"read: {c}")
			if c != b'':
				t = ord(c)
				# logger.info(f"t: {t}")
				if t == 0:
					reset_char_num += 1
				elif c == b'G':
					return "REDO"
				else:
					reset_char_num = 0
				if reset_char_num > zero_num_need:
					break
				# print("current status: ", reset_char_num, t)
			else:
				waiting_time += 1
				logger.info(f"Wait for Flush: {c}")
				if waiting_time > 30:
					logger.info("Failed to start task. Exit!")
					sys.exit(-1)
		return ""

	def save_and_close(self):
		self.out_fp.close()

	def write(self, data):
		self.serial.write(self.tx_encoder.encode(data))
		self.serial.flush()

	def create_csv(self, conf):
		fi = datetime.datetime.now().strftime("%m%d%H%M%S")
		out_file = f"{conf['Out']}/{conf['Dev']}_{fi}.csv"
		conf["Save"] = out_file
		return open(out_file, "w")

	def save(self, ev):
		self.out_fp.write(f"{ev.eid}, {ev.ti}, {ev.val}\n")


def open_serial_port(serial_port):
	ports = list(list_ports.grep(serial_port))
	if len(ports) < 1:
		ava_ports = '\n\t'.join([str(item) for item in list_ports.comports()])
		logger.error(f"Available ports: \n\t{ava_ports}")
		logger.error(f"Failed to open serial port: {serial_port}")
		exit(-1)
	port = ports[0]
	ser = serial.serial_for_url(port.device, 115200, timeout=1, do_not_open=False)
	logger.info(f"Success to open port: {port}")
	# esp32每次连接好像都会重启，输出一堆启动信息
	# flush_serial(ser)
	return ser


def parser_args():
	parser = argparse.ArgumentParser(description="uDeFi Data Collection")
	parser.add_argument("-m", "--com", required=True, help="Set COM Port")
	parser.add_argument("-o", "--out", default="out", help="Set Output Directory")
	parser.add_argument("-c", "--conf", default="task.yaml", help="Set Yaml Conf")
	parser.add_argument("-n", type=int, default=1, help="Run for n times.")
	parser.add_argument("-d", "--dev", default="", help="Set device name.")
	parser.add_argument("-s", "--seed", default=-1, type=int)
	parser.add_argument("-r", "--repeat", default=1, type=int)
	args = parser.parse_args()
	return args


def load_conf(out_dir: str, conf_fi: str):
	conf = OmegaConf.load(conf_fi)
	if not os.path.exists(out_dir):
		os.mkdir(out_dir)
	conf["Out"] = out_dir
	conf["File"] = conf_fi
	return conf


def signal_handler(sig, frame):
	global ctlr_c_exit
	ctlr_c_exit = True
	logger.info('You pressed Ctrl+C! Exit!')
	sys.exit(0)


def flush_serial(ser):
	while True:
		c = ser.read(1)
		if c == b'':
			break
		logger.info(f"Flush Extra Bytes: {c}")


def spending(tag):
	def timer_wrap(func):
		from time import time
		def wrap_func(*args, **kwargs):
			t1 = time()
			result = func(*args, **kwargs)
			t2 = time()
			print(f'Finsh {tag} in {(t2-t1):.2f}s')
			return result
		return wrap_func
	return timer_wrap

@spending('data collect')
def main():
	signal.signal(signal.SIGINT, signal_handler)

	args = parser_args()

	if args.seed != -1:
		random.seed(args.seed)

	serial_port = args.com
	out_dir = args.out
	conf_fi = args.conf
	conf = load_conf(out_dir, conf_fi)
	if args.dev != "":
		conf["Dev"] = args.dev
	logger.info(f"Current Setting: COM={args.com} Out: {out_dir}")
	ser = open_serial_port(serial_port)
	my_serial = MySerial(ser)

	my_serial.repeat_time = args.repeat

	for _ in range(args.n):
		my_serial.run_data_collect_tasks(conf)


if __name__ == "__main__":
	main()
