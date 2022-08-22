# Q&A

## 为什么不用 $\LaTeX$？

想呐，很想呐。不过学校是要求提交 Word 版本的。

## 会支持 WPS 吗？

仅通过了 Office 2016、Office 2019 等版本的测试，未进行 WPS 等其他软件测试，如有异常也不计划进行支持。我们建议您采用较新版本的 Office 编辑、查看。不过，Pull Request 我们是欢迎的。

## 我的参考文献中间有很大的“空格”

尝试手动进行段落设置。选中参考文献文本，右键进入“段落”对话框。在“中文版式”选项卡下，勾选“允许西文在单词中间换行”。

## 我的参考文献标号与内容之间有很大的“空格”

尝试手动进行段落设置。选中参考文献文本，右键进入“段落”对话框。在“缩进与间距”选项卡下，点击左下角的“制表符”按钮，调整“默认制表位”的宽度到满意的效果。可以尝试非整数字符的“默认制表位”，也许会有较好的结果。

## 想要中西文全部使用宋体？

切换 `Song` 分支，并自行合并。

全文不分中西文均采用宋体无疑是丑陋的、缺少韵律与呼吸的、难言优雅的。作者本人提交的最终版本即是由本项目 `master` 分支生成的、中文采用宋体、西文采用 Times New Roman 的版本。

## 可能的错误

### 生成时，命令行最后出现 `PermissionError:` 之类的错误

检查您是否打开了生成的 docx 文档。当 docx 文档被打开或占用时，我们的程序将无法完成修改保存的操作，因此请您确认完全关闭生成的 docx 文档后再试。

### 命令行最后出现 `AttributeError: 'NoneType' object has no attribute 'findall'`

```
File "./processer.py", line xyz, in document_process
    sectPr = pPr.findall("w:sectPr", namespaces)
AttributeError: 'NoneType' object has no attribute 'findall'
```

检查您的 Markdown 文件是否存在内容、是否在 Markdown 开头插入 `\newSectionInNewPage`。

### 命令行最后出现 `'pandoc' 不是内部或外部命令，也不是可运行的程序`

没有安装 Pandoc。请安装 Pandoc 或将 Pandoc 可执行文件放入 bin 目录内。
