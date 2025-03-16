# encoding: utf-8
# @File  : pyinstall.py
# @Author: Xiaolong.ZHANG
# @Date  : 2025/03/11/09:59


import os
import shutil
import subprocess

# 配置参数
python_root = r"D:\Python\Python312"
script_name = "main.py"
output_name = "diskmgr"
icon_path = r".\icon.ico"
dll_files = [
    os.path.join(python_root, "dll", "Everything64.dll"),
    os.path.join(python_root, "dll", "Everything32.dll")
]
config_file = os.path.join(python_root, "config.ini")

# 构建 PyInstaller 命令
pyinstaller_command = [
    "pyinstaller",
    "--onefile",
    "--uac-admin",
    "-w",
    f"-n {output_name}",
    f"-i {icon_path}"
]

# 添加 DLL 文件
for dll in dll_files:
    pyinstaller_command.append(f"--add-binary \"{dll};dll\"")

# 添加配置文件
pyinstaller_command.append(f"--add-data \"{config_file};.\"")

# 添加主脚本
pyinstaller_command.append(script_name)
# 执行 PyInstaller 命令
pyinstaller_command_str = " ".join(pyinstaller_command)
print(f"执行命令: {pyinstaller_command_str}")
try:
    subprocess.run(pyinstaller_command_str, shell=True, check=True)
    print("打包完成")
except subprocess.CalledProcessError as e:
    print(f"打包失败: {e}")
    exit(1)

# 复制文件到 dist 目录
dist_dir = os.path.join(os.getcwd(), "dist")
if not os.path.exists(dist_dir):
    os.makedirs(dist_dir)

# 复制 DLL 文件
dll_dest_dir = os.path.join(dist_dir, "dll")
if not os.path.exists(dll_dest_dir):
    os.makedirs(dll_dest_dir)
for dll in dll_files:
    shutil.copy2(dll, dll_dest_dir)
    print(f"复制 {dll} 到 {dll_dest_dir}")

# 复制配置文件
shutil.copy2(config_file, dist_dir)
print(f"复制 {config_file} 到 {dist_dir}")

print("文件复制完成")
