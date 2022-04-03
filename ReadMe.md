# XUJC Thesis Markdown

适用于 XUJC 毕业论文的 Markdown 解决方案。

如果该项目确实提升了您的论文写作效率，欢迎为该项目加 Star、介绍给朋友、在论文的致谢部分感谢这个项目，或是将该项目列入参考文献。当然，我也会很感谢你请我喝一杯咖啡：

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/foldblade)

[TOC]

## 授权协议

该项目开放源代码，但**并不是自由软件**。作者希望能将该项目对个人免费开放使用，但**不希望任何人以盈利为目的利用本软件**。

如若您有意贡献代码，将视为您同意将您贡献的代码遵守这一协定。

```
您可以自由地：
    个人使用 - 在遵守许可证条款的情况下以个人名义自由使用该项目。
    演绎 - 修改、转换或以本项目为基础进行创作。

但需注意以下事项：
    免除责任 - 本授权协议不对本项目承担任何担保责任。有关本程序质量与效
    能的全部风险均由您承担。如本项目被证明有瑕疵，您应承担所有必要的服务、
    修复或更正的费用。
    禁止分发原始项目 - 您可以分享该项目的 URL，但禁止将未经修改的原
    始项目打包进行二次分发或散布。
    署名 - 您必须给出适当的署名，提供指向本许可协议的链接，同时标明是否
    对原始项目作了修改。您可以用任何合理的方式来署名，但是不得以任何方式暗
    示许可人为您或您的使用背书。
    非商业性使用 - 您不得将本项目用于任何商业目的。
    相同方式共享 - 如果您再混合、转换或者基于本项目进行创作，您必须基于
    与原先许可协议相同的许可协议分发您贡献的作品，且必须在项目中包含该许可
    协议文本。
```

## 环境要求

- Pandoc（需加入 PATH）
- Python 3.x （>= 3.7）
- Zotero，用于管理文献、生成 BibTex 格式引文

请自行前往 [Pandoc 官网](https://pandoc.org/installing.html)、[Python 官网](https://www.python.org/downloads/)、[Zotero 官网](https://www.zotero.org/download/)下载安装。

## 开发环境

我们的开发环境是：

- Windows 10
- Python 3.7.3
- pandoc 2.13
  - Compiled with pandoc-types 1.22, texmath 0.12.2, skylighting 0.10.5, citeproc 0.3.0.9, ipynb 0.1.0.1

该项目未经过大规模测试，如有问题，欢迎提出 issue。我们将尽力解答。

## 快速上手

进行快速上手前，请确保您的写作环境已经满足前文所述的环境要求。

1. `git clone` 或下载该项目。您也可以前往 [jsDelivr 下载](https://www.jsdelivr.com/package/gh/foldblade/XUJC-thesis-markdown)。
2. 在终端中运行以下命令，安装所需的 Python 依赖：

```bash
pip install panflute python-docx regex lxml pandoc-fignos pandoc-eqnos pandoc-tablenos
```

3. 使用终端进入该项目根目录，运行：

```bash
python processer.py -O result.docx -F ./demo/readme.md -M ./demo/metadata.yaml -B ./demo/ref.bib
```

如不出意外，您应该可以看到，在项目的根目录生成了`result.docx`——快去体验吧！

想了解具体写法，请移步 [`demo/readme.md`](./demo/readme.md) 查看文档。

敬请注意：在更新后，建议您运行 `python processer.py --clean` 以清理临时文件。

## Q / A

### 为什么不用 $\LaTeX$？

想呐，很想呐。不过学校是要求提交 Word 版本的。

### 会支持 WPS 吗？

仅通过了 Office 2016、Office 2019 等版本的测试，未进行 WPS 等其他软件测试，如有异常也不计划进行支持。我们建议您采用较新版本的 Office 编辑、查看。不过，Pull Request 我们是欢迎的。