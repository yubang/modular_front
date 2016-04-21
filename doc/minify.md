# 静态资源压缩

*为何要压缩静态资源，因为带宽好重要～*


本工具压缩静态资源很简单，只需要编写规则，规则文件需要放在工具的rule目录下的任意子文件夹内。内容如下：
    # 压缩文件例子

    rule: minify
    source_path: demo/in/max
    target_path: demo/out/min
    encryption: True

demo/in/max改成要压缩的文件所在文件夹路径（相对路径），这目录下所有文件都会处理。demo/out/min是要输出压缩的文件夹路径（相对路径）。encryption是是否加密混淆js文件

注意如果混淆了js，你需要暴露的方法必须使用this.方法名暴露，不然无法正常调用
