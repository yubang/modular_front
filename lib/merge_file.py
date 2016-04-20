# coding:UTF-8


"""
合并文件模块
@author: yubang
2016.04.20
"""

from lib import static_minify
import os
import re


def get_after_merge_file_str(dir_path, is_first=True, file_type=r'.*', minify_type=None):
    """
    获取合并后的字符串
    :param dir_path: 文件夹路径
    :param is_first: 是不是第一次遍历，用于压缩
    :param file_type: 用于搜索文件
    :param minify_type: 使用哪一种压缩（html，css，js）
    :return:
    """
    now_str = ''
    if os.path.isdir(dir_path):
        dirs = os.listdir(dir_path)
        for obj in dirs:
            now_str = '\n'.join([now_str, get_after_merge_file_str(dir_path + '/' + obj, is_first=False, file_type=file_type, minify_type=minify_type)])
    else:
        if re.search(file_type, dir_path):
            with open(dir_path, 'r') as fp:
                now_str = '\n'.join([now_str, fp.read()])

    if is_first and minify_type:
        if minify_type == 'html':
            now_str = static_minify.handle_html(now_str)
        elif minify_type == 'css':
            now_str = static_minify.handle_css(now_str)
        else:
            now_str = static_minify.handle_javascript(now_str)

    return now_str
