# coding: utf-8

__author__ = 'Zhuo Zhang'
__date__ = '2020-06-04'
__version__ = '0.1'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020, Zhuo Zhang'

"""
Smart Code Copier简介：

在阅读和使用 祖传/github/各种博客 上的代码时，会遇到：
- 没有使用空格缩进，使用了tab（`\t`）缩进
- 或者，混合使用了空格和`\t`
- 文件中有中文，并且没有使用utf-8编码
- 行尾有多余的空格、tab字符
- Linux/Windows换行符混用：单个文件中同时出现了两种换行符

个人认为好的编码格式应该是：
- 统一用空格缩进而不是tab
- 文件用utf-8编码
- 统一的换行符（平台相关）

本项目提供了智能的：
- 单个源码文件拷贝功能，smart_copy_source_file()
- 指定源码目录的拷贝功能，smart_copy_source_folder()

NOTE: 
- 你可能需要手动处理二进制文件
- 暂时不支持.editorconfig的解析
"""

import chardet
import os

def tab_to_spaces(src_pth, dst_pth='output.c', tab_size=4):
    """
    文件复制，写入时把\t字符转为合适的空格数量
    以tab_size=4为例，并不是说把\t转为4个空格，而是说如果当前不是4字符数量则追加直到4的倍数，
    如果已经是4的倍数个字符则增加4个字符

    NOTE: 中文编码并不会做转换
    """
    fin = open(src_pth)
    fout = open(dst_pth, 'w')

    for line_num, line_content in enumerate(fin.readlines()):
        line_content = line_content.rstrip()
        if '\t' in line_content:
            line_content = reformat_str(line_content, tab_size)
        fout.write(line_content+'\n')

    fin.close()
    fout.close()

def tab_to_spaces_utf8(src_pth, dst_pth='output.c', tab_size=4):
    """
    文件复制，写入时把\t字符转为合适的空格数量，并且把文件按utf-8编码保存，包括中文转换。
    以tab_size=4为例，并不是说把\t转为4个空格，而是说如果当前不是4字符数量则追加直到4的倍数，
    如果已经是4的倍数个字符则增加4个字符
    """
    codec_desc = check_codec(src_pth)
    if codec_desc['confidence'] < 0.99:
        print('Error! Failed to guess the codec of file ' + src_pth + ', please manually check!')
        return

    encoding = codec_desc['encoding'].lower() #e.g. gb2312, utf-8

    fin = open(src_pth, encoding=encoding)
    fout = open(dst_pth, 'w', encoding='utf-8')

    for line_num, line_content in enumerate(fin.readlines()):
        line_content = line_content.rstrip()
        if '\t' in line_content:
            line_content = reformat_str(line_content, tab_size)
        line_content = str(line_content.encode('utf-8'), encoding='utf-8')
        fout.write(line_content+'\n')

    fin.close()
    fout.close()


def smart_copy_source_file(src_pth, dst_pth, tab_size):
    tab_to_spaces_utf8(src_pth, dst_pth, tab_size)

def test():
    s = ' *	r		g		b'
    for i, c in enumerate(s):
        if c=='\t':
            co ='[tab]'
        elif c==' ':
            co = '[space]'
        else:
            co = c
        print(co)

def align_up(x, n):
    """向上取整"""
    return ((x+n-1)//n)*n

def reformat_str(s, tab_size=4):
    #s = ' *	r		g		b'
    pos = 0
    res = ''
    for c in s:
        if c=='\t':
            aligned = align_up(pos, tab_size)
            if pos%4!=0:
                num_spaces = aligned - pos
            else:
                num_spaces = tab_size
            co = ' ' * num_spaces
            pos += num_spaces
        else:
            co = c
            pos += 1
        res = res + co
    return res

def str_to_utf8(src_pth, dst_pth='output.c'):
    """
    拷贝文件，写入时保存为utf-8编码
    
    首先猜测源文件编码encoding，根据encoding打开源文件
    保存的文件是用utf-8编码打开和写入的
    python3里的str转utf-8编码的str：
        line = str(line.encode('utf-8'), encoding="utf-8")
    """
    codec_desc = check_codec(src_pth)
    if codec_desc['confidence'] < 0.99:
        print('Error! Failed to guess the codec of file ' + src_pth + ', please manually check!')
        return

    encoding = codec_desc['encoding'].lower() #e.g. gb2312, utf-8

    fin = open(src_pth, encoding=encoding)
    fout = open(dst_pth, 'w', encoding='utf-8')

    for line in fin.readlines():
        line = line.rstrip()
        line = str(line.encode('utf-8'), encoding="utf-8")
        fout.write(line + '\n')

    fin.close()
    fout.close()

def check_codec(file_pth):
    """
    二进制方式读取文件的若干内容，猜测出它的编码
    NOTE： 如果文件过大，读取整个文件可能比较耗时甚至内存不足
    NOTE： 如果读取的内容过少以至于没读取到包含中文的部分，则返回ASCII编码这一错误结果
    """
    #filePath = unicode(filePath,'utf8')
    file_size = os.path.getsize(file_pth)

    #BLOCK_SIZE = 1048576  # or some other, desired size in bytes
    BLOCK_SIZE = file_size
    #print('file_size = ', file_size)
    # 判断文件的编码格式
    with open(file_pth, "rb") as f:
        data = f.read(BLOCK_SIZE)
        res = chardet.detect(data) # a dict
        #print(res)
        return res

def smart_copy_source_folder(src_dir, dst_dir, ext_and_tab_cfg):
    for item in os.listdir(src_dir):
        ext = item.split('.')[-1]
        if (item=='CMakeLists.txt'):
            ext = item
        tab_size = ext_and_tab_cfg.get(ext, 4) # if not specified, use 4 spaces
        print('processing ' + item)
        src_pth = src_dir + '/' + item
        dst_pth = dst_dir + '/' + item
        smart_copy_source_file(src_pth, dst_pth, tab_size)


def example_copy_file():
    src_dir = r'E:/share/from_qiuhan/20200603-颜色格式相关/各种颜色格式双向转换/colortrans'
    # src_pth = src_dir + '/' + 'lirgb_yuv.c'
    # src_pth = src_dir + '/' + 'litrimfun.h'
    src_pth = src_dir + '/' + 'test.c'
    tab_size = 4
    smart_copy_source_file(src_pth, 'output.c', tab_size)

def example_copy_folder():
    src_dir = 'E:/share/from_qiuhan/20200603-颜色格式相关/各种颜色格式双向转换/colortrans'
    dst_dir = 'E:/dbg/zz/cvfmt/temp'
    cfg = {
        '.c': 4,
        '.h': 4,
        '.py': 4,
        'CMakeLists.txt': 2,
        '.cmake': 2
    }
    smart_copy_source_folder(src_dir, dst_dir, cfg)

def example_copy_folder_by_editorconfig():
    """
    TODO: 解析editorconfig然后执行智能的拷贝
    """
    pass

if __name__ == '__main__':
    example_copy_file()
    example_copy_folder()