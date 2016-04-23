# css预编译

*为何要预编译，重复的东西定义变量，以后修改一个地方就好*


本工具支持css预编译（只支持scss和less），只需要编写规则，规则文件需要放在工具的rule目录下的任意子文件夹内。内容如下：
    # 预编译css

    rule: css_precompiled
    source_path: demo/pre/in
    target_path: demo/pre/out

demo/pre/in改成要压缩的文件所在文件夹路径（相对路径），这目录下所有.less和.scss都会处理。demo/pre/out是要输出压缩的文件夹路径（相对路径）。

