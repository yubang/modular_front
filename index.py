# coding:UTF-8


"""
前端模块化小工具，目标人群是0基础的前端和后台
@author： yubang
2016.04.20
"""


from script import v1
from config import project
import sys


def test():

    # project_path = input("请输入项目路径：")
    # if not os.path.exists(project_path):
    #     exit("项目路径不存在")
    #
    # v1.init({"project_path": project_path})

    argv = {"project_path": project.project_path, 'watch_path': project.watch_path}

    if len(sys.argv) == 2:
        if sys.argv[1] == 'build_html':
            print("编译html文件开始")
            v1.read_all_rule_in_build_html('./rule', argv)
            print("编译html文件结束")
        else:
            print("命令有误！")
        return

    v1.start_monitor(argv)

    print("ok")


if __name__ == '__main__':
    test()
