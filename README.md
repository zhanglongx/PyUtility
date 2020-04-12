# PyUtility

Utilities written in Python.

## Description

* achieve.py: archive packaging tool.

* baidu_compare.py: comparison tool for BaiduNetDisk. Compare the difference between NetDisk and local directory. Only compare file name, no comparison between file content, checksum, file size etc.

* chwindir.py: convert a Windows absolute path into Linux absolute path. E.g. path1\path2 -> path1/path2. This is especially useful in WSL(Windows Subsystem Linux).

* dep_counter.py: Count missing people by name.

* kill_git.py: kill TotosiseGit/SVN background caching process. Mainly used to clean up icon overlay issue of TortoiseGit/SVN.

* overlay.py: Fix the icon overlay problem under Windows.

* summary.py: summary peoples' rating.

## Run

Every script can be run through python. 

## Python3

All tools support Python3, and not tested under Python2.

## License

GNU GPL v3

# PyUtility

以Python编写的工具合集。

## 模块说明

* achieve.py：存档打包工具。

* baidu_compare.py：百度云盘比较工具。比较云盘目录（通过读取本地百度网盘数据库）和本地目录的差别。比较内容只支持文件名，不比较文件内容、校验和、文件大小等项。

* chwindir.py：将Windows路径转化为Linux路径，例如：path1\path2\ -> path1/path2。该命令在WSL(Windows Subsystem Linux)下特别有用。

* dep_counter.py：按人名统计缺失的人。

* kill_git.py：执行后，会杀掉Windows下的TortoiseGit/SVN客户端后台程序。主要用于清理TortoiseGit/SVN的图标叠加。

* overlay.py：在Windows下通过修改注册表，修正图标叠加问题。

* summary.py：按人统计分数。

## 运行方法

大部分程序可以直接通过python运行。

## Python3

大部分程序支持Python3，没有特别地对Python2进行测试。

## 使用授权

GNU GPL v3
