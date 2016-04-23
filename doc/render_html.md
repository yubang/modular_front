# html预编译

本工具支持html预编译，只需要编写规则，规则文件需要放在工具的rule目录下的任意子文件夹内。内容如下：
    # 渲染html

    rule: render_html
    source_path: demo/html
    target_path: demo/

demo/html改成要压缩的文件所在文件夹路径（相对路径），这目录下所有.html都会处理。demo是要输出压缩的文件夹路径（相对路径）。


*预编译的html会发生什么事情呢？*
- 自动为引入的js和css打上版本号（只为本地引用打版本号，样式为?v=16位文件md5）
- 支持import标签，引入href属性指定的文件，注意该路径是相对于import标签编写文件的路径。（例子 <import href="1.htm" />）
- 压缩html文件
