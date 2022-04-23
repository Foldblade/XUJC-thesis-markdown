# 从脚手架开始写作

我们提供了脚手架以助您快速开始。

您可以使用如下命令以创建一个脚手架：

```bash
python processer.py --new path_of_your_destination_directory
```

例如，通过以下命令，您可以在 D 盘 `my-thesis` 目录创建一个脚手架。

```bash
python processer.py --new "D:\my-thesis"
```

您会在目录中看到如下两个文件：

- metadata.yaml
- thesis.md

其中，`thesis.md` 提供了一个包含封面、中英文摘要、目录、正文、结论、致谢、参考文献、附录的论文基础模板；而 `metadata.yaml` 则是元数据与配置项所在地。

您可以从脚手架快速开始撰写——当然，永远要记得备份您的数据！

!!! tip
    觉得太难？请参阅[图形用户界面（GUI）](gui.md)。

有关写作的更多细节，请参阅[撰写指南](writing-guide.md)一章。
