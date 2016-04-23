# css预编译与合并（就是合并多个预编译文件，并且编译成css）

*为何要预编译，重复的东西定义变量，以后修改一个地方就好*


本工具支持css预编译（只支持scss和less），只需要编写规则，规则文件需要放在工具的rule目录下的任意子文件夹内。内容如下：
    # 编译并合并css

    rule: css_precompiled_and_merge
    source_path: demo/pre/in2
    target_path: demo/pre/out2/1.css

    # 编译方式（scss或则less）
    compiled_type: scss

	# 是否先编译再合并
    compiled_first: False

demo/pre/in2改成要压缩的文件所在文件夹路径（相对路径），这目录下所有.less和.scss都会处理。demo/pre/out2/1.css是要输出压缩的文件（相对路径）。

