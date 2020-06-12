# Smart Code Copier


## 简介
Smart Code Copier是一个好用的源码拷贝工具，提供功能：
- tab转空格
- gb2312编码转utf-8
- 去掉行尾空白字符
- 统一单个文件内换行符

当需要把多个文件按上述编码风格统一配置时，尽管有`.editorconfig`工具可用，但它似乎对已有源码文件并不生效，此时可以使用本工具执行转换。

提供功能：
- 单个文件的转换
- 整个目录的转换
- 指定`\t`对齐到的空格长度

## 注意
如果你的源文件是UTF-8编码、中文显示正确、仅需要替换`\t`为空格、处于Linux环境下，则可直接使用`expand`命令。例如：
```bash
expand -t 4 compute_flops_tf_pb.py > compute_flops_tf_pb_new.py
```

## 协议
MIT
