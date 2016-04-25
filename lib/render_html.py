# coding:UTF-8


"""
html预处理
@author: yubang
2016.04.24
"""


from bs4 import BeautifulSoup
from config import tip
from lib.static_minify import handle_html, handle_javascript
from lib import tools
import os
import hashlib


def get_the_file_all_use_file(input_file_path, output_file_path, project_path):
    """
    获取文件依赖的文件列表
    :param input_file_path: 输入文件地址
    :param output_file_path: 输出文件地址
    :param project_path: 项目路径
    :return:
    """
    if not os.path.exists(input_file_path):
        return {}

    input_file_path = os.path.realpath(input_file_path)

    use_files = {input_file_path: ''}
    output_path = os.path.dirname(output_file_path)
    with open(input_file_path, 'r') as fp:
        soup = BeautifulSoup(fp.read(), "html.parser")
        links = soup.find_all('link')
        for obj in links:
            if 'href' in obj.attrs:
                use_files[get_real_static_path(obj['href'], project_path, output_path)] = ''
        scripts = soup.find_all('script')
        for obj in scripts:
            if 'src' in obj.attrs:
                use_files[get_real_static_path(obj['src'], project_path, output_path)] = ''
        # 处理引入的html代码片段
        imports = soup.find_all('import')
        for obj in imports:
            if 'href' in obj.attrs:
                import_path = get_real_static_path(obj['href'], project_path, output_path)
                use_files[import_path] = ''
                d = get_the_file_all_use_file(import_path, output_file_path, project_path)
                use_files.update(d)
    return use_files


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


def get_real_static_path(static_href, project_path, output_path):
    """
    获取真实的静态文件路径
    :param static_href: 静态资源链接
    :param project_path: 项目路径
    :param output_path: 输出的html文件夹路径
    :return:
    """

    static_href = handle_css_of_js_path(static_href)

    if static_href[0] == '/' and static_href[1] != '/':
        # 绝对路径
        return os.path.realpath(project_path + static_href)
    elif static_href[0] != '/':
        # 相对路径
        return os.path.realpath(output_path + '/' + static_href)
    else:
        # cdn路径
        return None


def render_html_use_template(html_str, output_file_path, project_path, input_file_path):
    """
    渲染html代码
    :param html_str: html模板
    :param output_file_path: 输出的html文件路径
    :param project_path: 项目路径
    :return:
    """

    # 处理路径
    output_path = os.path.dirname(output_file_path)
    input_path = os.path.dirname(input_file_path)

    html_str = handle_html_code(html_str, input_path, project_path)
    html_str = handle_css_and_js_version(html_str, output_path, project_path)

    # 删除重复的css和js
    html_str = remove_repeat_link_and_script(html_str)

    html_str = handle_html(html_str)
    html_str = tip.html_tip + html_str
    return html_str


def handle_css_and_js_version(html_str, file_path, project_path):
    """
    为js和css打上版本号
    :param html_str: html代码
    :param project_path: 项目路径
    :return:
    """
    soup = BeautifulSoup(html_str, "html.parser")
    links = soup.find_all("link")

    for index, _ in enumerate(links):
        if 'href' not in links[index].attrs:
            continue
        link_path = handle_css_of_js_path(links[index]['href'])
        path = get_real_static_path(link_path, project_path, file_path)

        if path and os.path.exists(path):
            with open(path, 'r') as fp:
                version = hashlib.md5(fp.read().encode("UTF-8")).hexdigest()[8: -8]
                links[index]['href'] = link_path + '?v=' + version

    scripts = soup.find_all("script")

    for index, _ in enumerate(scripts):

        if not scripts[index].get('src', False):
            continue
        link_path = handle_css_of_js_path(scripts[index]['src'])
        path = get_real_static_path(link_path, project_path, file_path)

        if path and os.path.exists(path):
            with open(path, 'r') as fp:
                version = hashlib.md5(fp.read().encode("UTF-8")).hexdigest()[8: -8]
                scripts[index]['src'] = link_path + '?v=' + version

    return str(soup)


def hash_css_and_js_version(html_str, file_path, data, project_path):
    """
    hash静态资源
    :param html_str: html代码
    :return:
    """
    soup = BeautifulSoup(html_str, "html.parser")
    links = soup.find_all("link")
    for index, _ in enumerate(links):
        if 'href' not in links[index].attrs:
            continue
        link_path = handle_css_of_js_path(links[index]['href'])
        path = get_real_static_path(link_path, project_path, file_path)
        if path and os.path.exists(path):
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
        path = get_real_static_path(link_path, project_path, file_path)

        if path and os.path.exists(path):
            with open(path, 'r') as fp:
                version = hashlib.md5(fp.read().encode("UTF-8")).hexdigest()
                static_path = data['hash_static_path'] + '/' + str_to_file_path(version, 8) + '.min.js'
                tools.output_file(static_path, fp.read())
                scripts[index]['src'] = data['hash_static_path_prefix'] + '/' + str_to_file_path(version, 8) + '.min.js'

    return str(soup)


def handle_html_code(html_str, file_path, project_path):
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
        path = get_real_static_path(link_path, project_path, file_path)
        if path and os.path.exists(path):
            with open(path, 'r') as fp:
                links[index].replace_with(BeautifulSoup(handle_html_code(fp.read(), os.path.dirname(path), project_path), "html.parser"))

    return str(soup)


def separate_style(html_str, data):
    """
    分离css
    :param html_str: html代码
    :return:
    """
    css_index = 0
    css_data = ''
    soup = BeautifulSoup(html_str, "html.parser")

    styles = soup.find_all("style")
    for obj in styles:
        css_data += ('\n' + obj.string)

    objs = soup.find_all(True)
    for index, _ in enumerate(objs):
        obj = objs[index]
        style_text = obj.get('style', None)
        if style_text:
            css_data += ('\n' + ".modular_front_css_%d{%s}" % (css_index, style_text))
            if 'class' not in obj.attrs:
                obj.attrs['class'] = []
            obj.attrs['class'].append(("modular_front_css_%d" % css_index))
            del obj['style']
            css_index += 1

    # 写入分离出的css文件
    version = hashlib.md5(css_data.encode("UTF-8")).hexdigest()
    file_path = data['tools_obtain_static_path'] + '/' + str_to_file_path(version, 8) + '.min.css'

    tools.output_file(file_path, css_data)

    link_str = '<link rel="stylesheet" href="%s" />' % (data['tools_obtain_static_path_prefix'] + '/' + str_to_file_path(version, 8) + '.min.css')
    soup.find('head').append(BeautifulSoup(link_str, "html.parser"))

    return str(soup)


def separate_javascript(html_str, data):
    """
    分离js
    :param html_str: html代码
    :return:
    """
    js_data = ''
    soup = BeautifulSoup(html_str, "html.parser")

    scripts = soup.find_all("script")
    for obj in scripts:
        if obj.string and obj.string.strip():
            js_data += ('\n' + obj.string)
            obj.string = ''

    if not js_data:
        return html_str

    # 压缩js
    js_data = handle_javascript(js_data, False, False)

    # 写入分离出的js文件
    version = hashlib.md5(js_data.encode("UTF-8")).hexdigest()
    file_path = data['tools_obtain_static_path'] + '/' + str_to_file_path(version, 8) + '.min.js'

    tools.output_file(file_path, js_data)

    link_str = '<script src="%s"></script>' % (data['tools_obtain_static_path_prefix'] + '/' + str_to_file_path(version, 8) + '.min.js')
    soup.find('body').append(BeautifulSoup(link_str, "html.parser"))

    return str(soup)


def build_html_use_template(html_str, input_path, project_path, file_path, data):
    """
    生成线上html代码
    :param html_str: html模板
    :param project_path: 项目路径
    :return:
    """

    # 处理路径
    file_path = os.path.dirname(file_path)
    input_path = os.path.dirname(input_path)

    # 编译代码
    html_str = handle_html_code(html_str, input_path, project_path)

    # hash静态资源文件
    html_str = hash_css_and_js_version(html_str, file_path, data, project_path)

    # 分离静态资源
    html_str = separate_style(html_str, data)
    html_str = separate_javascript(html_str, data)

    # 删除重复的css和js
    html_str = remove_repeat_link_and_script(html_str)

    # 压缩html
    html_str = handle_html(html_str)
    # 为生成的代码打标示
    html_str = tip.html_tip + html_str
    return html_str


def remove_repeat_link_and_script(html_str):
    """
    删除重复的link和script
    :param html_str: html字符串
    :return:
    """
    labels = {}
    soup = BeautifulSoup(html_str, "html.parser")

    links = soup.find_all('link')

    for index, obj in enumerate(links):
        if not obj.attrs:
            links[index].decompose()
            continue
        if 'href' in obj.attrs:
            if obj['href'] in labels:
                links[index].decompose()
            else:
                labels[obj['href']] = ''
    scripts = soup.find_all('script')

    for index, obj in enumerate(scripts):
        if 'src' in obj.attrs:
            if obj['src'] in labels:
                scripts[index].decompose()
            else:
                labels[obj['src']] = ''
    return str(soup)
