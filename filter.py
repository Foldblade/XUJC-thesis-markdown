# encoding: utf-8

"""
Pandoc filter using panflute
"""

import datetime
import regex
from panflute import *
from processer import VERSION

# 硬编码一些组件，懒得拆 XML 了
page_break = RawBlock(
    "<w:p><w:r><w:br w:type=\"page\" /></w:r></w:p>", format="openxml")
section_break_with_new_page = RawBlock('''
<w:p>
    <w:pPr>
        <w:sectPr>
            <w:type w:val=\"nextPage\"/>
            <w:pgSz w:w="11906" w:h="16838" w:code="9"/>
        </w:sectPr>
    </w:pPr>
</w:p>
''', format="openxml")
section_break = RawBlock(
    "<w:p><w:pPr><w:sectPr><w:type w:val=\"continuous\" /></w:sectPr></w:pPr></w:p>", format="openxml")
toc = RawBlock(r'''
<w:sdt>
    <w:sdtContent xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
        <w:p>
            <w:r>
                <w:fldChar w:fldCharType="begin" w:dirty="true" />
                <w:instrText xml:space="preserve">TOC \o "1-3" \h \z \u</w:instrText>
                <w:fldChar w:fldCharType="separate" />
                <w:fldChar w:fldCharType="end" />
            </w:r>
        </w:p>
    </w:sdtContent>
</w:sdt>
''', format="openxml")
statement_of_originality = RawBlock(
    '''
<w:p>
    <w:pPr>
        <w:spacing w:line="360" w:before="0" w:after="0" w:lineRule="auto"/>
        <w:jc w:val="center"/>
        <w:rPr>
            <w:b/>
            <w:sz w:val="24"/>
        </w:rPr>
    </w:pPr>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:line="360" w:before="0" w:after="0" w:lineRule="auto"/>
        <w:jc w:val="center"/>
        <w:rPr>
            <w:b/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
    </w:pPr>
    <w:r>
        <w:rPr>
            <w:b/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
        <w:t>原创性声明</w:t>
    </w:r>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:line="360" w:before="0" w:after="0" w:lineRule="auto"/>
        <w:rPr>
            <w:sz w:val="30"/>
            <w:szCs w:val="30"/>
        </w:rPr>
    </w:pPr>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:line="360" w:before="0" w:after="0" w:lineRule="auto"/>
        <w:rPr>
            <w:sz w:val="30"/>
            <w:szCs w:val="30"/>
        </w:rPr>
    </w:pPr>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:line="360" w:before="0" w:after="0" w:lineRule="auto"/>
        <w:ind w:firstLineChars="200" w:firstLine="600"/>
        <w:rPr>
            <w:sz w:val="30"/>
            <w:szCs w:val="30"/>
        </w:rPr>
    </w:pPr>
    <w:r>
        <w:rPr>
            <w:sz w:val="30"/>
            <w:szCs w:val="30"/>
        </w:rPr>
        <w:t>兹呈交的学位论文（设计），是本人在导师指导下独立完成的研究成果。除文中已经明确标明引用或参考的内容外，本论文（设计）不包含任何其他个人或集体已经发表或撰写过的研究成果。本人依法享有和承担由此论文而产生的权利和责任。</w:t>
    </w:r>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:line="360" w:before="0" w:after="0" w:lineRule="auto"/>
        <w:rPr>
            <w:sz w:val="30"/>
            <w:szCs w:val="30"/>
        </w:rPr>
    </w:pPr>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:line="360" w:before="0" w:after="0" w:lineRule="auto"/>
        <w:rPr>
            <w:sz w:val="30"/>
            <w:szCs w:val="30"/>
        </w:rPr>
    </w:pPr>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:line="360" w:before="0" w:after="0" w:lineRule="auto"/>
        <w:rPr>
            <w:sz w:val="30"/>
            <w:szCs w:val="30"/>
        </w:rPr>
    </w:pPr>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:line="360" w:before="0" w:after="0" w:lineRule="auto"/>
        <w:ind w:firstLineChars="1250" w:firstLine="3750"/>
        <w:rPr>
            <w:sz w:val="30"/>
            <w:szCs w:val="30"/>
        </w:rPr>
    </w:pPr>
    <w:r>
        <w:rPr>
            <w:sz w:val="30"/>
            <w:szCs w:val="30"/>
        </w:rPr>
        <w:t>声明人（签名）：</w:t>
    </w:r>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:line="360" w:before="0" w:after="0" w:lineRule="auto"/>
        <w:ind w:firstLineChars="1250" w:firstLine="3750"/>
        <w:rPr>
            <w:sz w:val="30"/>
            <w:szCs w:val="30"/>
        </w:rPr>
    </w:pPr>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:line="360" w:before="0" w:after="0" w:lineRule="auto"/>
        <w:jc w:val="right"/>
        <w:rPr>
            <w:sz w:val="30"/>
            <w:szCs w:val="30"/>
        </w:rPr>
    </w:pPr>
    <w:r>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:sz w:val="30"/>
            <w:szCs w:val="30"/>
        </w:rPr>
        <w:t xml:space="preserve">日期：      年    月    日</w:t>
    </w:r>
</w:p>
<w:p>
    <w:pPr>
        <w:sectPr>
            <w:type w:val="nextPage"/>
            <w:pgSz w:w="11906" w:h="16838" w:code="9"/>
            <w:pgMar w:top="1134" w:right="1474" w:bottom="1134" w:left="1474" w:header="851" w:footer="992" w:gutter="0"/>
            <w:cols w:space="425"/>
            <w:docGrid w:type="lines" w:linePitch="312"/>
        </w:sectPr>
    </w:pPr>
</w:p>
''', format="openxml")


def generate_cover(metadata):
    cover_template = '''
<w:p>
    <w:pPr>
        <w:spacing w:before="0" w:after="0" w:line="240"/>
        <w:rPr>
            <w:rFonts w:ascii="仿宋_GB2312" w:eastAsia="仿宋_GB2312" w:hint="eastAsia"/>
            <w:sz w:val="24"/>
        </w:rPr>
    </w:pPr>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:before="0" w:after="0" w:line="240"/>
        <w:jc w:val="center"/>
        <w:rPr>
            <w:rFonts w:ascii="华文中宋" w:eastAsia="华文中宋" w:hAnsi="华文中宋"/>
            <w:sz w:val="52"/>
            <w:szCs w:val="52"/>
        </w:rPr>
    </w:pPr>
    <w:r>
        <w:rPr>
            <w:rFonts w:ascii="华文中宋" w:eastAsia="华文中宋" w:hAnsi="华文中宋"/>
            <w:sz w:val="52"/>
            <w:szCs w:val="52"/>
        </w:rPr>
        <w:t>{{{{logo_image}}}}</w:t>
    </w:r>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:before="0" w:after="0" w:line="240"/>
        <w:jc w:val="center"/>
        <w:rPr>
            <w:rFonts w:ascii="华文中宋" w:eastAsia="华文中宋" w:hAnsi="华文中宋"/>
            <w:sz w:val="52"/>
            <w:szCs w:val="52"/>
        </w:rPr>
    </w:pPr>
    <w:r>
        <w:rPr>
            <w:rFonts w:ascii="华文中宋" w:eastAsia="华文中宋" w:hAnsi="华文中宋"/>
            <w:sz w:val="52"/>
            <w:szCs w:val="52"/>
        </w:rPr>
        <w:t>{{{{school_name_image}}}}</w:t>
    </w:r>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:before="0" w:after="0" w:line="240"/>
        <w:jc w:val="center"/>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="30"/>
            <w:szCs w:val="28"/>
        </w:rPr>
    </w:pPr>
    <w:r>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="30"/>
            <w:szCs w:val="28"/>
        </w:rPr>
        <w:t>本科生毕业论文（设计）</w:t>
    </w:r>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:before="0" w:after="0" w:line="240"/>
        <w:jc w:val="center"/>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:sz w:val="28"/>
            <w:szCs w:val="28"/>
        </w:rPr>
    </w:pPr>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:before="0" w:after="0" w:line="240"/>
        <w:ind w:leftChars="225" w:left="2525" w:hanging="1985"/>
        <w:jc w:val="left"/>
        <!-- Original -->
        <!-- <w:ind w:firstLineChars="122" w:firstLine="539"/> -->
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="44"/>
            <w:szCs w:val="44"/>
        </w:rPr>
    </w:pPr>
    <w:r>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="44"/>
            <w:szCs w:val="44"/>
        </w:rPr>
        <w:t xml:space="preserve">题   目：</w:t>
    </w:r>
    <w:r>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="44"/>
            <w:szCs w:val="44"/>
        </w:rPr>
        <w:t xml:space="preserve">{title}</w:t>
    </w:r>
</w:p>
{title_break}
<w:p>
    <w:pPr>
        <w:spacing w:before="0" w:after="0" w:line="240"/>
        <w:ind w:firstLineChars="200" w:firstLine="643"/>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
    </w:pPr>
    <w:r>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
        <w:t xml:space="preserve">姓    名：{author}</w:t>
    </w:r>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:before="0" w:after="0" w:line="240"/>
        <w:ind w:firstLineChars="200" w:firstLine="643"/>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
    </w:pPr>
    <w:r>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
        <w:t>院    系：{school}</w:t>
    </w:r>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:before="0" w:after="0" w:line="240"/>
        <w:ind w:firstLineChars="200" w:firstLine="643"/>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
    </w:pPr>
    <w:r>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
        <w:t xml:space="preserve">专    业：{major}</w:t>
    </w:r>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:before="0" w:after="0" w:line="240"/>
        <w:ind w:firstLineChars="200" w:firstLine="643"/>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
    </w:pPr>
    <w:r>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
        <w:t xml:space="preserve">年    级：</w:t>
    </w:r>
    <w:r>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
        <w:t>{grade}</w:t>
    </w:r>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:before="0" w:after="0" w:line="240"/>
        <w:ind w:firstLineChars="200" w:firstLine="643"/>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
    </w:pPr>
    <w:r>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
        <w:t xml:space="preserve">学    号：</w:t>
    </w:r>
    <w:r>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
        <w:t>{studentID}</w:t>
    </w:r>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:before="0" w:after="0" w:line="240"/>
        <w:ind w:firstLineChars="200" w:firstLine="643"/>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
    </w:pPr>
    <w:r>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
        <w:t xml:space="preserve">指导教师：{adviser}</w:t>
    </w:r>
    <w:r>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
        <w:t>职称：{academicTitle}</w:t>
    </w:r>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:before="0" w:after="0" w:line="240"/>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:sz w:val="32"/>
            <w:szCs w:val="32"/>
        </w:rPr>
    </w:pPr>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:before="0" w:after="0" w:line="240"/>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:sz w:val="28"/>
            <w:szCs w:val="28"/>
        </w:rPr>
    </w:pPr>
</w:p>
<w:p>
    <w:pPr>
        <w:spacing w:before="0" w:after="0" w:line="240"/>
        <w:jc w:val="center"/>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:sz w:val="30"/>
            <w:szCs w:val="30"/>
        </w:rPr>
    </w:pPr>
    <w:r>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:sz w:val="30"/>
            <w:szCs w:val="30"/>
        </w:rPr>
        <w:t>{year} 年 {month} 月 {day} 日</w:t>
    </w:r>
</w:p>
<w:p>
    <w:pPr>
        <w:sectPr>
            <w:type w:val="nextPage"/>
            <w:pgSz w:w="11906" w:h="16838" w:code="9"/>
            <w:pgMar w:top="1440" w:right="1134" w:bottom="1440" w:left="1134" w:header="851" w:footer="992" w:gutter="0"/>
            <w:cols w:space="425"/>
            <w:docGrid w:type="lines" w:linePitch="312"/>
        </w:sectPr>
    </w:pPr>
</w:p>
'''
    title_paragraph_template = '''
<w:p>
    <w:pPr>
        <w:spacing w:before="0" w:after="0" w:line="240"/>
        <w:ind w:firstLineChars="122" w:firstLine="539"/>
        <w:rPr>
            <w:rFonts w:ascii="宋体" w:eastAsia="宋体" w:hint="eastAsia"/>
            <w:b/>
            <w:sz w:val="44"/>
            <w:szCs w:val="44"/>
        </w:rPr>
    </w:pPr>
</w:p>
'''

    date = datetime.datetime.strptime(metadata["date"], '%Y-%m-%d')
    wide_count, narrow_count, wide_len, narrow_len = east_asian_width_count(
        metadata["title"])

    return RawBlock(cover_template.format(
        title=metadata["title"],
        title_break=title_paragraph_template *
        2 if wide_len < 16 else title_paragraph_template,
        author='，'.join(metadata["author"]),
        school=metadata["school"],
        major=metadata["major"],
        grade=metadata["grade"],
        studentID=metadata["studentID"],
        adviser=metadata["adviser"].ljust(15 - len(metadata["adviser"]), ' '),
        academicTitle=metadata["academicTitle"],
        year=date.year,
        month=date.month,
        day=date.day,
    ), format="openxml")


def east_asian_width_count(s):
    '''
    计算字符串中 Unicode 东亚字符的宽、窄字符数目
    这是一个比较新的 Unicode 正则表达式，
    所以需要用比官方更勤快的 regex 包。

    理解东亚字符的宽、窄属性：https://www.unicode.org/reports/tr11/tr11-39.html
    Unicode 正则表达式：https://www.unicode.org/reports/tr18/
    '''
    pattern = regex.compile(r'\p{East Asian Width:Wide}')
    wide_count = len(pattern.findall(s))
    narrow_count = len(s) - wide_count
    return (wide_count, narrow_count, wide_count + round(narrow_count / 2, 2), wide_count * 2 + narrow_count)


def prepare(doc):
    pass


def action(elem, doc):
    '''
    处理（自创的） Tex 命令
    分页、目录
    '''
    if isinstance(elem, RawBlock):
        if elem.text == r"\pageBreak":
            if (doc.format == "docx"):
                debug("分页符")
                elem = page_break
        elif elem.text == r"\newSection":
            if (doc.format == "docx"):
                debug("分节符")
                elem = section_break
            else:
                elem = []
        elif elem.text == r"\newSectionInNewPage":
            if (doc.format == "docx"):
                debug("分节符（下一页）")
                elem = section_break_with_new_page
            else:
                elem = []
        elif elem.text == r"\cover":
            if (doc.format == "docx"):
                debug("封面")
                cover = generate_cover(doc.get_metadata())
                elem = [cover]
            else:
                elem = []
        elif elem.text == r"\statementOfOriginality":
            if (doc.format == "docx"):
                debug("原创性声明")
                elem = [statement_of_originality]
            else:
                elem = []
        elif elem.text == r"\abstract":
            if (doc.format == "docx"):
                debug("中文摘要")
                title = Div(*[Para(Str(doc.get_metadata()["title"]))],
                            attributes={"custom-style": "Title ZH"})
                abstract_title = Span(Str("【摘要】"), attributes={
                                      "custom-style": "Abstract Title ZH"})
                keywords_title = Span(Str("【关键词】"), attributes={
                                      "custom-style": "Abstract Title ZH"})
                abstract_text = "".join(
                    doc.get_metadata()["abstract"].replace('\n\n', '\n').split('\n'))
                keywords_text = "  ".join(doc.get_metadata()["keywords"])
                elem = [
                    title,
                    Para(SoftBreak()),
                    Div(*[Para(abstract_title, Space(), Str(abstract_text))],
                        attributes={"custom-style": "Abstract Content ZH"}),
                    Para(SoftBreak()),
                    Div(*[Para(keywords_title, Space(), Str(keywords_text))],
                        attributes={"custom-style": "Abstract Content ZH"})
                ]
            else:
                elem = []
        elif elem.text == r"\abstractEn":
            if (doc.format == "docx"):
                debug("英文摘要")
                title = Div(*[Para(Str(doc.get_metadata()["titleEn"]))],
                            attributes={"custom-style": "Title EN"})
                abstract_title = Span(Str("[Abstract]"), attributes={
                                      "custom-style": "Abstract Title EN"})
                keywords_title = Span(Str("[Keywords]"), attributes={
                                      "custom-style": "Abstract Title EN"})
                abstract_text = " ".join(
                    doc.get_metadata()["abstractEn"].replace('\n\n', '\n').split('\n'))
                keywords_text = ", ".join(doc.get_metadata()["keywordsEn"])
                elem = [
                    title,
                    Para(SoftBreak()),
                    Div(*[Para(abstract_title, Space(), Str(abstract_text))],
                        attributes={"custom-style": "Abstract Content EN"}),
                    Para(SoftBreak()),
                    Div(*[Para(keywords_title, Space(), Str(keywords_text))],
                        attributes={"custom-style": "Abstract Content EN"})
                ]
            else:
                elem = []
        elif elem.text == r"\toc":
            if (doc.format == "docx"):
                debug("目录")
                para = [Para(Str("目录"))]
                div = Div(*para, attributes={"custom-style": "TOC Heading"})
                # 目录下空两行，目录
                elem = [div, Para(SoftBreak()), Para(SoftBreak()), toc]
            else:
                elem = []
    '''
    处理 Markdown [TOC]
    '''
    if isinstance(elem, Para) and isinstance(elem.content[-1], Str) and elem.content[-1].text == '[TOC]':
        if (doc.format == "docx"):
            debug('Markdown [TOC]')
            para = [Para(Str("目录"))]
            div = Div(*para, attributes={"custom-style": "TOC Heading"})
            # 目录下空两行，目录
            elem = [div, Para(SoftBreak()), Para(SoftBreak()), toc]
    '''
    按要求处理特殊标题
    '''
    if isinstance(elem, Header):
        _contents = elem.content
        _lastcont = _contents[-1]
        if isinstance(_lastcont, Str) and _lastcont.text in ["引言", "致谢", "致谢语", "参考文献"] and doc.format == "docx":
            # 另起一页，四号黑体，居中，标题与内容之间空两行
            debug(_lastcont.text)
            para = [Para(Str(_lastcont.text))]
            div = Div(
                *para, attributes={"custom-style": "Introduction Title Like"})
            if _lastcont.text == '引言':
                # 因为引言紧跟目录，所以引言分页符需要是分节符（下一页）
                # 同时需要进行自定义，将前一节设为罗马数字页码
                special_section_break_with_new_page = RawBlock('''
<w:p>
    <w:pPr>
        <w:sectPr>
            <w:pgNumType w:fmt="upperRoman" w:start="1"/>
            <w:headerReference r:id="rId9" w:type="default"/>
            <w:footerReference r:id="rId10" w:type="default"/>
            <w:type w:val=\"nextPage\"/>
            <w:pgSz w:w="11906" w:h="16838" w:code="9"/>
            <w:pgMar w:top="1440" w:right="1797" w:bottom="1440" w:left="2364" w:header="851" w:footer="992" w:gutter="0"/>
        </w:sectPr>
    </w:pPr>
</w:p>
''', format="openxml")
                elem = [special_section_break_with_new_page,
                        div, Para(SoftBreak()), Para(SoftBreak())]
            else:
                elem = [page_break, div, Para(SoftBreak()), Para(SoftBreak())]
        elif isinstance(_lastcont, Str) and _lastcont.text == "附录" and doc.format == "docx":
            # 另起一页，四号黑体，居中
            debug(_lastcont.text)
            para = [Para(Str(_lastcont.text))]
            div = Div(
                *para, attributes={"custom-style": "Introduction Title Like"})
            elem = [page_break, div]
        elif isinstance(_lastcont, Str) and _lastcont.text in ["结论", "总结"] and doc.format == "docx":
            # 四号宋体，居中
            debug(_lastcont.text)
            para = [Para(Str(_lastcont.text))]
            div = Div(*para, attributes={"custom-style": "Conclusion Title"})
            elem = [div]
    '''
    '''
    # '''
    # 引号处理。
    # 默认情况下，引号会作为 Quoted 类型。
    # 中文双引号与西文双引号在 Unicode 中共用了编码。
    # 然而，在 Word 中，未定义语言的双引号将会被处理为西文，
    # 在我的模板中，西文会以 Times New Roman 字型处理，造成排版上的半宽。
    # 考虑到论文中难免会出现西文双引号的需要（如代码等），
    # 我并不想将双引号都硬编码为中文字符，
    # 也并没有什么很好的解决方法，唯有在前后加个空格了。
    # '''
    # if isinstance(elem, Quoted):
    #     return_list = [elem]
    #     if not isinstance(elem.prev, Space):
    #         return_list.insert(0, Space)
    #     if not isinstance(elem.prev, Space):
    #         return_list.append(Space)
    #     elem = return_list

    return elem


def finalize(doc):
    doc.metadata['geneInfo.project'] = 'XUJC-thesis-markdown'
    doc.metadata['geneInfo.url'] = 'https://github.com/foldblade/XUJC-thesis-markdown'
    doc.metadata['geneInfo.version'] = VERSION
    doc.metadata['geneInfo.datetime'] = datetime.datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S')


def main(doc=None):
    return run_filter(action,
                      prepare=prepare,
                      finalize=finalize,
                      doc=doc)


if __name__ == '__main__':
    main()
