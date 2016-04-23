# coding:UTF-8


"""
这个文件是项目相关配置文件
"""

import os


# 这是一个文件夹路径，不需要斜杠结束，项目路径
project_path = os.path.dirname(os.path.dirname(__file__))

# 监控文件变化的文件夹
watch_path = project_path + '/demo'
