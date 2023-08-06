# encoding=utf-8
import logging, time


# 日志部分
def init_log(name, much=False):
    """
    :param name: 日志名
    :param much: 按天记录
    :return: 日志对象
    """
    name = name if name.endswith(".log") else f"{name}.log"
    if much:
        name += time.strftime("%Y-%m-%d", time.localtime())
    # 创建一个带名称的日志程序
    logger = logging.getLogger("yazhe")
    # 设置该程序级别为debug
    logger.setLevel(logging.DEBUG)
    # 创建一个格式器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # 标准流处理器，设置的级别为WARAING
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    # 文件处理器，设置的级别为INFO
    file_handler = logging.FileHandler(filename=name, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
