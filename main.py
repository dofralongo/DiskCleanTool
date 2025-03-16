import os
import time
from datetime import datetime
import pathlib
from threading import Thread
import psutil
from dateutil.relativedelta import relativedelta
from dateutil import parser as du_parser
import sqlite3
import schedule
import inihelper
import iohelper
import logutil
import everytool
import psutilhelper

# 创建EveryTools对象
es = everytool.EveryTools()

# 创建IO对象
iostream = iohelper.iostream()

path_config_ini = iohelper.resource_path("config.ini")
logutil.logger.info(f"path_config_ini: {path_config_ini}")


def clear_data_file(save_days, clear_filter):
    """
    搜索文件，并删除
    :param save_days:
    :param clear_filter:
    :return:
    """
    logutil.logger.info(f"Entering clear_data_file with save_days={save_days} and clear_filter={clear_filter}")
    try:
        if save_days > 0:
            del_date = datetime.now().date() - relativedelta(days=save_days - 1)
            del_date_filter = f"dc:<{del_date} | dm:<{del_date} "
            del_keywords = f"{clear_filter} {del_date_filter}"
            logutil.logger.info(f"del_keywords : {del_keywords}")
            es.delete_file(del_keywords)
        else:
            logutil.logger.info(f"save days is negative , stop clear")
    except Exception as ex:
        logutil.logger.error(f"Error in clear_data_file: {ex}", exc_info=True)
    logutil.logger.info("Exiting clear_data_file")


def clear_execute_results(keywords):
    """
    清除ExcuteResults(检测数据、汇总数据、区域信息)文件夹中的数据
    :return:
    """
    logutil.logger.info(f"Entering clear_execute_results with keywords={keywords}")
    try:
        logutil.logger.info("begin clear ExcuteResults")
        start_time = time.time()

        logutil.logger.info(f"delete keywords : {keywords}")
        es.delete_folder(keywords)

        end_time = time.time()
        spend_time = round(end_time - start_time, 3)
        logutil.logger.info(f"end clear ExcuteResults , spend time is {spend_time}s")
    except Exception as ex:
        logutil.logger.error(f"Error in clear_execute_results: {ex}", exc_info=True)
    logutil.logger.info("Exiting clear_execute_results")


def clear_feature_image(keywords):
    """
    清除FeatureImage（特征图）文件夹中的数据
    :return:
    """
    logutil.logger.info(f"Entering clear_feature_image with keywords={keywords}")
    try:
        logutil.logger.info("begin clear FeatureImage")
        start_time = time.time()

        logutil.logger.info(f"delete keywords : {keywords}")
        es.delete_folder(keywords)

        end_time = time.time()
        spend_time = round(end_time - start_time, 3)
        logutil.logger.info(f"end clear FeatureImage , spend time is {spend_time}s")
    except Exception as ex:
        logutil.logger.error(f"Error in clear_feature_image: {ex}", exc_info=True)
    logutil.logger.info("Exiting clear_feature_image")


def clear_handle_image(keywords):
    """
    清除HandleImage（处理图）文件夹中的数据
    :return:
    """
    logutil.logger.info(f"Entering clear_handle_image with keywords={keywords}")
    try:
        logutil.logger.info("begin clear HandleImage")
        start_time = time.time()

        logutil.logger.info(f"delete keywords : {keywords}")
        es.delete_folder(keywords)

        end_time = time.time()
        spend_time = round(end_time - start_time, 3)
        logutil.logger.info(f"end clear HandleImage , spend time is {spend_time}s")
    except Exception as ex:
        logutil.logger.error(f"Error in clear_handle_image: {ex}", exc_info=True)
    logutil.logger.info("Exiting clear_handle_image")


def clear_source_image(keywords):
    """
    清除SourceImage(原图)文件夹中的数据
    :return:
    """
    logutil.logger.info(f"Entering clear_source_image with keywords={keywords}")
    try:
        logutil.logger.info("begin clear SourceImage")
        start_time = time.time()

        logutil.logger.info(f"delete keywords : {keywords}")
        es.delete_folder(keywords)

        end_time = time.time()
        spend_time = round(end_time - start_time, 3)
        logutil.logger.info(f"end clear SourceImage , spend time is {spend_time}s")
    except Exception as ex:
        logutil.logger.error(f"Error in clear_source_image: {ex}", exc_info=True)
    logutil.logger.info("Exiting clear_source_image")


def clear_exe_result(keywords):
    """
    清除"执行结果"文件夹中的数据
    :return:
    """
    logutil.logger.info(f"Entering clear_exe_result with keywords={keywords}")
    try:
        logutil.logger.info("begin clear exe")
        start_time = time.time()

        logutil.logger.info(f"delete keywords : {keywords}")
        es.delete_folder(keywords)

        end_time = time.time()
        spend_time = round(end_time - start_time, 3)
        logutil.logger.info(f"end clear exe , spend time is {spend_time}s")
    except Exception as ex:
        logutil.logger.error(f"Error in clear_exe_result: {ex}", exc_info=True)
    logutil.logger.info("Exiting clear_exe_result")


def clear_empty_folder(keywords):
    """
    清除空文件夹
    :return:
    """
    logutil.logger.info(f"Entering clear_empty_folder with keywords={keywords}")
    try:
        logutil.logger.info("begin clear empty folder")
        start_time = time.time()

        logutil.logger.info(f"delete keywords : {keywords}")
        es.delete_folder(keywords)

        end_time = time.time()
        spend_time = round(end_time - start_time, 3)
        logutil.logger.info(f"end clear empty folder , spend time is {spend_time}s")
    except Exception as ex:
        logutil.logger.error(f"Error in clear_empty_folder: {ex}", exc_info=True)
    logutil.logger.info("Exiting clear_empty_folder")


def clear_aoi_log():
    """
    清除AOI日志文件
    :return:
    """
    logutil.logger.info("Entering clear_aoi_log")
    try:
        logutil.logger.info("begin clear aoi log")
        start_time = time.time()
        # 获取需要清除的参数
        aoi_log_save_days = inihelper.get_item_int(path_config_ini, "clear_aoi_log",
                                                   "aoi_log_save_days")
        aoi_log_file_filter = inihelper.get_item_string(path_config_ini, "clear_aoi_log",
                                                        "aoi_log_file_filter")

        clear_data_file(aoi_log_save_days, aoi_log_file_filter)

        end_time = time.time()
        spend_time = round(end_time - start_time, 3)
        logutil.logger.info(f"end clear aoi log , spend time is {spend_time}s")
    except Exception as ex:
        logutil.logger.error(f"Error in clear_aoi_log: {ex}", exc_info=True)
    logutil.logger.info("Exiting clear_aoi_log")


def clear_aoi_log_empty_folder():
    """
    清除AOI日志空文件夹
    :return:
    """
    logutil.logger.info("Entering clear_aoi_log_empty_folder")
    try:
        logutil.logger.info("begin clear aoi log empty folder")
        start_time = time.time()
        # 获取需要清除的图像参数
        aoi_log_save_days = inihelper.get_item_int(path_config_ini, "clear_aoi_log",
                                                   "aoi_log_save_days")
        aoi_log_empty_folder_filter = inihelper.get_item_string(path_config_ini, "clear_aoi_log",
                                                                "aoi_log_empty_folder_filter")

        if aoi_log_save_days > 0:
            del_date = datetime.now().date() - relativedelta(days=aoi_log_save_days - 1)
            del_date_filter = f"dc:<{del_date} | dm:<{del_date} "
            del_keywords = f"{aoi_log_empty_folder_filter} {del_date_filter}"
            es.delete_folder(del_keywords)
        else:
            logutil.logger.info(f"save days is negative , stop clear")

        end_time = time.time()
        spend_time = round(end_time - start_time, 3)
        logutil.logger.info(f"end clear aoi log empty folder , spend time is {spend_time}s")
    except Exception as ex:
        logutil.logger.error(f"Error in clear_aoi_log_empty_folder: {ex}", exc_info=True)
    logutil.logger.info("Exiting clear_aoi_log_empty_folder")


def clear_plc_log():
    """
    清除PLC日志文件
    :return:
    """
    logutil.logger.info("Entering clear_plc_log")
    try:
        logutil.logger.info("begin clear plc log")
        start_time = time.time()
        # 获取需要清除的图像参数
        plc_log_save_days = inihelper.get_item_int(path_config_ini, "clear_plc_log",
                                                   "plc_log_save_days")
        plc_log_file_filter = inihelper.get_item_string(path_config_ini, "clear_plc_log",
                                                        "plc_log_file_filter")

        clear_data_file(plc_log_save_days, plc_log_file_filter)

        end_time = time.time()
        spend_time = round(end_time - start_time, 3)
        logutil.logger.info(f"end clear plc log , spend time is {spend_time}s")
    except Exception as ex:
        logutil.logger.error(f"Error in clear_plc_log: {ex}", exc_info=True)
    logutil.logger.info("Exiting clear_plc_log")


def clear_client_operate_records():
    logutil.logger.info("Entering clear_client_operate_records")
    try:
        logutil.logger.info("begin clear client operate records ")
        start_time = time.time()
        app_data = os.getenv("APPDATA")
        if app_data is None:
            logutil.logger.error("Environment variable APPDATA is not set.")
            return
        db_path = os.path.join(app_data, "BM.CommonCache", "Database", "Record.db")
        # print(db_path)
        if os.path.isfile(db_path):
            record_save_days = inihelper.get_item_int(path_config_ini, "clear_client_operate_record",
                                                      "record_save_days")
            if record_save_days < 1:
                return

            del_date = datetime.now().date() - relativedelta(days=record_save_days - 1)
            sql = f"delete from db_operation_record where r_time < '{del_date}'"

            try:
                conn = sqlite3.connect(db_path)
                cur = conn.cursor()
                logutil.logger.info(f"database connect successfull : {db_path}")

                cursor = cur.execute(sql)
                conn.commit()
                logutil.logger.info(sql)
                logutil.logger.info(f"total number of rows deleted : {conn.total_changes}")
            except Exception as ex:
                logutil.logger.error(f"database operate failed : {ex}", exc_info=True)
        else:
            logutil.logger.info(f"{db_path} does not exist")

        end_time = time.time()
        spend_time = round(end_time - start_time, 3)
        logutil.logger.info(f"end clear client operate records , spend time is {spend_time}s")
    except Exception as ex:
        logutil.logger.error(f"Error in clear_client_operate_records: {ex}", exc_info=True)
    logutil.logger.info("Exiting clear_client_operate_records")


# 删除其他数据文件
def clear_others_data(partition):
    """
    清除others配置中的数据
    :param partition:磁盘盘符
    :return:True表示没有数据可以删除，False表示有数据可以删除，并且已经删除
    """
    no_data_flag = True
    logutil.logger.info(f"Entering clear_others_data with partition={partition}")
    try:
        logutil.logger.info("begin clear others data")
        start_time = time.time()
        others_filter_list = inihelper.get_items(path_config_ini, "others")
        for option in others_filter_list:
            option_filter = inihelper.get_item_string(path_config_ini, "others", option)
            if option_filter.startswith(partition):
                filter_keywords = f"{option_filter}"
                es.search(filter_keywords)
                logutil.logger.info(
                    f"search keywords is : {es.get_search_keyword()} , get_num_total_results is : {es.get_num_total_results()}")
                if es.get_num_total_results() > 0:
                    df = es.results(max_num=1, sort_type=11)
                    date_filter = ""
                    try:
                        # 获取文件夹创建日期/修改日期
                        if df.iloc[0, 3]:  # 创建日期为空时，取修改日期
                            delete_date = du_parser.parse(df.iloc[0, 3]).date()
                            date_filter = f"dc:{delete_date}"
                        else:
                            delete_date = du_parser.parse(df.iloc[0, 4]).date()
                            date_filter = f"dm:{delete_date}"

                        delete_keywords = f"{filter_keywords} {date_filter}"
                        logutil.logger.info(f"delete keywords : {delete_keywords}")
                        es.delete_folder(delete_keywords)
                    except Exception as ex:
                        logutil.logger.error(f"Error in date processing in clear_others_data: {ex}", exc_info=True)
                    no_data_flag = no_data_flag & False
                else:
                    logutil.logger.info(f"get_num_total_results is {es.get_num_total_results()} : no data was found")
                    no_data_flag = no_data_flag & True
                    break

        end_time = time.time()
        spend_time = round(end_time - start_time, 3)
        logutil.logger.info(f"end clear others data , spend time is {spend_time}s")
    except Exception as ex:
        logutil.logger.error(f"Error in clear_others_data: {ex}", exc_info=True)
    logutil.logger.info("Exiting clear_others_data")
    return no_data_flag


# 清除AOI数据
def clear_aoi_data():
    logutil.logger.info("Entering clear_aoi_data")
    try:
        disk_free_percent = inihelper.get_item_float(path_config_ini, "settings", "disk_free_percent")
        partitions = psutil.disk_partitions()
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)

            if usage.percent > 100 - disk_free_percent:
                logutil.logger.info(
                    f"{partition.device} disk free is {100 - usage.percent}% , below the warning value {disk_free_percent}%")

                # 防止进入死循环
                max_loop_count = 30
                while usage.percent > 100 - disk_free_percent and max_loop_count > 0:
                    no_data_flag = True
                    max_loop_count = max_loop_count - 1
                    start_time = time.time()
                    logutil.logger.info(
                        f"begin clear aoi data : {partition.device} disk free is {100 - usage.percent}%")

                    keyword = f"{partition.device} vpk_data\\ SourceImage\\ folder:  len:<40"
                    es.search(keyword)
                    logutil.logger.info(
                        f"search keywords is : {es.get_search_keyword()} , get_num_total_results is : {es.get_num_total_results()}")
                    if es.get_num_total_results() > 0:
                        df = es.results(max_num=1, sort_type=11)

                        try:
                            # 获取文件夹创建日期/修改日期
                            if df.iloc[0, 3]:  # 创建日期为空时，取修改日期
                                delete_date = du_parser.parse(df.iloc[0, 3]).date()

                                logutil.logger.info(f"folder : {df.iloc[0, 0]} create time is {delete_date}")
                            else:
                                delete_date = du_parser.parse(df.iloc[0, 4]).date()
                                logutil.logger.info(f"folder : {df.iloc[0, 0]} modify time is {delete_date}")

                            logutil.logger.info(
                                f"deletable numbers : {es.get_num_total_results()} , delete oldest date : {delete_date}")

                            # 清除ExcuteResults(检测数据、汇总数据、区域信息)文件夹中的数据
                            clear_filter = inihelper.get_item_string(path_config_ini, "clear_execute_results",
                                                                     "clear_filter")
                            if clear_filter == "" or clear_filter is None:
                                clear_filter = "vpk_data\\ ExcuteResults\\ folder:  len:<20"
                            execute_results_keyword = f"{partition.device} {clear_filter} dc:<={delete_date} | dm:<={delete_date}"
                            clear_execute_results(execute_results_keyword)

                            # 清除FeatureImage（特征图）文件夹中的数据
                            clear_filter = inihelper.get_item_string(path_config_ini, "clear_feature_image",
                                                                     "clear_filter")
                            if clear_filter == "" or clear_filter is None:
                                clear_filter = "vpk_data\\ FeatureImage\\ folder:  len:<20"
                            feature_image_keyword = f"{partition.device} {clear_filter} dc:<={delete_date} | dm:<={delete_date}"
                            clear_feature_image(feature_image_keyword)

                            # 清除HandleImage（处理图）文件夹中的数据
                            clear_filter = inihelper.get_item_string(path_config_ini, "clear_handle_image",
                                                                     "clear_filter")
                            if clear_filter == "" or clear_filter is None:
                                clear_filter = "vpk_data\\ HandleImage\\ folder:  len:<20"
                            handle_image_keyword = f"{partition.device} {clear_filter} dc:<={delete_date} | dm:<={delete_date}"
                            clear_handle_image(handle_image_keyword)

                            # 清除SourceImage(原图)文件夹中的数据
                            clear_filter = inihelper.get_item_string(path_config_ini, "clear_source_image",
                                                                     "clear_filter")
                            if clear_filter == "" or clear_filter is None:
                                clear_filter = "vpk_data\\ SourceImage\\ folder:  len:<20"
                            source_image_keyword = f"{partition.device} {clear_filter} dc:<={delete_date} | dm:<={delete_date}"
                            clear_source_image(source_image_keyword)

                            # 清除"执行结果"文件夹中的数据
                            exe_result_keyword = f"{partition.device} vpk_data\\执行结果\\  regex:\\d- folder: dc:<={delete_date} | dm:<={delete_date}"
                            clear_exe_result(exe_result_keyword)

                            # 清除空文件夹
                            empty_folder_keyword = f"{partition.device} vpk_data\\ empty: dc:<={delete_date} | dm:<={delete_date}"
                            clear_empty_folder(empty_folder_keyword)

                            end_time = time.time()
                            spend_time = round(end_time - start_time, 3)
                            logutil.logger.info(f"end clear aoi data : {partition.device} spend time is {spend_time}s")
                        except Exception as ex:
                            logutil.logger.error(f"Error in aoi data deletion loop: {ex}", exc_info=True)

                        no_data_flag = no_data_flag & False
                    else:
                        logutil.logger.info(
                            f"get_num_total_results is {es.get_num_total_results()} : no data was found")
                        no_data_flag = no_data_flag & True

                    # 清除others配置中的数据
                    no_data_flag_others = clear_others_data(partition.device)
                    no_data_flag = no_data_flag & no_data_flag_others
                    if no_data_flag:
                        break

                    usage = psutil.disk_usage(partition.mountpoint)
            else:
                logutil.logger.info(
                    f"{partition.device} disk free is {100 - usage.percent}% , above the warning value {disk_free_percent}")
    except Exception as ex:
        logutil.logger.error(f"Error in clear_aoi_data: {ex}", exc_info=True)
    logutil.logger.info("Exiting clear_aoi_data")


# 定时任务
def schedule_job():
    logutil.logger.info(
        "************************************************ begin ************************************************")
    try:
        # 清除AOI检测数据
        clear_aoi_data()

        # 清除AOI日志
        clear_aoi_log()

        # 清除AOI日志空文件夹
        clear_aoi_log_empty_folder()

        # 清除PLC日志
        clear_plc_log()

        # 清除客户端保存的操作记录
        clear_client_operate_records()
    except Exception as ex:
        logutil.logger.error(f"Error in schedule_job: {ex}", exc_info=True)
    logutil.logger.info(
        "************************************************ end ************************************************")


def monitor(interval=0.1):
    logutil.logger.info("Entering monitor")
    try:
        current_pid = os.getpid()
        current_process_name = psutilhelper.get_processname_by_id(current_pid)

        thread_res = Thread(target=psutilhelper.monitor_resource, args=(current_process_name, interval), daemon=False)
        thread_res.start()
    except Exception as ex:
        logutil.logger.error(f"Error in monitor: {ex}", exc_info=True)
    logutil.logger.info("Exiting monitor")


def startup():
    logutil.logger.info("Entering startup")
    try:
        logutil.logger.info("diskmgr.exe startup")
        # 获取当前程序所有进程（路径匹配）
        self_procs = psutilhelper.get_self_processes()
        new_pid_list = [proc.pid for proc in self_procs]

        process_file = pathlib.Path(os.getcwd() + r"\process.txt")
        if process_file.exists():
            save_pid_text = process_file.read_text()
            if save_pid_text:
                save_pid_list = save_pid_text.split(",")
                for save_pid in save_pid_list:
                    save_pid_int = int(save_pid)
                    if save_pid_int in new_pid_list:
                        # 避免杀死自身（当前进程已在 new_pid_list 中）
                        continue
                    try:
                        psutilhelper.kill_procee_by_id(save_pid_int)
                    except Exception as ex:
                        logutil.logger.error(f"Failed to kill PID {save_pid_int}: {ex}")

        # 保存当前所有进程 PID（包括自身）
        data_text = ",".join(map(str, new_pid_list))
        process_file.write_text(data=data_text)
    except Exception as ex:
        logutil.logger.error(f"Error in startup: {ex}", exc_info=True)
    logutil.logger.info("Exiting startup")


if __name__ == '__main__':
    logutil.logger.info(f"加载配置文件：{path_config_ini}")

    # 防止多开
    startup()

    # 读取清理时间配置
try:
    clear_timer = inihelper.get_item_string(path_config_ini, "settings", "clear_time") or ""
    clear_timer_list = [t.strip() for t in clear_timer.split("|") if t.strip()]
except KeyError as e:
    logutil.logger.error(f"清理时间配置缺失：{e}")
    clear_timer_list = []

    # 注册定时任务
    schedule.clear()
    for at_timer in clear_timer_list:
        if not inihelper.validate_time_format(at_timer,"%H:%M"):  # 自定义时间格式校验函数
            continue
        logutil.logger.info(f"注册定时任务：{at_timer}")
        schedule.every().day.at(at_timer).do(schedule_job)

    # 读取开关配置
    try:
        on_off = inihelper.get_item_string(path_config_ini, "settings", "on_off") or "OFF"
        on_off = on_off.upper()
    except Exception as e:
        logutil.logger.warning(f"开关配置缺失，启用默认值 OFF。错误：{e}")
        on_off = "OFF"

    # 执行逻辑
    if on_off == "ON":
        logutil.logger.info("启动磁盘清理服务")
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logutil.logger.info("用户主动终止服务")
        except Exception as ex:
            logutil.logger.error(f"主循环异常：{ex}", exc_info=True)
    elif on_off == "OFF":
        logutil.logger.info("服务未启用")
    else:
        logutil.logger.error("无效的开关配置（仅允许ON/OFF）")