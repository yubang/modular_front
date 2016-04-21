# 静态资源合并

*为何要合并静态资源，因为带宽好重要～，现在只支持html，css，js的合并，减少http请求可以加快访问*


本工具合并静态资源很简单，只需要编写规则，规则文件需要放在工具的rule目录下的任意子文件夹内。内容如下：
    # 合并文件规则

    rule: merge
    source_path: ./demo/in/m
    target_path: ./demo/out/m/main.js

    # 压缩方式（html, css， js）
    minify: js

    # 是否混淆js
    encryption: True

./demo/in/m改成要压缩的文件所在文件夹路径（相对路径），这目录下所有文件都会处理。./demo/out/m/main.js是要输出合并后的文件（相对路径）。encryption是是否加密混淆js文件

minify是合并方式，暂时只支持html，css和js

注意如果混淆了js，你需要暴露的方法必须使用this.方法名暴露，不然无法正常调用
