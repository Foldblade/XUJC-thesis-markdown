# 快速开始

## 环境要求

- Pandoc >= 2.13 <3.0.0（开发时使用 2.18，测试未覆盖全部版本）
- Python 3.x（开发时使用 3.11，测试未覆盖全部版本）
- Zotero，用于管理文献

## 开发环境

我们的开发环境是：

- Windows 11
- Python 3.11.5
- pandoc 2.18
  Compiled with pandoc-types 1.22.2, texmath 0.12.5, skylighting 0.12.3,
  citeproc 0.7, ipynb 0.2, hslua 2.2.0
  Scripting engine: Lua 5.4

该项目未经过大规模测试，如有问题，欢迎提出 issue。我们将尽力解答。

## 环境搭建

### Pandoc

Pandoc 可实现不同标记语言间的格式转换，是该项目的重要依赖。请前往 [Pandoc 官网](https://pandoc.org/installing.html)下载安装。

!!! tip
    如果您使用 Typora 作为 Markdown 编辑器，并已经使用过其中的文档转换功能，那您很可能已经安装了 Pandoc。请在终端中使用 `pandoc --version` 检查版本是否高于 2.13 且 小于 3.0.0。若否，请卸载后重新安装。

!!! warning
    由于项目写就已有所时日，目前测试下 pandoc 的依赖还停留在较旧的 2.18 版本，3.0 及更高版本可能存在问题。我们更建议您下载 Pandoc 2.18 的可执行文件。在下文的[新手上路](#新手上路)一节中，我们会指导您将可执行文件安放在合适的位置。

### Python

该项目中的过滤器采用 Python 语言写就。请自行前往 [Python 官网](https://www.python.org/downloads/)下载安装。有关安装的具体步骤，您可以参阅：[Python3 环境搭建](https://www.runoob.com/python3/python3-install.html)。

!!! warning
    Python 需要加入 PATH。

### Zotero

我们采用 Zotero 进行文献管理，这是一个免费且开源的文献管理软件。请自行前往 [Zotero 官网](https://www.zotero.org/download/)下载安装

如果您只是体验该项目，则暂时可以不必安装。若您愿意采用此项目撰写您的毕业论文，则我们强烈推荐您安装 Zotero 及 Zotero Connector 浏览器插件，并参阅[附录](appendix.md)一章中的 Zotero 简明教程。

### Markdown 编辑器

用来编辑你的 Markdown 文件。Markdown 是一个纯文本文件，你可以使用常见的代码编辑器打开、编辑，诸如 VSCode 或 JetBrains 系 IDE 都对 Markdown 提供了支持。

Markdown 编辑器挑一个趁手的就好，个人推荐 [Typora](https://typora.io/)，这是一个所见即所得的 Markdown 编辑器。

## 新手上路

进行新手上路前，请确保您的写作环境已经满足前文所述的环境要求。

1. `git clone https://github.com/Foldblade/XUJC-thesis-markdown.git` 或[下载](https://github.com/Foldblade/XUJC-thesis-markdown/archive/refs/heads/master.zip)该项目
2. （针对不想安装 Pandoc 者）请在该项目根目录下新建 `bin` 目录，再前往 [Pandoc Releases 页](https://github.com/jgm/pandoc/releases)自行下载适合您系统版本的可执行文件。这通常会是一个压缩包，譬如 `pandoc-2.18-windows-x86_64.zip`，请在解压后，将可执行文件（如 `pandoc.exe`）放在 `bin` 目录中。我们建议您使用 2.18 版本。在 Windows 上，目录结构看起来应该类似：

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

3. 安装所需的 Python 依赖

   全局安装与 Python 虚拟环境二选一即可。我们更推荐您使用虚拟环境。

   1. 全局安装

    在终端中输入：

    ```bash
    pip install panflute python-docx regex lxml requests progressbar2 pandoc-fignos pandoc-eqnos pandoc-tablenos
    ```

   2. 选择使用 Python 虚拟环境（推荐）

    您需要使用终端进入该项目根目录，通过以下命令创建一个虚拟环境：

    ```bash
    python -m venv venv
    ```

    该行命令不得随意更改，虚拟环境的名称必须是 venv。

    通过以下命令激活虚拟环境：

    === "Windows"
        ```powershell
        venv\Scripts\activate
        ```

        !!! failure
            如果您在执行命令时出现“因为在此系统上禁止运行脚本”的错误，请执行 `Set-ExecutionPolicy RemoteSigned` 并在随后的询问中输入 `y` 以为当前用户设置 [PowerShell 的执行策略](https://docs.microsoft.com/zh-cn/powershell/module/microsoft.powershell.core/about/about_execution_policies)为 RemoteSigned。

    === "Linux"
        ```bash
        source venv/bin/activate
        ```

    完成虚拟环境的激活后，通过以下命令安装依赖：

    ```bash
    pip install -r requirements.txt
    ```

    如若您采用虚拟环境，则本项目相关的一切命令行操作均应在虚拟环境下运行。

4. 使用终端进入该项目根目录，运行：

    ```bash
    python processer.py -O result.docx -F ./demo/readme.md -M ./demo/metadata.yaml -B ./demo/ref.bib
    ```

!!! tip
    不知道如何“使用终端进入该项目根目录”？在 Windows 下，使用文件资源管理器，找到存在 `processer.py` 的目录，按住 Shift 键，在文件资源管理器空白处右键，选择“在终端中打开”、“在 PowerShell 中打开”等。或者，打开命令提示符或 PowerShell，使用 [`cd` 命令](https://docs.microsoft.com/zh-cn/windows-server/administration/windows-commands/cd)，在输入 `cd` 后接一个空格，粘贴存在 `processer.py` 的目录的路径后，按下回车，再复制第 4 步的命令。

!!! warning
    在该命令的执行过程中，可能会出现 `[WARNING] Could not convert TeX math \LaTeX, rendering as TeX:` 字样，Don't panic，毋需惊慌，只要最末一行出现 `Output file:` 即告成功。

如不出意外，您应该可以看到，在项目的根目录生成了`result.docx`，这是由 `demo` 目录中的[三大元素](three-elements.md)生成的。快去体验吧！

!!! tip
    `demo` 中的 `readme.md` 是由 `docs` 目录下的各文档拼合而成的。图片采用相对路径，取自 `docs` 目录下的 `readme.assets` 目录。

!!! tip
    有关命令的详细解读，请参考[命令行参数](command-line.md)一章。

!!! tip
    您也可以通过[图形用户界面](gui.md)中选择 `demo` 目录作为基础目录以体验生成效果。
