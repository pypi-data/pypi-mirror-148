# _*_ coding: utf-8 _*_
# @Author : 魏来
# @Version：基础版本(初级UI自动化框架)
# -------**---**-------



import yaml
import os
from common.base_path import _dir
from loguru import logger

def read_yaml():
    """读取yaml文件并return文件"""
    file_dir = _dir + '/config/cfg.yaml'.replace(r'\/'.replace(os.sep, ''), os.sep)
    #    path_file = file_dir.replace('libs', 'config').replace('utils','cfg.yaml')
    with open(file_dir, mode='r', encoding='utf-8') as file:
        msg = yaml.load(file, Loader=yaml.FullLoader)
    return msg


def load_yaml(file_path):
    """读取yaml并return"""
    logger.info("加载 {} 文件......".format(file_path))
    with open(file_path, mode='r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data


def load(file_name, path=_dir):
    """在项目内读取指定文件"""
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)  # 将目录和文件名拼接
        if os.path.isdir(c_path):  # 如果是目录继续调用
            data = load(file_name, c_path)
            if data is not None:
                return data
        elif file_name == i:
            data = load_yaml(c_path)
            return data

def read_yaml_url(key, filename=_dir + 'config/data.yaml'):
    with open(filename, 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        keys = key.split(".")
        for k in keys:
            data = data[k]
        return data
