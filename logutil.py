
from loguru import  logger

folder_ = "./log/"
prefix_ = "bm-"
rotation_ = "10 MB"
retention_ = "3 days"
encoding_ = "utf-8"
backtrace_ = True
diagnose_ = True



# 格式里面添加了process和thread记录，方便查看多进程和线程程序
format_ = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> ' \
            '| <magenta>{process}</magenta>:<yellow>{thread}</yellow> ' \
            '| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<yellow>{line}</yellow> - <level>{message}</level>'

# 这里面采用了层次式的日志记录方式，就是低级日志文件会记录比他高的所有级别日志，这样可以做到低等级日志最丰富，高级别日志更少更关键
# trace
logger.add(folder_ + prefix_ + "trace.log", level="TRACE", backtrace=backtrace_, diagnose=diagnose_,
            format=format_, colorize=False,
            rotation=rotation_, retention=retention_, encoding=encoding_,
            filter=lambda record: record["level"].no >= logger.level("TRACE").no)

# debug
logger.add(folder_ + prefix_ + "debug.log", level="DEBUG", backtrace=backtrace_, diagnose=diagnose_,
            format=format_, colorize=False,
            rotation=rotation_, retention=retention_, encoding=encoding_,
            filter=lambda record: record["level"].no == logger.level("DEBUG").no)

# info
logger.add(folder_ + prefix_ + "info.log", level="INFO", backtrace=backtrace_, diagnose=diagnose_,
            format=format_, colorize=False,
            rotation=rotation_, retention=retention_, encoding=encoding_,
            filter=lambda record: record["level"].no == logger.level("INFO").no)

# warning
logger.add(folder_ + prefix_ + "warning.log", level="WARNING", backtrace=backtrace_, diagnose=diagnose_,
            format=format_, colorize=False,
            rotation=rotation_, retention=retention_, encoding=encoding_,
            filter=lambda record: record["level"].no == logger.level("WARNING").no)

# error
logger.add(folder_ + prefix_ + "error.log", level="ERROR", backtrace=backtrace_, diagnose=diagnose_,
            format=format_, colorize=False,
            rotation=rotation_, retention=retention_, encoding=encoding_,
            filter=lambda record: record["level"].no == logger.level("ERROR").no)

# critical
logger.add(folder_ + prefix_ + "critical.log", level="CRITICAL", backtrace=backtrace_, diagnose=diagnose_,
            format=format_, colorize=False,
            rotation=rotation_, retention=retention_, encoding=encoding_,
            filter=lambda record: record["level"].no == logger.level("CRITICAL").no)

# logger.add(sys.stderr, level="CRITICAL", backtrace=backtrace_, diagnose=diagnose_,
#             format=format_, colorize=True,
#             filter=lambda record: record["level"].no >= logger.level("CRITICAL").no)