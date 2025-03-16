import datetime
import shutil
import sys
import time
import struct
import ctypes
import math
import os

# 定义变量
import pandas as pd

import logutil
from iohelper import resource_path

# 排序状态映射
EVERYTHING_SORT_NAME_ASCENDING = 1
EVERYTHING_SORT_NAME_DESCENDING = 2
EVERYTHING_SORT_PATH_ASCENDING = 3
EVERYTHING_SORT_PATH_DESCENDING = 4
EVERYTHING_SORT_SIZE_ASCENDING = 5
EVERYTHING_SORT_SIZE_DESCENDING = 6
EVERYTHING_SORT_EXTENSION_ASCENDING = 7
EVERYTHING_SORT_EXTENSION_DESCENDING = 8
EVERYTHING_SORT_TYPE_NAME_ASCENDING = 9
EVERYTHING_SORT_TYPE_NAME_DESCENDING = 10
EVERYTHING_SORT_DATE_CREATED_ASCENDING = 11
EVERYTHING_SORT_DATE_CREATED_DESCENDING = 12
EVERYTHING_SORT_DATE_MODIFIED_ASCENDING = 13
EVERYTHING_SORT_DATE_MODIFIED_DESCENDING = 14
EVERYTHING_SORT_ATTRIBUTES_ASCENDING = 15
EVERYTHING_SORT_ATTRIBUTES_DESCENDING = 16
EVERYTHING_SORT_FILE_LIST_FILENAME_ASCENDING = 17
EVERYTHING_SORT_FILE_LIST_FILENAME_DESCENDING = 18
EVERYTHING_SORT_RUN_COUNT_ASCENDING = 19
EVERYTHING_SORT_RUN_COUNT_DESCENDING = 20
EVERYTHING_SORT_DATE_RECENTLY_CHANGED_ASCENDING = 21
EVERYTHING_SORT_DATE_RECENTLY_CHANGED_DESCENDING = 22
EVERYTHING_SORT_DATE_ACCESSED_ASCENDING = 23
EVERYTHING_SORT_DATE_ACCESSED_DESCENDING = 24
EVERYTHING_SORT_DATE_RUN_ASCENDING = 25
EVERYTHING_SORT_DATE_RUN_DESCENDING = 26


EVERYTHING_REQUEST_FILE_NAME = 0x00000001
EVERYTHING_REQUEST_PATH = 0x00000002
EVERYTHING_REQUEST_FULL_PATH_AND_FILE_NAME = 0x00000004
EVERYTHING_REQUEST_EXTENSION = 0x00000008
EVERYTHING_REQUEST_SIZE = 0x00000010
EVERYTHING_REQUEST_DATE_CREATED = 0x00000020
EVERYTHING_REQUEST_DATE_MODIFIED = 0x00000040
EVERYTHING_REQUEST_DATE_ACCESSED = 0x00000080
EVERYTHING_REQUEST_ATTRIBUTES = 0x00000100
EVERYTHING_REQUEST_FILE_LIST_FILE_NAME = 0x00000200
EVERYTHING_REQUEST_RUN_COUNT = 0x00000400
EVERYTHING_REQUEST_DATE_RUN = 0x00000800
EVERYTHING_REQUEST_DATE_RECENTLY_CHANGED = 0x00001000
EVERYTHING_REQUEST_HIGHLIGHTED_FILE_NAME = 0x00002000
EVERYTHING_REQUEST_HIGHLIGHTED_PATH = 0x00004000
EVERYTHING_REQUEST_HIGHLIGHTED_FULL_PATH_AND_FILE_NAME = 0x00008000

# convert a windows FILETIME to a python datetime
# https://stackoverflow.com/questions/39481221/convert-datetime-back-to-windows-64-bit-filetime
WINDOWS_TICKS = int(1 / 10 ** -7)  # 10,000,000 (100 nanoseconds or .1 microseconds)
WINDOWS_EPOCH = datetime.datetime.strptime('1601-01-01 00:00:00',
                                           '%Y-%m-%d %H:%M:%S')
POSIX_EPOCH = datetime.datetime.strptime('1970-01-01 00:00:00',
                                         '%Y-%m-%d %H:%M:%S')
EPOCH_DIFF = (POSIX_EPOCH - WINDOWS_EPOCH).total_seconds()  # 11644473600.0
WINDOWS_TICKS_TO_POSIX_EPOCH = EPOCH_DIFF * WINDOWS_TICKS  # 116444736000000000.0


def handle_error(func, path, exc_info):
    logutil.logger.error(f"Error: {path} - {exc_info}")


def get_time(filetime):
    """Convert windows filetime winticks to python datetime.datetime."""
    winticks = struct.unpack('<Q', filetime)[0]
    microsecs = (winticks - WINDOWS_TICKS_TO_POSIX_EPOCH) / WINDOWS_TICKS
    # return microsecs
    # return datetime.datetime.fromtimestamp(microsecs)
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(microsecs))


class EveryTools:
    def __init__(self, machine=64):
        self.machine = machine


        # logutil.logger.info(f" es file is {os.path.dirname(os.path.realpath(sys.executable))}")
        # dll导入
        if self.machine == 64:
            dll_path = resource_path(r'\dll\Everything64.dll')
        elif self.machine == 32:
            dll_path = resource_path(r'\dll\Everything32.dll')
        else:
            dll_path = None

        # print(dll_path)
        logutil.logger.info(dll_path)
        self.everything_dll = ctypes.WinDLL(dll_path)

        # 定义数据类型
        self.everything_dll.Everything_GetResultDateCreated.argtypes = [ctypes.c_int,
                                                                        ctypes.POINTER(ctypes.c_ulonglong)]
        self.everything_dll.Everything_GetResultDateModified.argtypes = [ctypes.c_int,
                                                                         ctypes.POINTER(ctypes.c_ulonglong)]
        self.everything_dll.Everything_GetResultSize.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_ulonglong)]
        self.everything_dll.Everything_GetResultFileNameW.argtypes = [ctypes.c_int]
        self.everything_dll.Everything_GetResultFileNameW.restype = ctypes.c_wchar_p
        self.everything_dll.Everything_GetResultPathW.restype = ctypes.c_wchar_p
        self.everything_dll.Everything_GetResultExtensionW.restype = ctypes.c_wchar_p

        # 版本信息
        self.major_version = self.everything_dll.Everything_GetMajorVersion()
        self.minor_version = self.everything_dll.Everything_GetMinorVersion()
        self.revision = self.everything_dll.Everything_GetRevision()
        self.build_number = self.everything_dll.Everything_GetBuildNumber()
        self.version = f'{self.major_version}.{self.minor_version}.{self.revision}.{self.build_number}'

        # 搜索结果信息
        self.num_total_results = 0
        self.num_total_file = 0
        self.num_total_folder = 0

    def search(self, keywords, math_path=False, math_case=False, whole_world=False, regex=False):
        """ 基本搜索

        :param keywords: 关键词
        :param math_path: 匹配路径
        :param math_case: 区分大小写
        :param whole_world: 全字匹配
        :param regex: 使用正则
        :return:
        """

        # self.everything_dll.Everything_CleanUp()
        self.everything_dll.Everything_Reset()  # 重置状态
        self.everything_dll.Everything_SetSearchW(keywords)
        self.everything_dll.Everything_SetMatchPath(math_path)  # 匹配路径
        self.everything_dll.Everything_SetMatchCase(math_case)  # 区分大小写
        self.everything_dll.Everything_SetMatchWholeWord(whole_world)  # 全字匹配
        self.everything_dll.Everything_SetRegex(regex)  # 使用正则表达式


        # self.everything_dll.Everything_SetReplyWindow(0)
        # self.everything_dll.Everything_SetReplyID(0)
        # 执行查询
        self.everything_dll.Everything_QueryW(True)

        # 获取搜索结果
        self.num_total_results = self.everything_dll.Everything_GetNumResults()
        self.num_total_file = self.everything_dll.Everything_GetTotFileResults()
        self.num_total_folder = self.everything_dll.Everything_GetTotFolderResults()

    def get_search_keyword(self):
        """ 获取搜索关键词

        :return: string
        """
        self.everything_dll.Everything_GetSearchW.restype = ctypes.c_wchar_p
        return self.everything_dll.Everything_GetSearchW()

    def get_num_total_results(self):
        """ 获取全部结果数量

        :return:
        """
        return self.num_total_results

    def get_num_total_file(self):
        """ 获取全部'文件'结果数量

        :return:
        """
        return self.num_total_file

    def get_num_total_folder(self):
        """ 获取全部'文件夹'结果数量

        :return:
        """
        return self.num_total_folder

    def search_audio(self, keywords=''):
        """  搜索音频文件

        :param keywords: 关键词
        :return:
        """
        self.search(f'ext:aac;ac3;aif;aifc;aiff;au;cda;dts;fla;flac;it;m1a;m2a;m3u;m4a;mid;midi;mka;mod;mp2;mp3;mpa;'
                    f'ogg;ra;rmi;spc;rmi;snd;umx;voc;wav;wma;xm {keywords}')

    def search_zip(self, keywords=''):
        """ 搜索压缩文件

        :param keywords: 关键词
        :return:
        """
        self.search(f'ext:7z;ace;arj;bz2;cab;gz;gzip;jar;r00;r01;r02;r03;r04;r05;r06;r07;r08;r09;r10;r11;r12;r13;r14;'
                    f'r15;r16;r17;r18;r19;r20;r21;r22;r23;r24;r25;r26;r27;r28;r29;rar;tar;tgz;z;zip {keywords}')

    def search_doc(self, keywords=''):
        """ 搜索文档

        :param keywords: 关键词
        :return:
        """
        self.search(f'ext:c;chm;cpp;csv;cxx;doc;docm;docx;dot;dotm;dotx;h;hpp;htm;html;hxx;ini;java;lua;mht;mhtml;'
                    f'odt;pdf;potx;potm;ppam;ppsm;ppsx;pps;ppt;pptm;pptx;rtf;sldm;sldx;thmx;txt;vsd;wpd;wps;wri;'
                    f'xlam;xls;xlsb;xlsm;xlsx;xltm;xltx;xml {keywords}')

    def search_exe(self, keywords=''):
        """ 搜索可执行文件

        :param keywords: 关键词
        :return:
        """
        self.search(f'ext:bat;cmd;exe;msi;msp;scr {keywords}')

    def search_folder(self, keywords=''):
        """ 搜索文件夹

        :param keywords: 关键词
        :return:
        """
        self.search(f'folder: {keywords}')

    def search_pic(self, keywords=''):
        """ 搜索图片

        :param keywords: 关键词
        :return:
        """
        self.search(f'ext:ani;bmp;gif;ico;jpe;jpeg;jpg;pcx;png;psd;tga;tif;tiff;webp;wmf {keywords}')

    def search_video(self, keywords=''):
        """ 搜索视频

        :param keywords: 关键词
        :return:
        """
        self.search(f'ext:3g2;3gp;3gp2;3gpp;amr;amv;asf;avi;bdmv;bik;d2v;divx;drc;dsa;dsm;dss;dsv;evo;f4v;flc;fli;'
                    f'flic;flv;hdmov;ifo;ivf;m1v;m2p;m2t;m2ts;m2v;m4b;m4p;m4v;mkv;mp2v;mp4;mp4v;mpe;mpeg;mpg;mpls;'
                    f'mpv2;mpv4;mov;mts;ogm;ogv;pss;pva;qt;ram;ratdvd;rm;rmm;rmvb;roq;rpm;smil;smk;swf;tp;tpr;ts;'
                    f'vob;vp6;webm;wm;wmp;wmv {keywords}')

    def search_ext(self, ext, keywords=''):
        """ 搜索扩展名称

        :param ext: 拓展名
        :param keywords: 关键词
        :return:
        """
        self.search(f'ext:{ext} {keywords}')

    def search_in_located(self, path, keywords=''):
        """ 搜索路径下文件

        :param path: 搜索的路径
        :param keywords: 关键词
        :return:
        """
        self.search(f'{path} {keywords}')

    def results(self, max_num=None, sort_type=1, page_size=80):
        """ 输出结果

        :param max_num: 最大数量
        :param sort_type: 排序类型
        :param page_size: 分页大小，数量越大越占用性能，可能出现卡死现象
        :return:
        """
        # 定义块数据
        buffer_full_path_name = ctypes.create_unicode_buffer(260)
        buffer_created_time = ctypes.c_ulonglong(1)
        buffer_modified_time = ctypes.c_ulonglong(1)
        buffer_size = ctypes.c_ulonglong(1)

        # 设置排序
        self.everything_dll.Everything_SetSort(sort_type)

        page_result_list = []

        num_total = self.get_num_total_results()  # 获取全部结果数量
        if max_num and max_num < num_total:
            num_total = max_num
        pages = math.ceil(num_total / page_size)  # 向上取整获取分页数
        page_size = num_total if pages == 1 else page_size

        #  | EVERYTHING_REQUEST_ATTRIBUTES
        # 分页去获取数据
        for page in range(0, pages):
            self.everything_dll.Everything_SetMax(page_size)  # 最大搜索结果
            self.everything_dll.Everything_SetOffset(page * page_size)  # 偏移量
            self.everything_dll.Everything_SetRequestFlags(
                EVERYTHING_REQUEST_FILE_NAME | EVERYTHING_REQUEST_PATH | EVERYTHING_REQUEST_SIZE |
                EVERYTHING_REQUEST_DATE_CREATED | EVERYTHING_REQUEST_DATE_MODIFIED | EVERYTHING_REQUEST_EXTENSION
            )

            self.everything_dll.Everything_QueryW(True)
            num_total_page = self.everything_dll.Everything_GetNumResults()

            for i in range(num_total_page):
                file_name = self.everything_dll.Everything_GetResultFileNameW(i)
                file_path = self.everything_dll.Everything_GetResultPathW(i)
                # self.everything_dll.Everything_GetResultFullPathNameW(i, buffer_full_path_name, 260)

                # 创建时间
                self.everything_dll.Everything_GetResultDateCreated(i, buffer_created_time)
                if struct.unpack('<Q', buffer_created_time)[0] == 18446744073709551615:
                    created_time = None
                else:
                    created_time = get_time(buffer_created_time)

                # 获取查询信息
                self.everything_dll.Everything_GetResultDateModified(i, buffer_modified_time)
                modified_time = get_time(buffer_modified_time)
                self.everything_dll.Everything_GetResultSize(i, buffer_size)  # 大小
                file_size = buffer_size.value
                file_extension = self.everything_dll.Everything_GetResultExtensionW(i)  # 拓展
                # attributes = self.everything_dll.Everything_GetResultAttributes(i)
                is_file = self.everything_dll.Everything_IsFileResult(i)
                is_folder = self.everything_dll.Everything_IsFolderResult(i)
                is_volume = self.everything_dll.Everything_IsVolumeResult(i)
                # ctypes.wstring_at(_full_path_name),
                item = [
                    file_name,
                    file_path,
                    file_size,
                    created_time,
                    modified_time,
                    file_extension,
                    is_file,
                    is_folder,
                    is_volume
                ]

                page_result_list.append(item)

        columns = [
            'name',
            'path',
            'size',
            'created_date',
            'modified_date',
            'file_extension',
            'is_file',
            'is_folder',
            'is_volume'
        ]

        return pd.DataFrame(page_result_list, columns=columns)

    def exit(self):
        """ 执行退出客户端操作，会失去连接

        """
        self.everything_dll.Everything_Exit()

    def delete_folder(self, keywords=''):
        self.search(f'{keywords}')
        num_results = self.num_total_results
        filename = ctypes.create_unicode_buffer(260)
        date_modified_filetime = ctypes.c_ulonglong(1)
        file_size = ctypes.c_ulonglong(1)
        logutil.logger.info(f"num_total_results : {num_results}")

        for i in range(num_results):
            self.everything_dll.Everything_GetResultFullPathNameW(i, filename, 260)
            self.everything_dll.Everything_GetResultDateModified(i, date_modified_filetime)
            self.everything_dll.Everything_GetResultSize(i, file_size)
            # print("i: {}\nFilename: {}\nSize: {} bytes\n".format(i, ctypes.wstring_at(filename), file_size.value))

            dir_path = ctypes.wstring_at(filename)
            mtime = os.path.getmtime(dir_path)
            mdate = datetime.datetime.fromtimestamp(mtime).date()
            is_today = mdate == datetime.datetime.today().date()

            shutil.rmtree(dir_path, ignore_errors=True, onerror=handle_error)

            loop_count=0
            if is_today:
                loop_count=30  # 30秒
            else:
                loop_count=600 # 10分钟

            for i in range(loop_count):
                time.sleep(1)
                if os.path.exists(dir_path):
                    logutil.logger.info(f"{dir_path} deleting...")
                else:
                    logutil.logger.info(f"{dir_path} delete success")
                    break



    def delete_file(self, keywords=''):
        self.search(f'{keywords}')
        num_results = self.num_total_results
        filename = ctypes.create_unicode_buffer(260)
        file_size = ctypes.c_ulonglong(1)
        logutil.logger.info(f"num_total_results : {num_results}")

        # stat_time = time.time()
        for i in range(num_results):
            self.everything_dll.Everything_GetResultFullPathNameW(i, filename, 260)
            self.everything_dll.Everything_GetResultSize(i, file_size)
            # print("i: {}\nFilename: {}\nSize: {} bytes\n".format(i, ctypes.wstring_at(filename), file_size.value))
            del_filename = ctypes.wstring_at(filename)
            try:
                os.remove(del_filename)
                logutil.logger.info(f"{del_filename} delete success")
            except:
                logutil.logger.error(f"{del_filename} delete failed")
        # end_time = time.time()
        # spend_time = end_time - stat_time
        # print(f"spend time:{spend_time} s")


if __name__ == '__main__':
    et = EveryTools()
    # et.search('abcdefs')
    # et.search_ext('pdf', 'sql')
    # et.search_in_located(r"D:\code\python\diskmgr", ".log file:")
    # print('search keywords is:', et.get_search_keyword())
    # print("get_num_total_results:", et.get_num_total_results())
    # df = et.results(max_num=2,sort_type=14)
    # print(df.head())
    # et.delete_folder("vpk_data\ SourceImage\ folder:  len:<40")
    et.search(keywords="vpk_data\ SourceImage\ folder:  len:<40")
    print('search keywords is:', et.get_search_keyword())
    print("get_num_total_results:", et.get_num_total_results())
    df = et.results(max_num=2,sort_type=11)
    print(df.head())
    print(df["created_date"])
