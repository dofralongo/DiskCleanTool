import os
import sys
import time
import psutil

import logutil

# 获取指定名称的所有进程
def get_all_process_by_name(name):
    proc_list = []
    for pid in psutil.pids():
        try:
            proc = psutil.Process(pid)
            if proc.name() == name:
                proc_list.append(proc)
        except Exception as ex:
            logutil.logger.error(ex)

    return proc_list


# 通过进程ID获取进程的名称
def get_processname_by_id(pid):
    process = psutil.Process(pid)
    if process is None:
         return ""
    else:
        return process.name()

# 通过进程名称获取进程
def get_process_by_name(name):
    """
    通过进程名称获取进程
    :param name: 进程名称
    :return:
    """
    for process in psutil.process_iter(["name"]):
        if process.info["name"] == name:
            return process

    return None


# 判断进程是否已经运行
def check_process_running(name):
    """
    根据进程名称判断是否已经在运行中
    :param name: 进程名称
    :return:
    """
    process = get_process_by_name(name)
    if process is None:
        return False
    else:
        return True



# 根据进程名杀死进程
def kill_process_by_name(name):
    """
    根据进程名杀死进程
    :param name: 进程名
    :return:
    """
    pro = 'taskkill /f /im %s' % name
    os.system(pro)


# 根据pid杀死进程
def kill_procee_by_id(pid):
    """
    根据pid杀死进程
    :param pid: 进程ID
    :return:
    """
    process = 'taskkill /f /pid %s' % pid
    os.system(process)

# 监控指定进程CPU、内存、IO使用率
def monitor_resource(process_name,interval=0.1):
    """
    监控指定进程CPU、内存、IO使用率
    :param process_name: 进程名称
    :param interval: 间隔时间，单位秒，至少要大于0.1秒
    :return:
    """
    process = get_process_by_name(process_name)
    if process is not None:
        while True:
            # 监控指定进程CPU使用率
            cpu_percent = round(process.cpu_percent(interval), 2)
            logutil.logger.trace(f"cpu percent is {cpu_percent}%")

            # 监控指定进程内存使用情况
            memory_info = process.memory_info_ex()
            memory_percent = process.memory_percent()
            logutil.logger.trace(
                f"memory usage is {memory_info.rss/ (1024 * 1024):.2f} MB , memory percent is {memory_percent:.2f}%")

            # 监控指定进程IO使用情况
            io_counters = process.io_counters()
            logutil.logger.trace(
                f"io read_bytes is {io_counters.read_bytes / (1024 * 1024):.2f} MB , write_bytes is {io_counters.write_bytes / (1024 * 1024):.2f} MB")

            time.sleep(interval)

def get_self_processes():
    """获取当前程序的所有进程（根据路径匹配）"""
    self_path = sys.executable  # 当前程序路径（如打包后的 diskmgr.exe 路径）
    proc_list = []
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            # 匹配进程名和路径
            if proc.info['name'] == os.path.basename(self_path) and proc.info['exe'] == self_path:
                proc_list.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return proc_list

if __name__ == '__main__':
    pass
