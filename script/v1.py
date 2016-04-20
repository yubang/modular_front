# coding:UTF-8


"""
第一版脚本入口
@author: yubang
2016.04.20
"""


from lib.make_component import get_component_js_str
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
    if data['rule']:
        make_component(data)


def make_component(data):
    js = get_component_js_str(data['source_path'])
    tools.output_file(data['target_path'], js)
