"""
运行启动文件
"""
import pytest

from config.runConfig import mainSetup as ms, mainTearDown as mt

if __name__ == '__main__':
    ms()        #测试前置
    pytest.main()
    mt()        #测试后置




