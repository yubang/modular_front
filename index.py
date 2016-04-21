# coding:UTF-8


"""
前端模块化小工具，目标人群是0基础的前端和后台
@author： yubang
2016.04.20
"""


from script import v1
from config import project


def test():

    # project_path = input("请输入项目路径：")
    # if not os.path.exists(project_path):
    #     exit("项目路径不存在")
    #
    # v1.init({"project_path": project_path})

    v1.start_monitor({"project_path": project.project_path, 'watch_path': project.watch_path})

    print("ok")


if __name__ == '__main__':
    test()
