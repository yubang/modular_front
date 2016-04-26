# 组件打包

*为何要打包组件呢？*
很明显是要重复使用某一段代码片段啦，但是如果直接import的话，后台模板引擎很容易实现，但是前端该怎么办呢？本工具的解决办法是把组件打包成一个js，只需要引入js调用一个函数就好。

##### 第一步
组件准备，首先建立一个文件夹，里面必须有一个叫做c.yaml的文件，用于配置组件的相关信息。文件内容如下：

     # 组件说明
     # name关键字是必须的
     name: beta

beta改成自己组件的名字（随意但是有意义点，请用英文）

然后在这个文件夹里面放入三种类型文件（.html，.css.，js），这三种文件可以随意命名，并且可以在在这个文件夹下任意子文件夹，，文件可以任意多个。

##### 第二步
编写规则文件，规则文件需要放在工具的rule目录下的任意子文件夹内。内容如下：
    # 这是一个打包组件的规则文件
    
    rule: make_component
    source_path: cc
    target_path: out/c.js

cc改成组件文件夹路径，请注意该路径与config/project.py配置的项目路径是拼接成组件所在文件夹路径的，算是相对路径。

out/c.js是组件打包生成的js存放路径，也是相对路径。

**其实这样子，工具就会自动打包了，但是编写组件要需要约束的地方**

- 组件的js源文件的函数不能被直接调用，如果想被调用请写成this.方法名 = function(XXX，【xxx】){XXX}

- 组件的js调用写了this之后也是不能直接调用了，因为防止组件之间代码冲突工具自动把函数包起来了，调用的时候需要用component_XXX.方法 这样子来调用。XXX是组件配置时候写的名字

- 组件的js需要提供一个this.component_init = function(data, func){}的方法，用于组件挂载到页面之后回调，初始化方法请写在这里。

- 挂载组件的时候使用component_XXX.build_component('demo_1', {}, function(){}); demo_1改成要挂载到的元素的id

**如何使用打包的组件**
```html
<script src="./out/c/main.js"></script>
<script>
    component_beta.build_component('demo_1', {}, function(){});
</script>
```
引入js，调用build_component方法。component_beta改成component_你的组件名字，demo_1改成组件要放置的元素id，第二个参数为一个自定义参数，第三个参数为回调函数，就如此简单。