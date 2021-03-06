# coding:UTF-8


"""
杂七杂八的小工具
"""


from lib.log_lib import log
import os


def output_file(file_path, fp_data, write_type='w'):
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    log.info('写入文件：%s' % file_path)
    with open(file_path, write_type) as fp:
        fp.write(fp_data)


def get_file_type(file_path):
    """
    获取文件类型
    :param file_path: 文件路径
    :return:
    """
    t = file_path.split('.')
    if len(t) <= 1:
        return None
    else:
        return t[-1:][0]


def get_all_file_path_in_dir(dir_path):
    """
    获取目录下所有文件名字
    :param dir_path:
    :return:
    """
    fps = {}

    if os.path.isdir(dir_path):
        objs = os.listdir(dir_path)
        for obj in objs:
            d = get_all_file_path_in_dir(dir_path + '/' + obj)
            fps.update(d)
    else:
        fps[os.path.realpath(dir_path)] = ''

    return fps
