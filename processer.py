# encoding: utf-8
import zipfile
import os
import sys
import shutil
import base64
from docx.shared import Cm
from docx import Document
from lxml import etree
import urllib.request


WHERE_SCRIPT = os.path.split(os.path.realpath(__file__))[0]


def unzip(file_name):
    """
    解压指定文件
    :param file_name: 需解压的文件名
    :return: 解压后的文件夹路径
    """
    zip_file = zipfile.ZipFile(file_name)
    if os.path.isdir(file_name + "_files"):
        shutil.rmtree(file_name + "_files")
    else:
        os.mkdir(file_name + "_files")
    for names in zip_file.namelist():
        zip_file.extract(names, file_name + "_files/")
    zip_file.close()
    return file_name + "_files"


def zipDir(dirpath, outFullName):
    """
    压缩指定文件夹
    :param dirpath: 目标文件夹路径
    :param outFullName: 压缩文件保存路径
    :return: 无
    """
    zip_file = zipfile.ZipFile(outFullName, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去除目标与路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(dirpath, '')

        for filename in filenames:
            zip_file.write(os.path.join(path, filename),
                           os.path.join(fpath, filename))
    zip_file.close()


def download(url, file_name):
    """
    下载文件
    :param url: 下载链接
    :param file_name: 下载后保存的文件名
    :return: 无
    """
    if not os.path.exists(file_name):
        print("Downloading %s to %s..." % (url, file_name))
        f = open(file_name, 'wb')
        f.write(urllib.request.urlopen(url).read())
        f.close()
    else:
        print("Already exists: %s, skip." % file_name)


def add_cover_image(filepath):
    '''
    添加校徽与校名图片
    :param file: 目标文件路径
    :return: 无
    '''

    print("Adding cover image...")
    doc = Document(filepath)
    paragraphs = doc.paragraphs
    found_logo = False
    found_school_name = False
    for p in paragraphs:
        if(p.text == r"{{logo_image}}"):
            p.clear()
            r = p.add_run()
            r.add_picture(os.path.join(
                WHERE_SCRIPT, 'assets/logo_image.png'), width=Cm(5.45), height=Cm(5.45))
            found_logo = True
        elif(p.text == r"{{school_name_image}}"):
            p.clear()
            r = p.add_run()
            r.add_picture(os.path.join(
                WHERE_SCRIPT, 'assets/school_name_image.png'), width=Cm(11.43), height=Cm(1.91))
            found_school_name = True
        if(found_logo and found_school_name):
            break
    doc.save(filepath)
    print("Adding cover image done.")


def pandoc_process(*, source=os.path.join(WHERE_SCRIPT, 'demo/paper.md'),
                   output=os.path.join(WHERE_SCRIPT, 'build/pandoc_processed.docx')):
    '''
    将 Markdown 文档通过 Pandoc 转换成 Word 文档
    :return: os.system 包裹的 pandoc 命令，可取返回值
    '''
    pandoc_command = ('pandoc '
                      # 注意：每行后面必须加个空格
                      # docx 样式模板
                      + '--reference-doc "%s" ' % os.path.join(WHERE_SCRIPT, 'assets/template.docx')
                      + '-o "%s" ' % output  # 目标输出文件
                      + ('--metadata-file="%s" ' %
                         METADATA_FILE if METADATA_FILE is not None else '')  # 元数据文件

                      # 资源文件路径，默认与输入文件一致
                      + '--resource-path="%s" ' % os.path.dirname(source)
                      + '--highlight-style monochrome '  # 考虑到最后需要打印，选了个灰度的高亮风格
                      + '--filter pandoc-fignos '  # 图片自动编号
                      + '--filter pandoc-tablenos '  # 表格自动编号
                      # '--filter pandoc_eqnos '  # 公式自动编号，

                      # 2022年 3 月 31 日，个人测试 pandoc_eqnos 存在 bug，会导致生成的 docx 文件无法打开
                      # 开发者 nOkuda 提出了问题并提交了 PR，参见：https://github.com/tomduck/pandoc-eqnos/pull/64
                      # 我们会下载 https://raw.githubusercontent.com/nOkuda/pandoc-eqnos/docxOpen/pandoc_eqnos.py
                      # 并将 pandoc_eqnos.py 放置在本文件的同一层级目录下，并使用该文件作为 pandoc_qunos 的过滤器。
                      # 请关注 https://github.com/tomduck/pandoc-eqnos/pull/64 是否被合并、
                      # pandoc_eqnos 是否更新高于 2.5.0 的版本。若是、且想使用官方版本，
                      # 请：注释下一行，并取消上方“公式自动编号”行的注释。
                      + '--filter "%s" ' % os.path.join(WHERE_SCRIPT, 'pandoc_eqnos.py')

                      # 上面三个自动编号过滤器必须前置于我们的自定义过滤器与 --citeproc

                      # 自定义过滤器
                      + '--filter "%s" ' % os.path.join(WHERE_SCRIPT, 'filter.py')
                      + ('--bibliography "%s" ' %
                         BIBLIOGRAPHY if BIBLIOGRAPHY is not None else '')
                      + '--citeproc '  # 处理引用
                      # 引用格式，预处理时会自动下载
                      + '--csl "%s" ' % os.path.join(WHERE_SCRIPT, 'assets/chinese-gb7714-2005-numeric.csl')
                      + '--number-sections '  # 章节自动编号
                      + source)
    print("Using Pandoc to convert Markdown to Word...")
    print("Pandoc command: ")
    print(pandoc_command)
    print("Here goes with the Pandoc debug: ")
    return os.system(pandoc_command)


def document_process(dir_path):
    '''
    文档 后处理 流程。主要是 XML 操作。
    :param dir_path: 待处理的解压后的 docx 目录
    :return: 无
    '''
    tree = etree.parse(os.path.join(dir_path, 'word/document.xml'))
    root = tree.getroot()

    namespaces = root.nsmap

    body = root.find("w:body", namespaces)

    for p in body.findall("w:p", namespaces):
        pPr = p.find("w:pPr", namespaces)
        sectPr = pPr.findall("w:sectPr", namespaces)
        # 移除第一个分节符本身及其之前的全部内容
        if(not sectPr):
            body.remove(p)
        else:
            body.remove(p)
            break

    for p in body.findall("w:p", namespaces):
        # 处理 Pandoc 生成的 H1 编号为"第 x 章"，并将 tab 换成 空格
        for r in p.findall("w:r", namespaces):
            rpr = r.find("w:rPr", namespaces)
            if rpr is not None:
                rStyle = rpr.find("w:rStyle", namespaces)
                if rStyle is not None and rStyle.attrib.get("{%s}val" % namespaces["w"]) == "SectionNumber":
                    t = r.find("w:t", namespaces)
                    # H1 标号数字变 第 x 章
                    if len(t.text) == 1:
                        t.text = "第 %s 章" % t.text
                    # 章节标号后 Tab 换空格
                    maybeTab = r.getnext().find("w:tab", namespaces)
                    if maybeTab is not None:
                        r.getnext().remove(maybeTab)
                        space = etree.SubElement(
                            r.getnext(), "{%s}t" % namespaces["w"])
                        space.text = " "
                        space.set(
                            "{http://www.w3.org/XML/1998/namespace}space", "preserve")
            else:
                break

    tree.write(os.path.join(dir_path, 'word/document.xml'),
               encoding='utf-8', xml_declaration=True, standalone=True)


def modify_compress_punctuation(dir_path):
    '''
    后处理流程之二
    修改 Word 文档版式设定中的 字符间距控制 - 只压缩标点符号
    :param dir_path: 待处理的解压后的 docx 目录
    :return: 无
    '''
    tree = etree.parse(os.path.join(dir_path, 'word/settings.xml'))
    root = tree.getroot()

    namespaces = root.nsmap

    root.find("w:characterSpacingControl", namespaces).set(
        '{%s}val' % namespaces["w"], 'compressPunctuation')
    tree.write(os.path.join(dir_path, 'word/settings.xml'),
               encoding='utf-8', xml_declaration=True, standalone=True)


def pre_process():
    '''
    预处理流程
    预处理将会下载 cls 文件并生成模板 docx
    :return: 无
    '''
    print("Pre-processing...")
    # 创建 build
    if not os.path.exists(os.path.join(WHERE_SCRIPT, 'build')):
        os.mkdir(os.path.join(WHERE_SCRIPT, 'build'))
    # 创建 bin
    if not os.path.exists(os.path.join(WHERE_SCRIPT, 'bin')):
        os.mkdir(os.path.join(WHERE_SCRIPT, 'bin'))
    download("http://www.zotero.org/styles/chinese-gb7714-2005-numeric",
             os.path.join(WHERE_SCRIPT, 'assets/chinese-gb7714-2005-numeric.csl'))
    download("https://cdn.jsdelivr.net/gh/nOkuda/pandoc-eqnos@docxOpen/pandoc_eqnos.py",
             os.path.join(WHERE_SCRIPT, 'pandoc_eqnos.py'))
    if not os.path.exists(os.path.join(WHERE_SCRIPT, 'assets/template.docx')):
        zipDir(os.path.join(WHERE_SCRIPT, 'assets/template'),
               os.path.join(WHERE_SCRIPT, 'assets/template.docx'))
    else:
        print("Already exists: %s, skip." %
              os.path.join(WHERE_SCRIPT, 'assets/template.docx'))

    with open(os.path.join(WHERE_SCRIPT, 'assets/logo_image.b64'), 'r') as f:
        imgdata = base64.b64decode(f.read())
        file = open(os.path.join(WHERE_SCRIPT, 'assets/logo_image.png'), 'wb')
        file.write(imgdata)
        file.close()

    with open(os.path.join(WHERE_SCRIPT, 'assets/school_name_image.b64'), 'r') as f:
        imgdata = base64.b64decode(f.read())
        file = open(os.path.join(
            WHERE_SCRIPT, 'assets/school_name_image.png'), 'wb')
        file.write(imgdata)
        file.close()

    print("Pre-processing done.\n")


def post_process(*, source=os.path.join(WHERE_SCRIPT, 'build/pandoc_processed.docx'),
                 output=os.path.join(WHERE_SCRIPT, 'build/final.docx')):
    '''
    后处理将向过滤器输出的 docx 文件添加校徽与校名图片，并自动设置字符间距控制为
    “只压缩标点符号”，同时修改 Header 1 为“第 x 章”、替换 Header 后面的 Tab 为空格。

    部分后处理需要解压缩 docx 文件，大部分是 XML 操作，请参阅 [document_process()]
    :return: 无
    '''
    print("Post-processing...")
    add_cover_image(source)
    unzipped_dir_path = unzip(source)
    print(r"Removing first \newSectionInNewPage and previous contents...")
    document_process(unzipped_dir_path)
    print(r"Modifying document setting...")
    modify_compress_punctuation(unzipped_dir_path)
    if os.path.join(WHERE_SCRIPT, 'build/final.docx') == output:
        zipDir(unzipped_dir_path, output)
    else:
        zipDir(unzipped_dir_path, os.path.join(
            WHERE_SCRIPT, 'build/final.docx'))
        shutil.copy(os.path.join(WHERE_SCRIPT, 'build/final.docx'), output)
    zipDir(unzipped_dir_path, output)
    print("Post-processing done.")
    print("Output file: %s" % output)


def clean():
    '''
    清理工作
    :return: 无
    '''
    print("Cleaning...")
    if os.path.exists(os.path.join(WHERE_SCRIPT, 'build')):
        shutil.rmtree(os.path.join(WHERE_SCRIPT, 'build'))
    if os.path.exists(os.path.join(WHERE_SCRIPT, 'bin')):
        shutil.rmtree(os.path.join(WHERE_SCRIPT, 'bin'))
    if os.path.exists(os.path.join(WHERE_SCRIPT, 'pandoc_eqnos.py')):
        os.remove(os.path.join(WHERE_SCRIPT, 'pandoc_eqnos.py'))
    if os.path.exists(os.path.join(WHERE_SCRIPT, './assets/chinese-gb7714-2005-numeric.csl.py')):
        os.remove(os.path.join(WHERE_SCRIPT,
                  './assets/chinese-gb7714-2005-numeric.csl.py'))
    if os.path.exists(os.path.join(WHERE_SCRIPT, './assets/logo_image.png')):
        os.remove(os.path.join(WHERE_SCRIPT, './assets/logo_image.png'))
    if os.path.exists(os.path.join(WHERE_SCRIPT, './assets/school_name_image.png')):
        os.remove(os.path.join(WHERE_SCRIPT, './assets/school_name_image.png'))
    if os.path.exists(os.path.join(WHERE_SCRIPT, './assets/template.docx')):
        os.remove(os.path.join(WHERE_SCRIPT, './assets/template.docx'))
    print("Cleaning done.")


def print_helper():
    '''
    打印帮助文本
    '''
    print('''
process.py

--pre
\tPre processing only.
\t仅进行预处理。
\tPre processing will download the csl file and generate the template docx.
\t预处理将会下载 cls 文件并生成模板 docx。

--post
\tPost processing only.
\t仅进行后处理。
\tPost processing will add the logo and school name to the docx,
\tand automatically set compress punctuation, modify Header 1.
\t后处理将向过滤器输出的 docx 文件添加校徽与校名图片，并自动设置字符间距控制为
\t“只压缩标点符号”，同时修改 Header 1 为“第 x 章”、替换 Header 后面的 Tab 为空格。

-F\t--file
\tThe file which you want for pandoc convertation or post processing.
\t文件以供 Pandoc 转换或后处理。

-O\t--output
\tThe output file path which you want to save from pandoc convertation
\tor post processing.
\tPandoc 转换或后处理后文件的保存路径。

-M\t--metadata-file
\tThe metadata yaml file path which you want for pandoc convertation
\t用于 Pandoc 转换的 metadata 文件路径。

-B\t--bibliography
\tThe Bibtex format bibliography file path which you want for pandoc convertation
\t用于 Pandoc 转换的 Bibtex 格式参考文献文件路径。

--clean
\tClean the temporary files.
\t清理临时文件。

-H\t--help
\tPrint helper text.
\t打印帮助文本。
''')


if __name__ == '__main__':
    PRE_PROCESSING = False
    POST_PROCESSING = False
    FILE = None
    OUTPUT = None
    METADATA_FILE = None
    BIBLIOGRAPHY = None
    PANDOC_COMMAND = None

    for arg in sys.argv:
        if arg == '--pre':
            PRE_PROCESSING = True
        if arg == '--post':
            POST_PROCESSING = True
        if arg == '--clean':
            clean()
            sys.exit(0)
        if arg == '-H' or arg == '--help':
            print_helper()
            sys.exit(0)
        if arg == '-F' or arg == '--file':
            FILE = os.path.join(os.getcwd(),
                                sys.argv[sys.argv.index(arg) + 1])
        if arg == '-O' or arg == '--output':
            OUTPUT = os.path.join(os.getcwd(),
                                  sys.argv[sys.argv.index(arg) + 1])
        if arg == '-M' or arg == '--metadata-file':
            METADATA_FILE = os.path.join(os.getcwd(),
                                         sys.argv[sys.argv.index(arg) + 1])
        if arg == '-B' or arg == '--bibliography':
            BIBLIOGRAPHY = os.path.join(os.getcwd(),
                                        sys.argv[sys.argv.index(arg) + 1])
        if arg == '--overwrite-pandoc-command':
            PANDOC_COMMAND = sys.argv[sys.argv.index(arg) + 1]

    if PRE_PROCESSING:
        pre_process()
    elif POST_PROCESSING:
        post_process()
    elif PANDOC_COMMAND is not None:
        pre_process()
        print("Your Pandoc command: ")
        print(PANDOC_COMMAND)
        print("Here goes with the Pandoc debug: ")
        status = os.system(PANDOC_COMMAND)
        if (status == 0):
            print("Pandoc convertation done.\n")
            post_process(output=os.path.join(
                os.path.dirname(sys.argv[0]), OUTPUT))
        else:
            print(
                "Pandoc convertation failed. Please check the Pandoc command and debug info.\n")
    elif not PRE_PROCESSING and \
            not POST_PROCESSING and \
            OUTPUT is not None and \
            FILE is not None and \
            METADATA_FILE is not None:
        pre_process()
        status = pandoc_process(source=FILE)
        if (status == 0):
            print("Pandoc convertation done.\n")
            post_process(output=os.path.join(
                os.path.dirname(sys.argv[0]), OUTPUT))
        else:
            print(
                "Pandoc convertation failed. Please check the Pandoc command and debug info.\n")
    else:
        if len(sys.argv) > 1:
            print('参数组合不正确。使用 -H / --help 查看帮助文本。')
