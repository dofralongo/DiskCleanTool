;本工具清理如下内容：1)\VisionPK\vpk_data;  2)\VisionPK\Log;  3)操作记录;  4)PLC日志;  5)自定义数据;
;设置开启自启和其他说明请阅读根目录下diskmgr_manual.docx

[settings]
;总开关，是否启用本工具，ON代表启用，OFF代表不启用，默认不启用
on_off=off
;格式：mm:ss，如9点，则clear_time=09:00。如果需要多个时间点定时删除，用英文|分割，如08:10|20:10
clear_time=08:10|20:66
;磁盘警戒线,剩余磁盘百分比
disk_free_percent=30

;清除ExcuteResults(检测数据、汇总数据、区域信息)文件夹中的数据
[clear_execute_results]
clear_filter=vpk_data\ ExcuteResults\ folder:  len:<20

;清除FeatureImage（特征图）文件夹中的数据
[clear_feature_image]
clear_filter=vpk_data\ FeatureImage\ folder:  len:<20

;清除HandleImage（处理图）文件夹中的数据
[clear_handle_image]
clear_filter=vpk_data\ HandleImage\ folder:  len:<20

;清除SourceImage(原图)文件夹中的数据
[clear_source_image]
clear_filter=vpk_data\ SourceImage\ folder:  len:<20


;清除AOI日志及日志空文件夹
[clear_aoi_log]
;负数表示不启用清除
aoi_log_save_days=3
aoi_log_file_filter=path:Log\ExecutionStation|path:\Log\TriggerStation|path:\Log\SummaryStation file:
aoi_log_empty_folder_filter=path:Log\ExecutionStation|path:\Log\TriggerStation|path:\Log\SummaryStation empty:

;清除plc日志
[clear_plc_log]
;负数表示不启用清除
plc_log_save_days = 3
plc_log_file_filter=path:\plc_plugins \log *.log file:

;清除客户端（C）操作日志
[clear_client_operate_record]
record_save_days=180

;清除其他数据
[others]
clear_data_filter1=D:\minio\data\image\1\ \FeatureImage\ len:<10 folder:
clear_data_filter2=D:\minio\data\image\1\ \SourceImage\ len:<10 folder:

