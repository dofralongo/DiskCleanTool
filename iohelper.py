import os.path
import shutil
import sys

import psutil

import logutil


def get_disk_free(filepath):
    shutil.disk_usage(filepath)

# 获取硬盘所有的盘符
def get_all_disk_partitions():
    """
    获取硬盘所有的盘符
    :return:
    """
    psutil.disk_partitions()

class iostream:
    def __init__(self):
        pass

    def is_directory_empty(self,path):
        """
        判断文件夹是否为空
        :param path:
        :return:
        """
        if os.path.isdir(path):
            return len(os.listdir(path))
        else:
            return 0

    def copy_without_metadata(self,source,destination):
        """
        复制文件，但是不复制相关元数据，如权限，创建日期
        :param source:源路径
        :param destination:目的路径
        :return:
        """
        dir = os.path.dirname(destination)
        if not os.path.isdir(dir):
            os.makedirs(dir)

        if os.path.isfile(source):
            shutil.copyfile(source,destination)

    def copy_with_metadata(self,source,destination):
        """
        复制文件，并且复制相关元数据，如权限，创建日期
        :param source: 源路径
        :param destination: 目的路径
        :return:
        """
        dir = os.path.dirname(destination)
        if not os.path.isdir(dir):
            os.makedirs(dir)

        if os.path.isfile(source):
            shutil.copy2(source, destination)

    def move(self,source,destination):
        """
        移动文件，如果目的路径中存在同名的文件，即进行覆盖
        :param source: 源路径
        :param destination: 目的路径
        :return:
        """
        dir = os.path.dirname(destination)
        if not os.path.isdir(dir):
            os.makedirs(dir)

        shutil.move(source,destination)

    def remove_folder(self,folder):
        """
        删除整个文件夹及其下面的文件和子文件夹
        :param folder: 文件夹路径
        :return:
        """
        if os.path.isdir(folder):
            shutil.rmtree(folder)

    def remove_file(self,file):
        """
        删除文件
        :param file: 文件路径
        :return:
        """
        if os.path.isfile(file):
            os.remove(file)



def disk_usage():
    partitions = psutil.disk_partitions()

    for partition in partitions:
        print(f"Disk:{partition.device}")
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"Total：{usage.total}")
            print(f"Used：{usage.used}")
            print(f"Free：{usage.free}")
            print(f"Percent：{usage.percent}")
        except PermissionError:
            print("Permission denied")

def resource_path(relative_path):
        python_root = os.path.dirname(os.path.realpath(sys.executable))
        return python_root + relative_path

if __name__ == '__main__':
    # io = iostream()
    # src=r"D:\code\git\1\11\111.xml"
    # dest = r"D:\code\git\2\22\222.xml"
    # io.copy_with_metadata(src,dest)
    # io.move(src,dest)
    # io.remove_folder(os.path.dirname(dest))
    # print(io.is_directory_empty(r"D:\VisionPK\vpk_data\11"))
    # disk_usage()
    dll_path = resource_path(r"dll\Everything64.dll")
    print(dll_path)

