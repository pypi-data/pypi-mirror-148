# _*_ coding: utf-8 _*_
# @Author : 魏来
# @Version：基础版本(初级UI自动化框架)
# -------**---**-------



import time
import allure
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from loguru import logger
from common.base_path import _dir


class BaseUtil():
    """
    selenium底层方法封装

    """

    def __init__(self ,driver, page_name=''):
        self.driver=driver
        self.page = page_name
        # #############浏览器操作部分#############
        def get(self, url):
            """
            发送url请求
            :param url: 请求url
            :return: None
            """
            try:
                logger.info(f'打开:{url}')
                self.driver.get(url)
            except Exception:
                raise

        def find_element(self, ele, timeout_=30, poll_=0.5,  msg=''):
            """
            定位元素方法封装 匿名函数+显示等待
            :param timeout_:
            :param poll_:
            :param ele:
            :param msg:
            :return:
            """
            if not isinstance(ele, tuple):
                raise TypeError('loc参数类型错误，必须是元组；loc = ("id", "value1")')

            else:
                try:
                    logger.info('定位{}页面元素：{}, 元素描述：{}'.format(self.page, ele, msg))
                    start_time = time.time()
                    _wait = WebDriverWait(self.driver, timeout=timeout_, poll_frequency=poll_)
                    _location = _wait.until(lambda x: x.find_element(*ele))
                    end_time = time.time()
                except Exception:
                    logger.error('元素定位失败!')
                    self.save_screenshot()
                    raise
                else:
                    logger.info('元素定位成功：耗时{}秒!'.format(round(end_time - start_time, 3)))
                    return ele

        def save_screenshot(self):
            """
            截图加入allure报告
            :return: None
            """
            name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
            filepath = _dir + r'\img\{}.png'.format(name)
            try:
                self.driver.save_screenshot(filepath)
                logger.info("截屏成功,图片路径为{}".format(filepath))
                sleep(1)
                allure.attach.file(filepath, name, allure.attachment_type.PNG)
            except Exception:
                logger.error("截屏失败")