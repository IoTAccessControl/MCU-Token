import numpy as np
import random
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--test_type", dest="test_type", type=str, default="123")
parser.add_argument("--out_len", dest="out_len", type=int, default=2000)
args_parser = parser.parse_args()

def APHash(s):
	hash = 0xAAAAAAAA
	for i in range(len(s)):
		hash ^= ((hash <<  7) ^ (ord(s[i])) * (hash >> 3)) if ((int(i) & 1) == 0) else (~((hash << 11) + ((ord(s[i])) ^ (hash >> 5))))
		hash = hash & 0xFFFFFFFF
	return hash

def conflict_test():
	conflict = set()
	c = 0
	l = int(1e5)
	for i in tqdm(range(l)):
		res = APHash("open_the_car_door" + str(i))
		if res in conflict:
			c += 1
		else:
			conflict.add(res)
	print(c, c / l)

operation = "op"
payloads = []
random_number = []
digest = 0
results = []
Hash_fun = APHash

# Attack: modify operation
operation_total = [i for i in range(200)]
payloads_space = 2 ** 32
random_number_space = 2 ** 16
output_space = args_parser.out_len
epoch = 100

# H1 H2 H3
if args_parser.test_type == "123":
	for _ in tqdm(range(epoch)):
		[operation, modified_operation] = np.random.choice(operation_total, 2)
		payloads = [random.randint(0, payloads_space), random.randint(0, payloads_space)]
		random_number = random.randint(0, random_number_space)
		
		H1_0 = Hash_fun(str(operation) + str(random_number) + str(digest))
		H2_0 = Hash_fun(str(random_number) + str(payloads[0]))
		H3_0 = Hash_fun(str(random_number) + str(payloads[-1]))
		digest_0 = Hash_fun(str(H1_0) + str(H2_0) + str(H3_0))
		task_0 = digest_0 % output_space
		H1_1 = Hash_fun(str(operation) + str(random_number) + str(digest_0))
		H2_1 = Hash_fun(str(random_number) + str(payloads[1]))
		H3_1 = Hash_fun(str(random_number) + str(payloads[0]))
		digest_1 = Hash_fun(str(H1_1) + str(H2_1) + str(H3_1))
		task_1 = digest_1 % output_space

		modified_random_number = random.randint(0, random_number_space)
		modified_payloads = [random.randint(0, payloads_space), random.randint(0, payloads_space)]
		H1_0_ = Hash_fun(str(modified_operation) + str(modified_random_number) + str(digest))
		H2_0_ = Hash_fun(str(modified_random_number) + str(modified_payloads[0]))
		H3_0_ = Hash_fun(str(modified_random_number) + str(modified_payloads[-1]))
		digest_0_ = Hash_fun(str(H1_0_) + str(H2_0_) + str(H3_0_))
		task_0_ = digest_0_ % output_space
		H1_1_ = Hash_fun(str(modified_operation) + str(modified_random_number) + str(digest_0_))
		H2_1_ = Hash_fun(str(modified_random_number) + str(modified_payloads[1]))
		H3_1_ = Hash_fun(str(modified_random_number) + str(modified_payloads[0]))
		digest_1_ = Hash_fun(str(H1_1_) + str(H2_1_) + str(H3_1_))
		task_1_ = digest_1_ % output_space
		try_times = 0

		while task_0 != task_0_ or task_1_ != task_1:
			if task_0 != task_0_:
			# modified_random_number = random.randint(0, random_number_space)
				modified_payloads[0] = random.randint(0, payloads_space)
			if task_1 != task_1_:
			# modified_random_number = random.randint(0, random_number_space)
				modified_payloads[1] = random.randint(0, payloads_space)
			if task_0 != task_0_ and task_1 != task_1_:
				modified_random_number = random.randint(0, random_number_space)
			H1_0_ = Hash_fun(str(modified_operation) + str(modified_random_number) + str(digest))
			H2_0_ = Hash_fun(str(modified_random_number) + str(modified_payloads[0]))
			H3_0_ = Hash_fun(str(modified_random_number) + str(modified_payloads[-1]))
			digest_0_ = Hash_fun(str(H1_0_) + str(H2_0_) + str(H3_0_))
			task_0_ = digest_0_ % output_space
			H1_1_ = Hash_fun(str(modified_operation) + str(modified_random_number) + str(digest_0_))
			H2_1_ = Hash_fun(str(modified_random_number) + str(modified_payloads[1]))
			H3_1_ = Hash_fun(str(modified_random_number) + str(modified_payloads[0]))
			digest_1_ = Hash_fun(str(H1_1_) + str(H2_1_) + str(H3_1_))
			task_1_ = digest_1_ % output_space
			try_times+=1
			if (try_times + 1) % 10000 == 0:
				print(try_times)
			if try_times >= 2 ** 20:
				break
		if task_0 != task_0_ or task_1_ != task_1:
			print("Fail after trying", try_times)
		else:
			print("Success", try_times)

# \H2 \H3
if args_parser.test_type == "1":
	for _ in tqdm(range(epoch)):
		[operation, modified_operation] = np.random.choice(operation_total, 2)
		payloads = [random.randint(0, payloads_space), random.randint(0, payloads_space)]
		random_number = random.randint(0, random_number_space)
		
		H1_0 = Hash_fun(str(operation) + str(random_number) + str(digest))
		digest_0 = Hash_fun(str(H1_0))
		task_0 = digest_0 % output_space
		H1_1 = Hash_fun(str(operation) + str(random_number) + str(digest_0))
		digest_1 = Hash_fun(str(H1_1))
		task_1 = digest_1 % output_space

		modified_random_number = random.randint(0, random_number_space)
		modified_payloads = [random.randint(0, payloads_space), random.randint(0, payloads_space)]
		H1_0_ = Hash_fun(str(modified_operation) + str(modified_random_number) + str(digest))
		digest_0_ = Hash_fun(str(H1_0_))
		task_0_ = digest_0_ % output_space
		H1_1_ = Hash_fun(str(modified_operation) + str(modified_random_number) + str(digest_0_))
		digest_1_ = Hash_fun(str(H1_1_))
		task_1_ = digest_1_ % output_space
		try_times = 0

		while task_0 != task_0_ or task_1_ != task_1:
			if task_0 != task_0_:
				modified_random_number = random.randint(0, random_number_space)
				modified_payloads[0] = random.randint(0, payloads_space)
			if task_1 != task_1_:
				modified_random_number = random.randint(0, random_number_space)
				modified_payloads[1] = random.randint(0, payloads_space)
			H1_0_ = Hash_fun(str(modified_operation) + str(modified_random_number) + str(digest))
			digest_0_ = Hash_fun(str(H1_0_))
			task_0_ = digest_0_ % output_space
			H1_1_ = Hash_fun(str(modified_operation) + str(modified_random_number) + str(digest_0_))
			digest_1_ = Hash_fun(str(H1_1_))
			task_1_ = digest_1_ % output_space
			try_times+=1
			if (try_times + 1) % 10000 == 0:
				print(try_times)
			if try_times >= 2 ** 20:
				break
		if task_0 != task_0_ or task_1_ != task_1:
			print("Fail after trying", try_times)
		else:
			print("Success", try_times)

# \H1 \H2
if args_parser.test_type == "3":
	for _ in tqdm(range(epoch)):
		[operation, modified_operation] = np.random.choice(operation_total, 2)
		payloads = [random.randint(0, payloads_space), random.randint(0, payloads_space)]
		random_number = random.randint(0, random_number_space)
		
		H3_0 = Hash_fun(str(random_number) + str(payloads[-1]))
		digest_0 = Hash_fun(str(H3_0))
		task_0 = digest_0 % output_space

		H3_1 = Hash_fun(str(random_number) + str(payloads[0]))
		digest_1 = Hash_fun(str(H3_1))
		task_1 = digest_1 % output_space

		modified_random_number = random.randint(0, random_number_space)
		modified_payloads = [random.randint(0, payloads_space), random.randint(0, payloads_space)]
		H3_0_ = Hash_fun(str(modified_random_number) + str(modified_payloads[-1]))
		digest_0_ = Hash_fun(str(H3_0_))
		task_0_ = digest_0_ % output_space
		H3_1_ = Hash_fun(str(modified_random_number) + str(modified_payloads[0]))
		digest_1_ = Hash_fun(str(H3_1_))
		task_1_ = digest_1_ % output_space
		try_times = 0

		while task_0 != task_0_ or task_1_ != task_1:
			if task_0 != task_0_:
				# modified_random_number = random.randint(0, random_number_space)
				modified_payloads[1] = random.randint(0, payloads_space)
			if task_1 != task_1_:
				# modified_random_number = random.randint(0, random_number_space)
				modified_payloads[0] = random.randint(0, payloads_space)
			H3_0_ = Hash_fun(str(modified_random_number) + str(modified_payloads[-1]))
			digest_0_ = Hash_fun(str(H3_0_))
			task_0_ = digest_0_ % output_space
			H3_1_ = Hash_fun(str(modified_random_number) + str(modified_payloads[0]))
			digest_1_ = Hash_fun(str(H3_1_))
			task_1_ = digest_1_ % output_space
			try_times+=1
			if (try_times + 1) % 10000 == 0:
				print(try_times)
			if try_times >= 2 ** 20:
				break
		if task_0 != task_0_ or task_1_ != task_1:
			print("Fail after trying", try_times)
		else:
			print("Success", try_times)

# \H3
if args_parser.test_type == "12":
	for _ in tqdm(range(epoch)):
		[operation, modified_operation] = np.random.choice(operation_total, 2)
		payloads = [random.randint(0, payloads_space), random.randint(0, payloads_space)]
		random_number = random.randint(0, random_number_space)
		
		H1_0 = Hash_fun(str(operation) + str(random_number) + str(digest))
		H2_0 = Hash_fun(str(random_number) + str(payloads[0]))
		digest_0 = Hash_fun(str(H1_0) + str(H2_0))
		task_0 = digest_0 % output_space
		H1_1 = Hash_fun(str(operation) + str(random_number) + str(digest_0))
		H2_1 = Hash_fun(str(random_number) + str(payloads[1]))
		digest_1 = Hash_fun(str(H1_1) + str(H2_1))
		task_1 = digest_1 % output_space

		modified_random_number = random.randint(0, random_number_space)
		modified_payloads = [random.randint(0, payloads_space), random.randint(0, payloads_space)]
		H1_0_ = Hash_fun(str(modified_operation) + str(modified_random_number) + str(digest))
		H2_0_ = Hash_fun(str(modified_random_number) + str(modified_payloads[0]))
		digest_0_ = Hash_fun(str(H1_0_) + str(H2_0_))
		task_0_ = digest_0_ % output_space
		H1_1_ = Hash_fun(str(modified_operation) + str(modified_random_number) + str(digest_0_))
		H2_1_ = Hash_fun(str(modified_random_number) + str(modified_payloads[1]))
		digest_1_ = Hash_fun(str(H1_1_) + str(H2_1_))
		task_1_ = digest_1_ % output_space
		try_times = 0

		while task_0 != task_0_ or task_1_ != task_1:
			if task_0 != task_0_:
				# modified_random_number = random.randint(0, random_number_space)
				modified_payloads[0] = random.randint(0, payloads_space)
			if task_1 != task_1_:
				# modified_random_number = random.randint(0, random_number_space)
				modified_payloads[1] = random.randint(0, payloads_space)
			H1_0_ = Hash_fun(str(modified_operation) + str(modified_random_number) + str(digest))
			H2_0_ = Hash_fun(str(modified_random_number) + str(modified_payloads[0]))
			digest_0_ = Hash_fun(str(H1_0_) + str(H2_0_))
			task_0_ = digest_0_ % output_space
			H1_1_ = Hash_fun(str(modified_operation) + str(modified_random_number) + str(digest_0_))
			H2_1_ = Hash_fun(str(modified_random_number) + str(modified_payloads[1]))
			digest_1_ = Hash_fun(str(H1_1_) + str(H2_1_))
			task_1_ = digest_1_ % output_space
			try_times+=1
			if (try_times + 1) % 10000 == 0:
				print(try_times)
			if try_times >= 2 ** 20:
				break
		if task_0 != task_0_ or task_1_ != task_1:
			print("Fail after trying", try_times)
		else:
			print("Success", try_times)
