# XUJC Thesis Markdown

适用于 XUJC 毕业论文的 Markdown 解决方案。

当然，需要注意的是，不同院系、不同指导老师的要求不一样，所以，最终多多少少需要对生成的 docx 文件进行调整，例如图片的大小、表格的尺寸等。总的来说，您可以使用 Markdown 撰写草稿，在文本定稿后使用本工具快速生成排版后的 docx 文档，最终根据老师需求进行一些微调后定稿。

如果该项目确实提升了您的论文写作效率，欢迎为该项目加 Star、介绍给朋友、在论文的致谢部分感谢这个项目，或是将该项目列入参考文献。当然，我也会很感谢你请我喝一杯咖啡：

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/foldblade)

## 为什么您需要它

- 通过 Markdown 专注于内容撰写
- 减少排版所需时间与返工次数
- 自动生成章节、图、表、公式编号，无需手动管理
- 使用文献管理工具生成引文，无需手动整理格式插入
- 使用您最喜爱的代码管理工具管理您的论文版本
- 获得更加优雅的论文撰写体验

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

- Pandoc >= 2.13 （更老版本未经测试）
- Python 3.x （>= 3.7，更老版本未经测试）
- Zotero，用于管理文献

## 快速上手

您可以访问我们的[文档网站](https://foldblade.github.io/XUJC-thesis-markdown)查看文档，或是移步 [`demo/readme.md`](./demo/readme.md) 查看文档。

敬请注意：在更新后，建议您运行 `python processer.py --clean` 以清理临时文件。
