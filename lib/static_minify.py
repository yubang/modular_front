# coding:UTF-8


"""
静态资源压缩
@author: yubang
2016.04.20
"""

from slimit import minify
import cssmin
import htmlmin


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


def handle_javascript(js_data):
    """
    压缩混淆js
    :param js_data: js字符串
    :return:
    """
    return minify(js_data, mangle=True, mangle_toplevel=True)


def minify_file(data, minify_type):
    """
    压缩文件
    :param data: 文件字符串
    :param minify_type: 压缩方式（html, css, js, None）
    :return:
    """
    if minify_type == 'html':
        return handle_html(data)
    elif minify_type == 'css':
        return handle_css(data)
    elif minify_type == 'js':
        return handle_javascript(data)
    else:
        return data
