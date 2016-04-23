# coding:UTF-8


"""
css预编译处理
@author: yubang
2016.04.23
"""

from lib.static_minify import handle_css
from functools import wraps
from scss import Compiler
from six import StringIO
import lesscpy


def minify_css(fn):
    @wraps(fn)
    def handle(*k, **v):
        return handle_css(fn(*k, **v))
    return handle


@minify_css
def handle_scss(scss_str):
    """
    编译scss字符串
    :param scss_str: scss字符串
    :return:
    """
    return Compiler().compile_string(scss_str)


@minify_css
def handle_less(less_str):
    """
    编译less字符串
    :param less_str: less字符串
    :return:
    """
    return lesscpy.compile(StringIO(less_str))


