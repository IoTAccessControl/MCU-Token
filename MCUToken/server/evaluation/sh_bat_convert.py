import os

convert_files = []
shell_type = ""
for file_name in os.listdir("./"):
  if "0_generate_ref_log" not in file_name and (".bat" in file_name or ".sh" in file_name):
    convert_files.append(file_name)
    shell_type = file_name.split(".")[-1]

for file_name in convert_files:
  f = open(file_name, "r").read()
  f = f.replace("\n\n", "\n")
  open(file_name, "w").write(f)
  if ".bat" in file_name:
    os.rename(file_name, file_name.replace(".bat", ".sh"))
  elif ".sh" in file_name:
    os.rename(file_name, file_name.replace(".sh", ".bat"))

# the special shell
if shell_type == "bat":
  f = open("0_generate_ref_log.bat", "r").read()
  f = f.replace("call", "sh")
  f = f.replace(".bat", ".sh")
  f = f.replace("\n\n", "\n")
  open("0_generate_ref_log.sh", "w").write(f)
  os.remove("0_generate_ref_log.bat")
elif shell_type == "sh":
  f = open("0_generate_ref_log.sh").read()
  f = f.replace("sh", "call")
  f = f.replace(".call", ".bat")
  f = f.replace("\n\n", "\n")
  open("0_generate_ref_log.bat", "w").write(f)
  os.remove("0_generate_ref_log.sh")
