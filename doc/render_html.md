# html预编译

本工具支持html预编译，只需要编写规则，规则文件需要放在工具的rule目录下的任意子文件夹内。内容如下：

    # 渲染html

    rule: render_html
    source_path: demo/html
    target_path: demo/


    # 提取的静态资源文件存放路径
    tools_obtain_static_path: demo/obtain

    # 提取的静态文件存放路径前缀
    tools_obtain_static_path_prefix: /demo/hash

    # hash掉的静态文件存放路径
    hash_static_path: demo/hash

    # hash掉的静态文件存放路径前缀
    hash_static_path_prefix: /demo/hash


demo/html改成要压缩的文件所在文件夹路径（相对路径），这目录下所有.html都会处理。demo是要输出压缩的文件夹路径（相对路径）。


*如何编译线上用的版本呢？（分离html里面的css和js，引用的静态资源hash化文件名）*
运行：python index.py build_html


*预编译的html会发生什么事情呢？*
- 自动为引入的js和css打上版本号（只为本地引用打版本号，样式为?v=16位文件md5）
- 支持import标签，引入href属性指定的文件，注意该路径是相对于import标签编写文件的路径。（例子 `<import href="1.htm" />`）
- 压缩html文件
- 支持分离写在html页面的js和css（标签上的style也会分离喔）
- 支持引用的js和css文件名变成内容hash值（防止传统的更新文件采取覆盖旧文件，打版本号更新不一致问题，具体参考[这里](http://www.infoq.com/cn/articles/front-end-engineering-and-performance-optimization-part1 "这里")的基于hash更新原因）
