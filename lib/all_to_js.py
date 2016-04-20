# coding:UTF-8


"""
这个文件的目标是所有的数据都转换成js
@author: yubang
2016.04.20
"""


import time
import hashlib


def build_js_data(source_str, str_name=None):
    """
    原始数据转成js
    :param source_str: 原始数据
    :param str_name: 生成的js字符串名字
    :return:
    """

    if not str_name:
        str_name = hashlib.md5(str(time.time())).hexdigest()

    after_handle_data = source_str.strip()
    after_handle_data = after_handle_data.replace('"', '\\"')
    return 'var ' + str_name + '="' + after_handle_data + '";', str_name
