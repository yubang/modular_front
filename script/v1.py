# coding:UTF-8


"""
第一版脚本入口
@author: yubang
2016.04.20
"""


from lib.make_component import get_component_js_str
from lib.merge_file import get_after_merge_file_str
from lib.static_minify import minify_file
from lib import tools
import os
import yaml


def init():
    read_all_rule('./rule')


def read_all_rule(rule_dir):
    if os.path.isdir(rule_dir):
        dirs = os.listdir(rule_dir)
        for obj in dirs:
            read_all_rule(rule_dir + '/' + obj)
    else:
        with open(rule_dir, 'r') as fp:
            handle_rule(yaml.load(fp.read()))


def handle_rule(data):
    if data['rule'] == 'make_component':
        make_component(data)
    elif data['rule'] == 'merge':
        merge_file(data)
    elif data['rule'] == 'minify':
        minify_file_in_script(data)


def make_component(data):
    """
    制作组件
    :param data: 规则字典
    :return:
    """
    js = get_component_js_str(data['source_path'])
    tools.output_file(data['target_path'], js)


def merge_file(data):
    """
    合并文件
    :param data: 规则字典
    :return:
    """
    text = get_after_merge_file_str(data['source_path'])
    text = minify_file(text, data['minify'])
    tools.output_file(data['target_path'], text)


def minify_file_in_script(data, offset_path='.'):
    """
    压缩文件
    :param data: 规则字典
    :param path: 当前路径
    :return:
    """
    now_path = data['source_path'] + '/' + offset_path
    if os.path.isdir(now_path):
        fps = os.listdir(now_path)
        for fp in fps:
            minify_file_in_script(data, offset_path + '/' + fp)
    else:
        fp_type = tools.get_file_type(now_path)
        if fp_type and fp_type in ['html', 'css', 'js']:
            read_type = 'r'
        else:
            read_type = 'rb'
        print(fp_type)
        with open(now_path, read_type) as fp:
            fp_data = fp.read()
            if fp_type and fp_type in ['html', 'css', 'js']:
                fp_data = minify_file(fp_data, fp_type)
                write_type = 'w'
            else:
                write_type = 'wb'
            tools.output_file(data['target_path'] + '/' + offset_path, fp_data, write_type)
