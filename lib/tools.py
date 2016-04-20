# coding:UTF-8


"""
杂七杂八的小工具
"""


import os


def output_file(file_path, fp_data):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    with open(file_path, 'w') as fp:
        fp.write(fp_data)


def get_file_type(file_path):
    """
    获取文件类型
    :param file_path: 文件路径
    :return:
    """
    t = file_path.split('.')
    if len(t) <= 1:
        return None
    else:
        return t[-2:-1]
