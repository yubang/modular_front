# coding:UTF-8


"""
第一版脚本入口
@author: yubang
2016.04.20
"""


from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from lib.make_component import get_component_js_str
from lib.merge_file import get_after_merge_file_str
from lib.static_minify import minify_file
from lib import tools
from lib.log_lib import log
import traceback
import os
import yaml
import copy


def init(argv):
    read_all_rule('./rule', argv)


def read_all_rule(rule_dir, argv):
    """
    读取所有的规则文件
    :param rule_dir: 规则文件目录
    :param argv: 启动参数
    :return:
    """
    if os.path.isdir(rule_dir):
        dirs = os.listdir(rule_dir)
        for obj in dirs:
            read_all_rule(rule_dir + '/' + obj, argv)
    else:
        with open(rule_dir, 'r') as fp:
            handle_rule(yaml.load(fp.read()), argv)


def handle_rule_data(data, argv):
    """
    处理规则字典
    :param data: 规则字典
    :param argv: 动态参数
    :return:
    """
    data['source_path'] = argv['project_path'] + '/' + data['source_path']
    data['target_path'] = argv['project_path'] + '/' + data['target_path']
    return data


def handle_rule(data, argv):
    """
    规则处理器
    :param data: 规则字典
    :param argv: 动态参数
    :return:
    """

    data = handle_rule_data(data, argv)

    # 判断规则是不是需要执行
    changle_file_path = argv['change_file_path']
    if not changle_file_path.startswith(os.path.realpath(data['source_path'])):
        return

    if data['rule'] == 'make_component':
        log.info('触发制作组件，文件源：%s' % changle_file_path)
        make_component(data)
    elif data['rule'] == 'merge':
        log.info('触发合并文件，文件源：%s' % changle_file_path)
        merge_file(data)
    elif data['rule'] == 'minify':
        log.info('触发压缩文件，文件源：%s' % changle_file_path)
        minify_file_in_script(data)


def make_component(data):
    """
    制作组件
    :param data: 规则字典
    :return:
    """
    js, code = get_component_js_str(data['source_path'])

    if code == 0:
        tools.output_file(data['target_path'], js)
    elif code == -1:
        log.info('由于没有发现组件配置文件，所以忽略本次制作')


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

        with open(now_path, read_type) as fp:
            fp_data = fp.read()
            if fp_type and fp_type in ['html', 'css', 'js']:
                fp_data = minify_file(fp_data, fp_type, data['encryption'], data['encryption'])
                write_type = 'w'
            else:
                write_type = 'wb'
            tools.output_file(data['target_path'] + '/' + offset_path, fp_data, write_type)


class MyHandle(FileSystemEventHandler):
    def __init__(self, argv):
        self.argv = argv
        super(MyHandle, self).__init__()

    def handle_all(self, event):
        if not event.is_directory:
            log.info('监控到文件变化：%s' % event.src_path)
            argv = copy.deepcopy(self.argv)
            argv['change_file_path'] = event.src_path
            try:
                init(argv)
            except:
                traceback.print_exc()

    def on_created(self, event):
        if not event.is_directory and os.path.exists(event.src_path) and os.path.getsize(event.src_path):
            self.handle_all(event)

    def on_deleted(self, event):
        self.handle_all(event)

    def on_modified(self, event):
        self.handle_all(event)

    def on_moved(self, event):
        self.handle_all(event)


def start_monitor(argv):
    """
    启动文件监视器
    :return:
    """
    log.info('启动前端模块化小工具')
    monitor = Observer()
    event_handler = MyHandle(argv)
    monitor.schedule(event_handler, path=argv['watch_path'], recursive=True)
    monitor.start()
    input("按回车自动退出\n")
    log.info('退出前端模块化小工具')
    exit(0)
