# coding:UTF-8


"""
第一版脚本入口
@author: yubang
2016.04.20
"""


from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from lib.log_lib import log
from lib import tools, dao_lib
import copy
import traceback
import os
import yaml
import time


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

    if 'hash_static_path' in argv:
        data['hash_static_path'] = argv['project_path'] + '/' + data['hash_static_path']

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
        dao_lib.make_component(data)
        print('制作组件完成 ' + time.strftime('%H:%M:%S'))
    elif data['rule'] == 'merge':
        log.info('触发合并文件，文件源：%s' % changle_file_path)
        dao_lib.merge_file(data)
        print('合并文件完成 ' + time.strftime('%H:%M:%S'))
    elif data['rule'] == 'minify':
        log.info('触发压缩文件，文件源：%s' % changle_file_path)
        dao_lib.minify_file_in_script(data, argv=argv)
        print('压缩文件完成 ' + time.strftime('%H:%M:%S'))
    elif data['rule'] == 'css_precompiled':
        log.info('触发预编译css文件，文件源：%s' % changle_file_path)
        dao_lib.css_precompiled(data, argv=argv)
        print('预编译css文件完成 ' + time.strftime('%H:%M:%S'))
    elif data['rule'] == 'css_precompiled_and_merge':
        log.info('触发预编译css文件，文件源：%s' % changle_file_path)
        # 获取合并后的css
        if data['compiled_first']:
            # 先编译再合并
            d = dao_lib.css_precompiled_get_str(data)
        else:
            d = dao_lib.get_after_merge_file_str(data['source_path'], file_type='[scss|less]$')
            if data['compiled_type'] == 'scss':
                d = dao_lib.css_precompiled_lib.handle_scss(d)
            elif data['compiled_type'] == 'less':
                d = dao_lib.css_precompiled_lib.handle_less(d)

        tools.output_file(data['target_path'], d)
        print('预编译css文件（并且合并成一个css）完成 ' + time.strftime('%H:%M:%S'))
    elif data['rule'] == 'render_html':
        log.info('触发预编译html文件，文件源：%s' % changle_file_path)
        dao_lib.handle_render_html(data, argv=argv)
        print('预编译html文件完成 ' + time.strftime('%H:%M:%S'))


class MyHandle(FileSystemEventHandler):
    def __init__(self, argv):
        self.argv = argv
        super(MyHandle, self).__init__()

    def handle_all(self, event):

        # 忽略 .开头的隐藏文件
        if os.path.basename(event.src_path)[0:1] == '.':
            return
        # 忽略文件夹
        if not event.is_directory:
            log.info('监控到文件变化：%s' % event.src_path)
            argv = copy.deepcopy(self.argv)
            argv['change_file_path'] = event.src_path

            # 只处理已知的几种文件
            know_files = [
                'html', 'vue', 'txt', 'js', 'css',
                'jpg', 'png', 'less', 'scss', 'sass',
                'htm'
            ]
            if tools.get_file_type(event.src_path) not in know_files:
                return

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


def handle_html_build_in_release(data, argv):
    """
    编译成线上运行所需要的html
    :return:
    """
    # 判断是不是编译html指令
    if data['rule'] != 'render_html':
        return

    dao_lib.build_html(data, argv=argv)


def read_all_rule_in_build_html(rule_dir, argv):
    """
    读取所有的规则文件
    :param rule_dir: 规则文件目录
    :param argv: 启动参数
    :return:
    """
    if os.path.isdir(rule_dir):
        dirs = os.listdir(rule_dir)
        for obj in dirs:
            read_all_rule_in_build_html(rule_dir + '/' + obj, argv)
    else:
        with open(rule_dir, 'r') as fp:
            handle_html_build_in_release(yaml.load(fp.read()), argv)