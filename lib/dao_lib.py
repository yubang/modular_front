# coding:UTF-8


"""
该文件是必须实现的接口
@author: yubang
2016.04.23
"""


from lib.make_component import get_component_js_str
from lib.merge_file import get_after_merge_file_str
from lib.static_minify import minify_file
from lib import tools
from lib.log_lib import log
from lib import css_precompiled as css_precompiled_lib
from lib.render_html import render_html_use_template, build_html_use_template
import os


def css_precompiled_get_str(data, offset_path='.'):
    """
    预编译css
    :param data: 规则字典
    :param argv: 输入变量
    :return:
    """
    css_str = ''
    now_path = data['source_path'] + '/' + offset_path
    if os.path.isdir(now_path):
        fps = os.listdir(now_path)
        for fp in fps:
            css_str += css_precompiled_get_str(data, '/'.join([offset_path, fp]))
    else:
        with open(now_path, 'r') as fp:
            file_type = tools.get_file_type(now_path)
            if file_type not in ['styl', 'less', 'scss', 'css']:
                return
            if file_type == 'scss':
                fp_data = css_precompiled_lib.handle_scss(fp.read())
            elif file_type == 'less':
                fp_data = css_precompiled_lib.handle_less(fp.read())
            else:
                fp_data = fp.read()
            css_str += fp_data
    return css_str + '\n'


def css_precompiled(data, offset_path='.', argv=None):
    """
    预编译css
    :param data: 规则字典
    :param argv: 输入变量
    :return:
    """
    now_path = data['source_path'] + '/' + offset_path
    if os.path.isdir(now_path):
        fps = os.listdir(now_path)
        for fp in fps:
            css_precompiled(data, '/'.join([offset_path, fp]), argv)
    else:

        # 判断是不是修改了这个文件
        if os.path.realpath(now_path) != os.path.realpath(argv['change_file_path']):
            return

        with open(now_path, 'r') as fp:
            file_type = tools.get_file_type(now_path)
            if file_type not in ['styl', 'less', 'scss', 'css', 'sass']:
                return
            if file_type == 'scss' or file_type == 'sass':
                fp_data = css_precompiled_lib.handle_scss(fp.read())
            elif file_type == 'less':
                fp_data = css_precompiled_lib.handle_less(fp.read())
            else:
                fp_data = fp.read()
            tools.output_file(data['target_path'] + '/' + offset_path + '.css', fp_data)


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
    text = minify_file(text, data['minify'], data['encryption'], data['encryption'])
    tools.output_file(data['target_path'], text)


def minify_file_in_script(data, offset_path='.', argv=None):
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
            minify_file_in_script(data, offset_path + '/' + fp, argv=argv)
    else:

        # 判断是不是修改了这个文件
        if os.path.realpath(now_path) != os.path.realpath(argv['change_file_path']):
            return

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


def handle_render_html(data, offset_path='.', argv=None):
    """
    渲染html
    :param data: 规则字典
    :return:
    """
    now_path = data['source_path'] + '/' + offset_path
    if os.path.isdir(now_path):
        fps = os.listdir(now_path)
        for fp in fps:
            handle_render_html(data, '/'.join([offset_path, fp]), argv)
    else:

        # 判断是不是.html文件
        if not now_path.endswith('.html'):
            return

        with open(now_path, 'r') as fp:
            html = render_html_use_template(fp.read(), now_path)
            tools.output_file(data['target_path'] + '/' + offset_path, html)


def build_html(data, offset_path='.', argv=None):
    """
    生成线上html
    :return:
    """
    now_path = data['source_path'] + '/' + offset_path
    if os.path.isdir(now_path):
        fps = os.listdir(now_path)
        for fp in fps:
            build_html(data, '/'.join([offset_path, fp]), argv)
    else:

        # 判断是不是.html文件
        if not now_path.endswith('.html'):
            return

        # 编译html文件
        print("编译html文件：%s" % now_path)
        log.info("编译html文件：%s" % now_path)

        with open(now_path, 'r') as fp:
            html = build_html_use_template(fp.read(), now_path, data)
            tools.output_file(data['target_path'] + '/' + offset_path, html)

