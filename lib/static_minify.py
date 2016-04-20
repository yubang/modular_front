# coding:UTF-8


"""
静态资源压缩
@author: yubang
2016.04.20
"""


from css_html_js_minify import html_minify, css_minify, js_minify


def handle_html(html_data):
    return html_minify(html_data)


def handle_css(css_data):
    return css_minify(css_data)


def handle_javascript(js_data):
    return js_minify(js_data)
