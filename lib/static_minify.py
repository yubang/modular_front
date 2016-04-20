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
    html = htmlmin.minify(html_data, remove_comments=True, remove_empty_space=True, remove_all_empty_space=True)
    return html


def handle_css(css_data):
    return cssmin.cssmin(css_data)


def handle_javascript(js_data):
    return minify(js_data, mangle=True, mangle_toplevel=True)


def minify_file(data, minify_type):
    if minify_type == 'html':
        return handle_html(data)
    elif minify_type == 'css':
        return handle_css(data)
    elif minify_type == 'js':
        return handle_javascript(data)
    else:
        return data
