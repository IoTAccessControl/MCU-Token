#-*-coding:utf-8-*-

import os
import sys
import glob
import yaml
from lxml import etree

"""
tutorial:
https://yeonghoey.com/lxml/element/
"""

def parse_yaml_conf(conf, dir_prefix):
	codes = {}
	with open(conf, "r") as stream:
		try:
			groups = yaml.safe_load(stream)
			for gp, fis in groups.items():
				codes[gp] = []
				if not fis:
					continue
				for fi in fis:
					if "*" in fi:
						#fi = os.path.join(os.path.abspath(dir_prefix), fi)
						all_fi = glob.glob(fi)
						#print("Glob=================", all_fi, fi)
						for m in all_fi:
							code = os.path.join(dir_prefix, m)
							code = code.replace("/", "\\")
							codes[gp].append(code)
					else:
						code = os.path.join(dir_prefix, fi)
						code = code.replace("/", "\\")
						codes[gp].append(code)
		except yaml.YAMLError as exc:
			print(exc)
	#print("all files", codes)
	return codes

def update_uv_proj_code_list(uvoptx, uvprojx, codes, use_optx=True):
	from copy import deepcopy
	print("find uv proj conf:", uvoptx, uvprojx)

	def get_code_file_type(code):
		if code.endswith(".h"):
			return 5
		elif code.endswith(".c"):
			return 1
		return 1
	
	def add_optx_groups(tree, gps):
		gp_num, fi_num = 0, 0
		for fi in tree.xpath(".//Group/File"):
			gn = int(fi.xpath("GroupNumber/text()")[0])
			gp_num = max(gp_num, gn)
			fn = int(fi.xpath("FileNumber/text()")[0])
			fi_num = max(fi_num, fn)
		# copy a node as template
		# print(fi_num, gp_num)
		empty_node = tree.xpath(".//Group")[0]
		empty_node = deepcopy(empty_node)

		file_nodes = empty_node.xpath("File")
		fnode = deepcopy(file_nodes[0])

		for fi in file_nodes:
			empty_node.remove(fi)

		# print(etree.tostring(empty_node))
		# print(empty_node, file_nodes[0], fnode)
		for gp in gps:
			gp_num += 1
			fis = gps[gp]
			cur_group = deepcopy(empty_node)
			cur_group.xpath("GroupName")[0].text = gp
			for fi in fis:
				fi_num += 1
				cur_file = deepcopy(fnode)
				cur_file.xpath("GroupNumber")[0].text = str(gp_num)
				cur_file.xpath("FileNumber")[0].text = str(fi_num)
				cur_file.xpath("FileType")[0].text = str(get_code_file_type(os.path.basename(fi)))
				cur_file.xpath("PathWithFileName")[0].text = fi
				cur_file.xpath("FilenameWithoutPath")[0].text = os.path.basename(fi)
				cur_group.append(cur_file)
			# print(etree.tostring(cur_group))
			tree.append(cur_group)
	
	def add_proj_groups(tree, gps):
		# copy a node as template
		# print(fi_num, gp_num)
		proj_groups = tree.xpath("//Groups")[0]
		empty_node = proj_groups.xpath("Group")[0]
		empty_node = deepcopy(empty_node)

		files_node = empty_node.xpath("Files")[0]

		file_nodes = files_node.xpath("File")
		fnode = deepcopy(file_nodes[0])

		for fi in file_nodes:
			files_node.remove(fi)

		# print(etree.tostring(empty_node))
		# print(empty_node, file_nodes[0], fnode)
		for gp in gps:
			fis = gps[gp]
			cur_group = deepcopy(empty_node)
			cur_group.xpath("GroupName")[0].text = gp
			cur_files = cur_group.xpath("Files")[0]
			for fi in fis:
				cur_file = deepcopy(fnode)
				cur_file.xpath("FileName")[0].text = os.path.basename(fi)
				cur_file.xpath("FileType")[0].text = str(get_code_file_type(os.path.basename(fi)))
				cur_file.xpath("FilePath")[0].text = fi
				cur_files.append(cur_file)	
			# print(etree.tostring(cur_group))
			proj_groups.append(cur_group)

	def save_xml(tree, pt):
		print("Save to ", pt)
		et = etree.ElementTree(tree)
		et.write(pt, xml_declaration=True, encoding='UTF-8', standalone=False, pretty_print=True)
	
	"""
	1. remove exisiting groups and files in.uvprojx
	2. re-add these xml nodes from yaml conf 
	"""
	if use_optx:
		tree_optx = etree.parse(uvoptx).getroot()
	tree_proj = etree.parse(uvprojx).getroot()
	proj_groups = tree_proj.xpath("//Groups")[0]
	for gp in codes:
		if gp != "INCLUDE" and gp != "DEFINE":
			if use_optx:
				xml_gp = tree_optx.xpath(".//Group/GroupName[text()='{}']".format(gp))
				if xml_gp:
					print("Remove existing group:", gp, uvoptx)
					tree_optx.remove(xml_gp[0].getparent())
			xml_gp = proj_groups.xpath(".//Group/GroupName[text()='{}']".format(gp))
			if xml_gp:
				print("Remove existing group:", gp, uvprojx)
				proj_groups.remove(xml_gp[0].getparent())

	# set include path, first need to remove all new added headers
	my_sep = "MY_SEP"
	inc_sep = ";"
	if "INCLUDE" in codes.keys():
		include_path = tree_proj.xpath("//Cads/VariousControls/IncludePath")[0].text
		#print("before", include_path)
		ipaths = codes["INCLUDE"]
		sep = inc_sep + my_sep
		include_path = include_path.split(sep)[0] # two parts: origin + my_sep + new_add
		origin_items = include_path.split(inc_sep) 
		origin_items.append(my_sep)
		
		for ipath in ipaths:
			if ipath not in origin_items:
				origin_items.append(ipath)
				#include_path += ";" + ipath
		include_path = inc_sep.join(origin_items)
		#print("after", include_path)
		tree_proj.xpath("//Cads/VariousControls/IncludePath")[0].text = include_path
		del codes["INCLUDE"]

	# set define/macro
	# first need to remove all new added items 
	define_sep = "CUSTOM_DEFINE"
	if "DEFINE" in codes.keys():
		orig_defines = tree_proj.xpath("//Cads/VariousControls/Define")[0].text
		defines = codes["DEFINE"]
		if orig_defines == None:
			orig_defines = define_sep
		orig_defines = orig_defines.split(define_sep)[0]
		orig_defines += define_sep
		for define in defines:
			define = os.path.basename(define)
			# if define not in orig_defines:
			orig_defines = orig_defines + " " + define
		tree_proj.xpath("//Cads/VariousControls/Define")[0].text = orig_defines
		del codes["DEFINE"]

	# update optx
	if use_optx:
		add_optx_groups(tree_optx, codes)
		save_xml(tree_optx, uvoptx)
	
	# update projx
	add_proj_groups(tree_proj, codes)
	save_xml(tree_proj, uvprojx)

def write_uv_proj_conf(uv_dir, codes):
	print("search uv proj conf")
	uvoptx = glob.glob(uv_dir + "/*.uvoptx")
	uvprojx = glob.glob(uv_dir + "/*.uvprojx")
	if uvoptx:
		for i in range(len(uvoptx)):
			update_uv_proj_code_list(uvoptx[i], uvprojx[i], codes)
	elif len(uvprojx) > 0:
		update_uv_proj_code_list(uvprojx[0], uvprojx[0], codes, False)
	else:
		print(f"No uvprojx file find in {uv_dir}.")

def main(uv_proj, file_list):
	uv_dir = os.path.abspath(uv_proj)
	flst_path = os.path.abspath(file_list)
	work_dir = os.path.dirname(flst_path)
	print("UV Project Dir", uv_dir)
	print("File list: ", flst_path)
	rel_path = os.path.relpath(work_dir, uv_dir)
	codes = parse_yaml_conf(flst_path, rel_path)
	write_uv_proj_conf(uv_dir, codes)

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Need More Args: uv_proj_dir, file_list")
		print("python update_keil_proj.py ..\\nrf52840\\without-os\\project\\mdk5\\ files.yaml")
		sys.exit(-1)
	# print(sys.argv)
	uv_proj, file_list = sys.argv[1], sys.argv[2]
	main(uv_proj, file_list)
