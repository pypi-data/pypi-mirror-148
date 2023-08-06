# _*_ coding: utf-8 _*_
# @Author : 魏来
# @Version：基础版本(初级UI自动化框架)
# -------**---**-------




from selenium.webdriver import Remote
from selenium import webdriver
from loguru import logger
from common.base_path import _dir
from common import _read_yaml


def browser_init():
    """定义浏览器类型并返回driver对象"""
    web_cfg_data = _read_yaml.read_yaml()['browser']
    if web_cfg_data['type'] == 'chrome':
        if web_cfg_data['env'] == 'localhost':
            driver = webdriver.Chrome()
        elif web_cfg_data['env'] == 'grid':
            driver = Remote(command_executor=web_cfg_data['gridUrl'],
                            desired_capabilities={
                                "browserName": "chrome",
                            })
        else:
            raise ValueError('env类型定义错误！')

    elif web_cfg_data['type'] == 'firefox':
        if web_cfg_data['env'] == 'localhost':
            driver = webdriver.Firefox()
        else:
            raise ValueError('env类型定义错误！')
    elif web_cfg_data['type'] == 'ie':
        if web_cfg_data['env'] == 'localhost':
            driver = webdriver.Ie()
        elif web_cfg_data['env'] == 'grid':
            driver = Remote(command_executor=web_cfg_data['gridUrl'],
                            desired_capabilities={
                                "browserName": "internet explorer",
                            })
        else:
            raise ValueError('env类型定义错误！')
    else:
        raise ValueError('driver驱动类型定义错误！')
    logger.info(f'在{web_cfg_data["env"]}使用{web_cfg_data["type"]}执行')
    driver.maximize_window()


    return driver
