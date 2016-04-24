# coding:UTF-8


"""
html预处理
@author: yubang
2016.04.24
"""


from bs4 import BeautifulSoup
from config import tip
from lib.static_minify import handle_html
from lib import tools
import os
import hashlib


def handle_css_of_js_path(path):
    path = path.split("?")
    return path[0]


def str_to_file_path(string, char_num):
    """
    字符串切割成若干等分
    :param string: 字符串
    :param char_num: 每段字符
    :return:
    """
    objs = []

    for index, c in enumerate(string):
        i = int(index / char_num)
        if len(objs) <= i:
            objs.append('')
        objs[i] += c

    return '/'.join(objs)


def render_html_use_template(html_str, file_path):
    """
    渲染html代码
    :param html_str: html模板
    :return:
    """

    # 处理路径
    file_path = os.path.dirname(file_path)

    html_str = handle_html_code(html_str, file_path)
    html_str = handle_css_and_js_version(html_str, file_path)
    html_str = handle_html(html_str)
    html_str = tip.html_tip + html_str
    return html_str


def handle_css_and_js_version(html_str, file_path):
    """
    为js和css打上版本号
    :param html_str: html代码
    :return:
    """
    soup = BeautifulSoup(html_str, "html.parser")
    links = soup.find_all("link")
    for index, _ in enumerate(links):
        if 'href' not in links[index]:
            continue
        link_path = handle_css_of_js_path(links[index]['href'])
        path = file_path + '/' + link_path
        if os.path.exists(path):
            with open(path, 'r') as fp:
                version = hashlib.md5(fp.read().encode("UTF-8")).hexdigest()[8: -8]
                links[index]['href'] = link_path + '?v=' + version

    scripts = soup.find_all("script")

    for index, _ in enumerate(scripts):

        if not scripts[index].get('src', False):
            continue
        link_path = handle_css_of_js_path(scripts[index]['src'])
        path = file_path + '/' + link_path

        if os.path.exists(path):
            with open(path, 'r') as fp:
                version = hashlib.md5(fp.read().encode("UTF-8")).hexdigest()[8: -8]
                scripts[index]['src'] = link_path + '?v=' + version

    return str(soup)


def hash_css_and_js_version(html_str, file_path, data):
    """
    hash静态资源
    :param html_str: html代码
    :return:
    """
    soup = BeautifulSoup(html_str, "html.parser")
    links = soup.find_all("link")
    for index, _ in enumerate(links):
        if 'href' not in links[index]:
            continue
        link_path = handle_css_of_js_path(links[index]['href'])
        path = file_path + '/' + link_path
        if os.path.exists(path):
            with open(path, 'r') as fp:
                version = hashlib.md5(fp.read().encode("UTF-8")).hexdigest()
                static_path = data['hash_static_path'] + '/' + str_to_file_path(version, 8) + '.min.css'
                tools.output_file(static_path, fp.read())
                links[index]['href'] = data['hash_static_path_prefix'] + '/' + str_to_file_path(version, 8) + '.min.css'

    scripts = soup.find_all("script")

    for index, _ in enumerate(scripts):

        if not scripts[index].get('src', False):
            continue
        link_path = handle_css_of_js_path(scripts[index]['src'])
        path = file_path + '/' + link_path

        if os.path.exists(path):
            with open(path, 'r') as fp:
                version = hashlib.md5(fp.read().encode("UTF-8")).hexdigest()
                static_path = data['hash_static_path'] + '/' + str_to_file_path(version, 8) + '.min.js'
                tools.output_file(static_path, fp.read())
                scripts[index]['src'] = data['hash_static_path_prefix'] + '/' + str_to_file_path(version, 8) + '.min.js'

    return str(soup)


def handle_html_code(html_str, file_path):
    """
    引入代码片段
    :param html_str: html代码
    :param file_path: 当前文件路径
    :return:
    """
    soup = BeautifulSoup(html_str, "html.parser")
    links = soup.find_all("import")
    for index, _ in enumerate(links):
        link_path = handle_css_of_js_path(links[index]['href'])
        path = file_path + '/' + link_path
        if os.path.exists(path):
            with open(path, 'r') as fp:
                links[index].replace_with(BeautifulSoup(handle_html_code(fp.read(), os.path.dirname(path)), "html.parser"))

    return str(soup)


def build_html_use_template(html_str, file_path, data):
    """
    生成线上html代码
    :param html_str: html模板
    :return:
    """

    # 处理路径
    file_path = os.path.dirname(file_path)

    # 编译代码
    html_str = handle_html_code(html_str, file_path)

    # hash静态资源文件
    html_str = hash_css_and_js_version(html_str, file_path, data)

    # 压缩html
    html_str = handle_html(html_str)
    # 为生成的代码打标示
    html_str = tip.html_tip + html_str
    return html_str
