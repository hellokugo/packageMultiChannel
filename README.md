# 使用说明

github clone下来的文件有三个，分别是local_tool、src和readme，其中local_tool是已经打包好的包含可运行的exe文件（双击目录下的local_tool.exe），src是python源码，供按需定制并重新生成exe。

src要生成exe可执行文件电脑必须安装好pyqt的相关环境，在确认安装好环境下直接在命令行输入pyinstaller -w /src/script/local_tool.py即可看到生成dist文件，里面就是包含可执行的exe文件，这里的-w参数主要是禁止在执行exe文件时弹出cmd窗口。注意的是，由于在运行过程中需要一些额外的辅助文件，而在生成exe过程中并没有把这些文件拷贝到dist目录下，所以这里需要手动做拷贝，不然会运行不成功。主要拷贝的是scripts同级目录下的 extra和plugins文件夹。

***注意：生成的dist目录下会有plugins目录，但是我们还是要对他做拷贝，因为对比发现，生成的plugins会比提供的plugins少了文件，这里面是python自带的一些库，如果这个些库已经配到电脑的环境变量中，则可以不做拷贝。但是为了保险起见，还是希望原封不动的把plugins拷贝到最终的dist目录下，例子请看local_tool***

[参考介绍](https://hellokugo.github.io/2016/11/06/Android%E5%A4%9A%E6%B8%A0%E9%81%93%E5%8C%85%E5%A4%84%E7%90%86/)

