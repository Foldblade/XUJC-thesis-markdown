# 快速开始

## 环境要求

- Pandoc >= 2.13 （更老版本未经测试）
- Python 3.x （>= 3.7，更老版本未经测试）
- Zotero，用于管理文献（可选）

## 开发环境

我们的开发环境是：

- Windows 10
- Python 3.7.3
- pandoc 2.18
  Compiled with pandoc-types 1.22.2, texmath 0.12.5, skylighting 0.12.3,
  citeproc 0.7, ipynb 0.2, hslua 2.2.0
  Scripting engine: Lua 5.4

该项目未经过大规模测试，如有问题，欢迎提出 issue。我们将尽力解答。

## 环境搭建

### Pandoc

Pandoc 可实现不同标记语言间的格式转换，是该项目的重要依赖。请前往 [Pandoc 官网](https://pandoc.org/installing.html)下载安装。

!!! tip
    如果您使用 Typora 作为 Markdown 编辑器，并已经使用过其中的文档转换功能，那您很可能已经安装了 Pandoc。请在终端中使用 `pandoc --version` 检查版本是否高于 2.13，若否，请卸载后重新安装。

!!! tip
    如果您不想安装 Pandoc，可以暂时跳过该节。在[新手上路](#新手上路)一节中，我们会指导您将可执行文件安放在合适位置。

### Python

该项目中的过滤器采用 Python 语言写就。请自行前往 [Python 官网](https://www.python.org/downloads/)下载安装。有关安装的具体步骤，您可以参阅：[Python3 环境搭建](https://www.runoob.com/python3/python3-install.html)。

!!! warning
    Python 需要加入 PATH。

### Zotero

我们采用 Zotero 进行文献管理，这是一个免费且开源的文献管理软件。请自行前往 [Zotero 官网](https://www.zotero.org/download/)下载安装

如果您只是体验该项目，则暂时可以不必安装。若您愿意采用此项目撰写您的毕业论文，则我们强烈推荐您安装 Zotero 及 Zotero Connector 浏览器插件，并参阅[附录](appendix.md)一章中的 Zotero 简明教程。

## 新手上路

进行新手上路前，请确保您的写作环境已经满足前文所述的环境要求。

1. `git clone https://github.com/Foldblade/XUJC-thesis-markdown.git` 或[下载](https://github.com/Foldblade/XUJC-thesis-markdown/archive/refs/heads/master.zip)该项目
2. 在终端中运行以下命令，安装所需的 Python 依赖：

    ```bash
    pip install panflute python-docx regex lxml pandoc-fignos pandoc-eqnos pandoc-tablenos
    ```

3. （针对不想安装 Pandoc 者）请在该项目根目录下新建 `bin` 目录，再前往 [Pandoc Releases 页](https://github.com/jgm/pandoc/releases)自行下载适合您系统版本的可执行文件。这通常会是一个压缩包，譬如 `pandoc-2.18-windows-x86_64.zip`，请在解压后，将可执行文件（如 `pandoc.exe`）放在 `bin` 目录中。在 Windows 上，目录结构看起来应该类似：

    ```
    │  .gitignore
    │  filter.py
    │  LICENSE
    │  processer.py
    │  略...
    │
    ├─bin
    │  └─ pandoc.exe
    │
    ├─略...
    │
    └─略...
    ```

4. 使用终端进入该项目根目录，运行：

    ```bash
    python processer.py -O result.docx -F ./demo/readme.md -M ./demo/metadata.yaml -B ./demo/ref.bib
    ```

!!! warning
    在该命令的执行过程中，可能会出现 `[WARNING] Could not convert TeX math \LaTeX, rendering as TeX:` 字样，Don't panic，毋需惊慌，只要最末一行出现 `Output file:` 即告成功。

如不出意外，您应该可以看到，在项目的根目录生成了`result.docx`——快去体验吧！

!!! tip
    `demo` 中的 `readme.md` 是由 `docs` 目录下的各文档拼合而成的。图片采用相对路径，取自 `docs` 目录下的 `readme.assets` 目录。

!!! tip
    有关命令的详细解读，请参考[命令行参数](command-line.md)一章。
