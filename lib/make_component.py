# coding:UTF-8


"""
制作小组件
@author: yubang
2016.04.20
"""


from lib.merge_file import get_after_merge_file_str
from lib.all_to_js import build_js_data
import yaml


def get_component_js_str(dir_path):
    """
    获取打包好的组件js文件
    :param dir_path: 组件代码文件夹路径
    :return: str
    """
    html = get_after_merge_file_str(dir_path, file_type=r'\.html$', minify_type='html')
    css = get_after_merge_file_str(dir_path, file_type=r'\.css$', minify_type='css')
    js = get_after_merge_file_str(dir_path, file_type=r'\.js$', minify_type='js')

    html_js_str, html_js_name = build_js_data(html, 'tools_html')
    css_js_str, css_js_name = build_js_data(css, 'tools_css')

    # 读取组件配置
    with open(dir_path+'/c.yaml', 'r') as fp:
        fp_data = fp.read()
        component_config = yaml.load(fp_data)

    component_js = """
        // 该组件由modular_front打包生成，具体请查看：https://github.com/yubang/modular_front
        var component_%s = function(){
            %s
            %s
            %s
            this.build_component = function(dom_id){
              document.getElementById(dom_id).innerHTML = tools_html + '\n' + tools_css;
              component_init();
            }

            return this;
        }
    """ % (component_config['name'], html_js_str, css_js_str, js)

    return component_js
