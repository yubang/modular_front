# 小工具安装篇

**环境准备**
python3.4+（做工具的时候就没想过去适应python2，望见谅）
pip（python的包管理工具）

**工具下载**
- git clone git@github.com:yubang/modular_front.git
- wget https://github.com/yubang/modular_front/archive/master.zip

**工具配置**
当我们下载好小工具之后，请解压到一个目录（非常不建议路径带有中文，我没测试过中文路径的情况）

然后进入工具文件夹，执行pip install -r requirements.txt 安装好必须的依赖

然后修改config目录下的project.py文件，里面的project_path填写项目路径用于后面配置处理规则的根目录，watch_path设置为需要监视文件变化触发编译的目录路径（全路径，为了减轻文件读写次数，请合理设置）

然后修改好信息之后，运行python index.py即可。

**工具文件夹说明**
- config：小工具配置文件夹
- demo：制作小工具时的测试例子
- doc：帮助手册
- lib：工具类库
- log：工具的日志
- rule：规则文件（这个文件夹需要自己防止规则文件以便实现各种功能）
- script： 工具的启动脚本（请勿直接运行）
