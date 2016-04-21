# coding:UTF-8


"""
静态资源压缩
@author: yubang
2016.04.20
"""

from slimit import minify
import cssmin
import htmlmin
import time
import hashlib


def handle_html(html_data):
    """
    压缩html文件
    :param html_data: html字符串
    :return:
    """
    html = htmlmin.minify(html_data, remove_comments=True, remove_empty_space=True, remove_all_empty_space=True)
    return html


def handle_css(css_data):
    """
    压缩css文件
    :param css_data: css字符串
    :return:
    """
    return cssmin.cssmin(css_data)


def handle_javascript(js_data, mangle=True, mangle_toplevel=True):
    """
    压缩混淆js
    :param js_data: js字符串
    :return:
    """
    return minify(js_data, mangle=mangle, mangle_toplevel=mangle_toplevel)


def minify_file(data, minify_type, encryption=True, add_anonymous_function=False):
    """
    压缩文件
    :param data: 文件字符串
    :param minify_type: 压缩方式（html, css, js, None）
    :param encryption: 是否混淆js
    :param add_anonymous_function: 是否为js添加匿名函数
    :return:
    """
    if minify_type == 'html':
        return handle_html(data)
    elif minify_type == 'css':
        return handle_css(data)
    elif minify_type == 'js':
        js = handle_javascript(data, encryption, encryption)

        if add_anonymous_function:
            js = handle_js_anonymous_function(js)
        return js
    else:
        return data


def handle_js_anonymous_function(js_data):
    """
    为js函数包裹上匿名函数，防止函数冲突
    :param js_data: js字符串
    :return:
    """

    function_name = hashlib.md5(str(time.time()).encode("UTF-8")).hexdigest()

    code = """function tools_anonymous_%s(){%s return this;}tools_anonymous_%s();""" % (function_name, js_data, function_name)
    code = code.strip()
    return "//本文件使用https://github.com/yubang/modular_front压缩\n"+code
