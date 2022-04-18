# 撰写指南

我们建议您做好 demo 目录下所有文件的备份，最好一开始就复制一份出来。如果您没有足够的耐心阅读文档，我们更建议运用脚手架开始写作，且时常运行生成命令以检查错误，而不是从一份空白的 Markdown 文档开始。

## Markdown

Markdown 的基础语法，我相信凭借自己实力找到这个项目的人已经有所了解。

但如果您还不会 Markdown，我建议您花费一些时间学习它。您可以参考[这个教程](https://markdown.com.cn/intro.html)，或是[这个知乎问题](https://www.zhihu.com/question/20409634)。

单纯的 Markdown 并不足以支持我们完成毕业论文的生成。因此，请继续向下看。

## Pandoc Markdown

由于 Markdown 到 docx 转换采用的是 Pandoc[@Pandoc]，这里就不得不提 Pandoc Markdown 语法了。您可以在撰写时使用 Pandoc Markdown 语法实现一些 Pandoc 特性，不过这可能需要您对 Pandoc 有着熟练掌握，并按需修改 `filter.py`。具体细节，请查阅[官方文档](https://pandoc.org/MANUAL.html#pandocs-markdown)，或是[这份（可能有些过时的）中文翻译](http://pages.tzengyuxio.me/pandoc/)。

请放心，不会 Pandoc Markdown 语法并不会影响您对本项目的使用。

## 自定义类 $\LaTeX$ 命令

!!! info
    这一节中包含封面、原创性声明、中英文摘要、目录等的生成。

您可以使用我们自定义的一些类 $\LaTeX$ 命令辅助 docx 的排版。相信您应该已经在本文件的开头部分见过它们了：

```LaTex
\cover - 封面
\statementOfOriginality - 原创性声明
\abstract - 生成中文摘要
\abstractEn - 生成英文摘要
\toc - 目录
\newSectionInNewPage - 分节符（下一页）
\newSection - 分节符
\pageBreak - 分页符
```

比如，依照撰写规范[@ShaMenDa]，引言及正文之间是需要另起一页的。所以，您应该在引言与第一章之间，插入一个 `\pageBreak`。

!!! tip
    如若您的学院要求“每个章节以新一页作为开始”，则也需在正文的每个章节标题前插入一个 `\pageBreak`。

!!! warning
    您**必须**在文档开头插入一个 `\newSectionInNewPage`。

Pandoc 在生成时，会自动在文档开头生成元数据中的标题、作者等信息，这对我们来说是多余的。因此，在后处理流程中，我们会删除第一个 `\newSectionInNewPage` 及其之前的所有内容。

部分 Markdown 编辑器支持 `[TOC]` 目录。您也可以在适当位置插入 `[TOC]`，我们的过滤器会将 `[TOC]` 视为 `\toc`。这些命令的转换过程发生在项目根目录的 `filter.py` 中，您可以自行前往，查看具体的转换与实现。

封面、原创性声明均取自学校提供的模板文件，唯进行了排版的优化，如将“回车换页”优化为了更科学的分页符换页，此改动不会影响您的使用。

## 元数据

!!! info
    这一节中包含封面中的标题、作者、院系、专业、学号、指导教师、职称等信息的配置，以及中英文摘要和关键词的配置。

`demo/metadata.yaml` 文件以及脚手架中的 `metadata.yaml` 均是我们的元数据文件。在该文件中，您可以修改封面中的标题、作者等信息，撰写您的摘要，也可以进行一些诸如图片自动编号、表格自动编号、公式自动编号的配置。

您可以用代码或文本编辑器打开 YAML 文件进行编辑。如果您并不熟悉 YAML 语法，请在完成编辑后将全部内容复制到 [YAML 校验工具](https://www.bejson.com/validators/yaml_editor/)进行校验，通过后再进行保存。

!!! tip
    YAML 的注释用 `#`。

!!! tip
    元数据中的 `abstract` 与 `abstractEn` 字段，我们强烈建议您在一行内完成撰写。如果您觉得一行不够“优雅”、希望分段呈现，则您必须在每段之间空一行（实际上便是在每段后加入两个换行符、按两下回车）。如果您仅使用一个回车、不在段落中空一行，您的中文摘要可能出现意想不到的情况，例如句间的空格。

## 封底

默认会在文档末尾生成空白页作为封底。如您不需要，请参阅[命令行参数](command-line.md)一章中的[不在文档末尾生成空白页作为封底](#不在文档末尾生成空白页作为封底)一节，在生成命令后加上参数 `--no-blank-back-cover`。

## 段落

自由地按照 Markdown 语法撰写段落即可。要创建段落，请使用空白行将一行或多行文本进行分隔。不要用空格或制表符缩进段落。

!!! tip
    如您需保留一个空段落——或者更通常意义上的“换行”；例如，您的指导老师要求您在“结论”后空一行；那您应该在结论后空出一段，并在那一段落中输入四个空格。由于 Markdown 靠两个换行符进行段落的划分，因此，实际的 Markdown 应该表现为：结论与结论第一段之间空出三行，在其中的第二行输入四个空格。

## 章节标题及自动编号

不同于 Markdown 文件中通常只出现一个一级标题，在我们的 Markdown 中，第几级标题便是几级标题。这意味着，您的一级标题“绪论”，应该使用 Markdown 的一级标题语法：`# 绪论`。

引言、结论、致谢、参考文献、附录也采用一级标题。为了正确生成对应的样式，您的引言、结论、致谢、参考文献、附录，**能且只能**取值为：引言、总结、结论、致谢、致谢语、参考文献、附录。具体细节，请参阅[模板文件样式说明](#模板文件样式说明)一节。如果您变换了这些标题，它们将无法得到正确处理。

我们默认配置了章节标题自动编号——包括每章开头自动转变为“第 x 章”，您仅需在 Markdown 中行云流水地创作即可。如果您选择了章节标题自动编号，正如 `demo/readme.md` 与脚手架所展示的那样，您还需要在引言、结论、致谢、参考文献、附录的后面加上 `{.unnumbered}`，这会让 Pandoc 意识到这几节是无需自动编号的。

当然，您也可以选择手动编号——这将给您标题编号的更多自由度，比如结构为：

- 第一章
  - （一）
    - `1.`
      - （1）
        - ①

等，这需要您在撰写标题时就手动加入。您需要手动撰写标题如 `# 第一章 绪论`而不像自动编号这样的 `# 绪论`。此外，您还需要在根目录的 `processer.py` 中找到 `pandoc_process` 函数，在其中注释以下内容：

````diff
--- processer.py
                      + '--csl "%s" ' % os.path.join(WHERE_SCRIPT, 'assets/chinese-gb7714-2005-numeric.csl')
-                     + '--number-sections '  # 章节自动编号
+                  #  + '--number-sections '  # 章节自动编号
                      + source)
````

## 图片、表格、公式的引用及自动编号

!!! info
    自动编号是可选的。您完全可以按照 Markdown 语法手动进行编号。

!!! warning
    该项目采用的是我们修改过的 pandoc-xnos 部分组件，但官方文档仍是适用的。

该功能采用 [pandoc-xnos](https://github.com/tomduck/pandoc-xnos) 过滤器套件实现[@Duck2022pandoc-xnos]。您可以在元数据文件中修改它的配置：

```yaml
***-plus-name: 图 # 行内引用
***-star-name: 图 # 行首引用（汉字理论上是和行内没区别的，主要面向西文用户，大小写需求）
***-caption-name: 图 # 说明文字（题目）名称，如 图、Fig、Figure 等
***-caption-separator: space # 说明文字（题目）编号与说明文字（题目）分隔符，可取值为 none, colon, period, space, quad, newline
***-number-by-section: false # 是否按章节编号
```

有关我们自定义的配置项：

```yaml
***-section-separator: '-' # 章节编号分隔符，如 1-1，若注释或删除则默认为 1.1
```

### 图片及自动编号

!!! warning
    该项目采用的是[我们修改过的 pandoc-fignos](https://github.com/foldblade/pandoc-fignos)。但官方文档仍是适用的。

该功能采用 pandoc-fignos[Duck2022pandoc-fignos] 实现。

在 Word 中的显示效果则类似：

图片说明文字（题目）：`图 1.1  这是图片描述`

图片引用：`图 1.1`

您可以像这样插入一张图片：

```markdown
![Photo by Baim Hanif on Unsplash, Free to use under the Unsplash License](readme.assets/baim-hanif-pYWuOMhtc6k-unsplash.jpg){#fig:graduation}
```

其中，中括号内写图片的说明文字（题目），括号内是文件的路径，最后的大括号中 `#fig:` 来自 pandoc-fignos，冒号后需要是一个全文唯一的字符串或是数字。您可以通过 `+@fig:graduation{nolink=True}` 这样的语法去引用图片并实现自动编号，一般来说，行内引用以 `+` 开头，行首引用以 `*` 开头。`nolink=True` 表示不为引用生成超链接。当您引用图片时，如果选择添加超链接，您可能需要在引用命令外包裹以大括号：`{+@fig:graduation}`。具体配置均存放于元数据文件中，有关配置的具体细节，请参阅 [pandoc-fignos 文档](https://github.com/tomduck/pandoc-tablenos)。

!!! tip
    我们建议您使用 Markdown 编辑器生成相对 Markdown 文件的**相对路径**，因为我们会默认 Markdown 文件所在目录为资源所在目录。

!!! info
    若需修改自动编号格式，可在元数据文件中修改它的配置。

!!! tip
    如果你需要修改章节分隔符，如从 图 1.1 变成 图 1-1，则应该在元数据中设置 `fignos-section-separator: '-'`。

如果您想手动为图片编号，仅需按 Markdown 标准语法撰写：

```markdown
![图 1.1 Photo by Baim Hanif on Unsplash, Free to use under the Unsplash License](readme.assets/baim-hanif-pYWuOMhtc6k-unsplash.jpg)
```

#### 样例

!!! warning
    样例部分唯有在生成的 docx 中才能看到最终效果。在 Markdown 编辑器或渲染结果中，您可以参考学习语法。

上述语法插入的图片来自 [Unsplash](https://unsplash.com/s/photos/graduation?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) 网站的 [Baim Hanif](https://unsplash.com/@baim?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)，采用 [Unsplash License](https://unsplash.com/license) 授权免费使用，如下+@fig:graduation{nolink=True}所示：

![Photo by Baim Hanif on Unsplash,  Free to use under the Unsplash License](readme.assets/baim-hanif-pYWuOMhtc6k-unsplash.jpg){#fig:graduation}

另一张来自 [Unsplash](https://unsplash.com/s/photos/graduation?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) 网站 [Joan Kwamboka](https://unsplash.com/@city_child?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) 的图片，采用 [Unsplash License](https://unsplash.com/license) 授权免费使用，如下{+@fig:graduation2}所示：

![Photo by Joan Kwamboka on Unsplash, Free to use under the Unsplash License](readme.assets/joan-kwamboka-hvL7qlvZ5T4-unsplash.jpg){#fig:graduation2}

### 表格及自动编号

!!! warning
    该项目采用的是[我们修改过的 pandoc-tablenos](https://github.com/foldblade/pandoc-tablenos)，但官方文档仍是适用的。

该功能采用 pandoc-tablenos[@Duck2022pandoc-tablenos] 实现。

在 Word 中的显示效果则类似：

表格说明文字（题目）：`表 1.1  这是表格描述`

表格引用：`表 1.1`

表格的插入建议采用编辑器。目前，Markdown 中的表格并不支持合并单元格；HTML 表格也暂时不被支持。我们建议您留空所需的单元格，在生成 Word 文档后手动合并。我们的表格样式采用三线表，有关表格样式的详细情况，请参阅[项目实现](implement.md)一章中的[Table](#Table) 一节。

您可以在表格前后这样这样插入表格的说明文字（题目）：

```markdown
: 知识共享许可协议的四项基本权利 {#tbl:CC_four_rights}
```

最后的大括号中 `#tbl:` 来自 pandoc-tablenos，冒号后需要是一个全文唯一的字符串或是数字。您可以通过 `+@tbl:CC_four_rights{nolink=True}` 这样的语法去引用图片并实现自动编号，一般来说，行内引用以 `+` 开头，行首引用以 `*` 开头。`nolink=True` 表示不为引用生成超链接。当您引用图片时，如果选择添加超链接，您可能需要在引用命令外包裹以大括号：`{+@tbl:CC_four_rights}`。具体配置均存放于元数据文件中，有关配置的具体细节，请参阅 [pandoc-tablenos 文档](https://github.com/tomduck/pandoc-tablenos)。

!!! info
    若需修改自动编号格式，可在元数据文件中修改它的配置。

!!! tip
    如果你需要修改章节分隔符，如从 表 1.1 变成 表 1-1，则应该在元数据中设置 `tablenos-section-separator: '-'`。

如果您想手动为表格编号，仅需按如下语法撰写：

```markdown
: 表 1.1 知识共享许可协议的四项基本权利 {#tbl:CC_four_rights}
```

#### 样例

!!! warning
    样例部分唯有在生成的 docx 中才能看到最终效果。在 Markdown 编辑器或渲染结果中，您可以参考学习语法。

下+@tbl:CC_four_rights{nolink=True}引用自[知识共享许可协议 - 维基百科，自由的百科全书](https://zh.wikipedia.org/wiki/%E7%9F%A5%E8%AF%86%E5%85%B1%E4%BA%AB%E8%AE%B8%E5%8F%AF%E5%8D%8F%E8%AE%AE)：

: 知识共享许可协议的四项基本权利 {#tbl:CC_four_rights}

| 权利                                                         | 备注                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| **署名**（英语：Attribution，**by**）                        | 您（用户）可以复制、发行、展览、表演、放映、广播或通过信息网络传播本作品；您必须按照作者或者许可人指定的方式对作品进行署名。 |
| **[相同方式共享](https://zh.wikipedia.org/wiki/相同方式共享)**（英语：**S**hare**A**like，**sa**） | 您可以自由复制、散布、展示及演出本作品；若您改变、转变或更改本作品，仅在遵守与本作品相同的授权条款下，您才能散布由本作品产生的派生作品。（参见 [copyleft](https://zh.wikipedia.org/wiki/Copyleft)）。 |
| **非商业性使用**（英语：**N**on**c**ommercial,**nc** ）      | 您可以自由复制、散布、展示及演出本作品；您不得为[商业](https://zh.wikipedia.org/wiki/商业)目的而使用本作品。 |
| **禁止演绎**（英语：**N**o **D**erivative Works，**nd**)     | 您可以自由复制、散布、展示及演出本作品；您不得改变、转变或更改本作品。 |

下{+@tbl:open_source_licenses_comparison}引用自[自由及开放原始码软体许可证比较 - 维基百科，自由的百科全书](https://zh.wikipedia.org/wiki/%E8%87%AA%E7%94%B1%E5%8F%8A%E9%96%8B%E6%94%BE%E5%8E%9F%E5%A7%8B%E7%A2%BC%E8%BB%9F%E9%AB%94%E8%A8%B1%E5%8F%AF%E8%AD%89%E6%AF%94%E8%BC%83)：

: 自由及开放原始码软体许可证比较 {#tbl:open_source_licenses_comparison}

| 许可证                                                       | 版本 | 包含许可证 | 包含原始码 | 连结 | 状态变化 | 商业使用 | 散布 | 修改 | 专利授权 | 私人使用 | 授权转售 | 无担保责任 | 没有商标 |
| ------------------------------------------------------------ | ---- | ---------- | ---------- | ---- | -------- | -------- | ---- | ---- | -------- | -------- | -------- | ---------- | -------- |
| [Apache 许可证](https://zh.wikipedia.org/wiki/Apache许可证)  | 2.0  | 是         |            |      | 是       | 是       | 是   | 是   | 是       | 是       | 是       | 是         | 是       |
| [3 句版 BSD 许可证](https://zh.wikipedia.org/wiki/BSD许可证) |      | 是         |            |      |          | 是       | 是   | 是   |          | 是       | 是       | 是         | 是       |
| [2 句版 BSD 许可证](https://zh.wikipedia.org/wiki/BSD许可证) |      | 是         |            |      |          | 是       | 是   | 是   |          | 是       | 是       | 是         |          |
| [GNU 通用公共许可证](https://zh.wikipedia.org/wiki/GNU通用公共许可证) | 2.0  | 是         | 是         |      | 是       | 是       | 是   | 是   | 是       | 是       | 否       | 是         |          |
| [GNU 通用公共许可证](https://zh.wikipedia.org/wiki/GNU通用公共许可证) | 3.0  | 是         | 是         |      | 是       | 是       | 是   | 是   | 是       | 是       | 是       | 是         |          |
| [GNU 宽通用公共许可证](https://zh.wikipedia.org/wiki/GNU宽通用公共许可证) | 2.1  | 是         | 是         | 是   |          | 是       | 是   | 是   | 是       | 是       | 是       | 是         |          |
| [GNU 宽通用公共许可证](https://zh.wikipedia.org/wiki/GNU宽通用公共许可证) | 3.0  | 是         | 是         | 是   |          | 是       | 是   | 是   | 是       | 是       | 是       | 是         |          |

### 公式及自动编号

!!! warning
    该项目采用的是[我们修改过的 pandoc-eqnos](https://github.com/foldblade/pandoc-tablenos)，但官方文档仍是适用的。

该功能采用 pandoc-eqnos[@Duck2022pandoc-eqnos] 实现。

在 Word 中的显示效果则类似：

公式显示：`pi = 3.14159265  (1.1)`

公式引用：开启美国数学协会风格：`式 (1.1)`、关闭美国数学协会风格：`式 1.1`

美国数学协会风格默认关闭。您可以在 `metadata.yaml` 中修改它的配置，去除注释并设定为 `true`：

```yaml
eqnos-eqref: true # 开启美国数学协会（AMS）风格引用
```

您可以以下列语法输入公式：单行公式使用双美元符 `$$` 包裹，行内公式使用单美元符 `$` 包裹，公式需遵循 $\TeX$ 语法，您可以使用[LaTeX 公式编辑器](https://www.latexlive.com)辅助生成。

```tex
$$ \pi = 3.141592653589793238462643 \ldots $$ {#eq:pi}
$$ S = \pi \times r^{2} $$ {#eq:area_of_circle}
```

最后的大括号中 `#eq:` 来自 pandoc-eqnos，冒号后需要是一个全文唯一的字符串或是数字。您可以通过 `+@eq:area_of_circle{nolink=True}` 这样的语法去引用图片并实现自动编号，一般来说，行内引用以 `+` 开头，行首引用以 `*` 开头。`nolink=True` 表示不为引用生成超链接。当您引用图片时，如果选择添加超链接，您可能需要在引用命令外包裹以大括号：`{+@eq:area_of_circle}`。具体配置均存放于元数据文件中，有关配置的具体细节，请参阅 [pandoc-eqnos 文档](https://github.com/tomduck/pandoc-eqnos)。

!!! info
    若需修改自动编号格式，可在元数据文件中修改它的配置。

!!! tip
    如果你需要修改章节分隔符，如从 式 1.1 变成 式 1-1，则应该在元数据中设置 `eqnos-section-separator: '-'`。

如果您想手动为公式编号，仅需按如下语法撰写：

```tex
$$ S = \pi \times r^{2} $$ (1.1)
```

#### 样例

!!! warning
    样例部分唯有在生成的 docx 中才能看到最终效果。在 Markdown 编辑器或渲染结果中，您可以参考学习语法。

$$ \pi = 3.141592653589793238462643 \ldots $$ {#eq:pi}

$$ S = \pi \times r^{2} $$ {#eq:area_of_circle}

*@eq:pi{nolink=True} 展现了圆周率 π，它是一个无理数。计算圆的面积，一般会用{+@eq:area_of_circle}。

行内公式，可以使用语法 `$\pi = 3.141592653589793238462643 \ldots$` 。结果是这样的：$\pi = 3.141592653589793238462643 \ldots$。

!!! warning
    由于本文档中出现了部分的 $\LaTeX$ 语法，在转换时可能出现 Warning，诸如 `[WARNING] Could not convert TeX math \LaTeX, rendering as TeX:` 。在撰写时，请尽量保证公式采用 $\TeX$ 语法。

## 代码与代码高亮

!!! warning
    代码块会采用 Consolas 字体，这可能无法符合部分指导老师对正文部分的要求。请谨慎使用。

代码请使用 Markdown 代码块。代码高亮风格，参阅[Pandoc 文档 Syntax highlighting 一节](https://pandoc.org/MANUAL.html#syntax-highlighting)。考虑到打印需求，我们采用了一个灰度风格`monochrome`。高亮风格的样例，可以在[这里](https://github.com/kaityo256/pandoc_highlight)查看。如需修改，请在根目录的 `processer.py` 中找到 `pandoc_process` 函数中修改：

```diff
--- processer.py
                      # 资源文件路径，默认与输入文件一致
                      + '--resource-path="%s" ' % os.path.dirname(source)
-                     + '--highlight-style monochrome '  # 考虑到最后需要打印，选了个灰度的高亮风格
+                     + '--highlight-style pygments '  # 换成了 pygments 风格
                      + '--filter pandoc-fignos '  # 图片自动编号
```

## 参考文献及自动生成引文

### 参考文献放置

根据 [Pandoc 文档 Placement of the bibliography](https://pandoc.org/MANUAL.html#placement-of-the-bibliography)，您需要在放置参考文献列表的地方放置以下文本：

```
::: {#refs}
:::
```

如不放置，将会在文末最后生成参考文献列表。

### 引文文件与引文自动生成

引文依靠 Pandoc 自动生成，需要提供一个 BibTeX 格式[@BibTeX]引文文件。您可以在 `/demo/ref.bib` 中找到本文使用的引文文件。具体教程，请参阅附录中的 [Zotero 简明教程](#Zotero_简明教程)。

您可以通过以下语法插入引文：`[@BibTeX]`。在希望插入引文的地方，插入方括号，`@` 后跟 Zotero 内的 Citation Key 即可。

#### 样例

!!! warning
    样例部分唯有在生成的 docx 中才能看到最终效果。在 Markdown 编辑器或渲染结果中，您可以参考学习语法。

比如，我又引用了一遍 BibTeX 官网[@BibTeX]。
