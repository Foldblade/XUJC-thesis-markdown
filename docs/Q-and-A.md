# Q&A

## 为什么不用 $\LaTeX$？

想呐，很想呐。不过学校是要求提交 Word 版本的。

## 会支持 WPS 吗？

仅通过了 Office 2016、Office 2019 等版本的测试，未进行 WPS 等其他软件测试，如有异常也不计划进行支持。我们建议您采用较新版本的 Office 编辑、查看。不过，Pull Request 我们是欢迎的。

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
