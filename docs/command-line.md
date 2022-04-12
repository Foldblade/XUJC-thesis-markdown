# 命令行参数

!!! warning
    以下命令给出的示例均假设您处于本项目根目录内运行。并不是所有示例都是可以成功运行的。

!!! info
    命令行参数理论上支持相对路径与绝对路径。您可以在我们的项目内外运行我们的 `procsser.py`，命令行参数的路径可以是绝对路径或是当前工作目录的相对路径。

## 一般性使用

一般性使用包含预处理、Pandoc 处理、后处理整个流程。您可以运行：

```bash
python processer.py -O result.docx -F ./demo/readme.md -M ./demo/metadata.yaml -B ./demo/ref.bib
```

其中：

- `-O` 或 `--output`：后接您期望的输出 docx 文件路径。必须。
- `-F` 或 `--file`：后接输入的 Markdown 文件路径。必须。
- `-M` 或 `--metadata-file`：后接输入的元数据 yaml 文件路径。必须。
- `-B` 或 `--bibliography`：后接输入的参考文献 BibTeX 文件路径。该参数是可选的，便于您在尚未添加引文时查看文档的排版效果。比如，当您尚未进行到引文的引入时，可以仅运行有三个参数的命令：`python processer.py -O result.docx -F ./demo/readme.md -M ./demo/metadata.yaml`

## 仅进行预处理

```bash
python processer.py --pre
```

## 仅进行后处理

```bash
python processer.py --post -O result.docx -F ./build/pandoc_processed.docx 
```

其中：

- `-O` 或 `--output`：后接您期望的输出 docx 文件路径。可选，默认为该项目下的 `build/final.docx`。
- `-F` 或 `--file`：后接输入的、pandoc 处理过的 docx 文件路径。可选，默认为该项目下的 `build/pandoc_processed.docx`。

## 清理

```
python processer.py --clean
```

将清理预处理生成的内容。建议在每次更新后运行。

!!! danger
    完成`assets/template.docx`修改后，请**自行备份**好您的 。我们的清理命令会删除 `assets/template.docx`。

!!! danger
    运行该命令，将会删除 `bin`、`assets` 目录，请不要将您的修改内容留存在这些目录内。

该命令将清理临时文件。

## 帮助文本

```bash
python processer.py --h
```

## 不在文档末尾生成空白页作为封底

```bash
python processer.py ...略... --no-blank-back-cover
```

若不添加该参数，则默认会在文档末尾生成空白页作为封底。

## 创建脚手架

```bash
python processer.py --new path_of_your_destination_directory
```

使用该命令，在指定目录创建脚手架以便快速开始，

## 更多

参阅 `processer.py`。
