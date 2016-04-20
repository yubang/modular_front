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
