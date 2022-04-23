# 三大元素

我们需要三个文件以完成论文的生成：

1. 使用 Markdown 撰写论文
2. 使用元数据文件设定论文的部分信息、进行配置
3. 使用 BibTeX 格式引文文件生成引文

一个典型的论文基础目录结构是这样的：

```
.
    thesis.md
    metadata.yaml
    ref.bib
```

- `thesis.md` 是 Markdown 格式的论文，您应当在这里参考[撰写指南](writing-guide.md)自由起舞、撰写论文
- `metadata.yaml` 是元数据文件，您可以使用文本编辑器打开编辑，参考[撰写指南](writing-guide.md)修改封面、摘要的信息并进行一些配置
- `ref.bib` 是 BibTeX 格式引文文件，这应当参考[附录](appendix.md)中的 [Zotero 简明教程](appendix.md#附录一 Zotero 简明教程 {.unnumbered})使用 Zotero 导出

对一篇完整的论文来说，这三个文件不可或缺；但如果您刚刚开始写作，您可以暂不添加 BibTeX 格式的引文文件。

!!! tip
    例如，`demo` 目录中就存在着这三大元素;而我们的“[新建脚手架](start-writing-from-the-scaffold.md)”操作就仅会创建 Markdown 文件与元数据文件。

三个文件的文件名是可以更改的，但相应地，您也要更改您的[生成命令](command-line.md)；当然，您也可以通过[图形用户界面（GUI）](gui.md)直接进行选择。
