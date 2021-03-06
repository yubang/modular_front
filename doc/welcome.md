# 欢迎使用前端模块化小工具

*为什么我要制作这样的一个小工具呢，现在市面上不是有一大堆这样子的工具了么，何苦要自己造轮子呢？*

**因为现在主流的前端打包工具都是基于nodejs制作的，js博大精深，本人还没有能力去阅读工具的源码来修改成适合自己项目的小工具。另一个原因是，这些主流工具入门门槛比较高，对于一个没多少技术积累的团队来说，需要太多时间去适应。**

这个小轮子的目标：

1. 让使用者30分钟内就可以上手该工具

2. 旧项目也可以无缝接入该工具

3. 不影响自己的开发模式

4. 跨平台使用，能够在win，linux，mac下工作

5. 能够解决项目文件混乱的问题

这个小轮子的v1版功能：
- 打包组件
- 合并html，css，js文件
- 压缩混淆js文件
- 简单html生成（静态使用hash作为版本发布，分离写在html的css和js）
- 预编译scss，less

**为什么前端需要模块化？**

因为如果我们还是用以前那种后台mvc开发模式，后台生成html输出到浏览器。对前端小伙伴来说，还要学习后台的模板语言，还需要搭建后台开发环境，这简直是灾难。

这个时候前后端分离就很迫切需要了，前后端分离第一步，前端写html页面，通过ajax与后台交换数据，后台只输出ajax数据。这个时候前端需要写大量的dom操作，所以前端框架应运而生，各种前端模板引擎出现了。

然而单纯的前端框架无法解决页面重复内容重复利用的问题，前端发展到后期必定是页面由一个又一个的组件构造而成，并且各种js，css按需打包合并引入。

##### 本工具无法解决以上全部问题，只为了简单实现一下前端模块化。

使用文档：
- [安装工具](https://github.com/yubang/modular_front/blob/master/doc/install.md "安装工具")
- [组件打包](https://github.com/yubang/modular_front/blob/master/doc/component.md "组件打包")
- [合并静态资源](https://github.com/yubang/modular_front/blob/master/doc/merge.md "合并静态资源")
- [压缩静态资源](https://github.com/yubang/modular_front/blob/master/doc/minify.md "压缩静态资源")
- [css预编译](https://github.com/yubang/modular_front/blob/master/doc/precompiled.md "css预编译")
- [css预编译与压缩](https://github.com/yubang/modular_front/blob/master/doc/precompiled_and_merge.md "css预编译与压缩")
- [html预编译](https://github.com/yubang/modular_front/blob/master/doc/render_html.md "html预编译")