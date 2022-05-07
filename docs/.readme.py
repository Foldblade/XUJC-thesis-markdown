# encoding= utf-8

import re
import os

WHERE_SCRIPT = os.path.split(os.path.realpath(__file__))[0]

f = open(os.path.join(WHERE_SCRIPT, ".readme-template.md"), "r", encoding='UTF-8')
readme_template = f.read()
f.close()

files = [
    "three-elements",
    "quick-start",
    "start-writing-from-the-scaffold",
    "gui",
    "writing-guide",
    "modify-template-style",
    "command-line",
    "after-generation",
    "implement",
    "Q-and-A",
    "extended-reading",
    "appendix",
]

contents = {}


def process_to_emoji(src):
    src = src.replace('\r\n', '\n')
    warning = re.compile(r'!!![\s]?warning\n[\s]{4,}')
    failure = re.compile(r'!!![\s]?failure\n[\s]{4,}')
    danger = re.compile(r'!!![\s]?danger\n[\s]{4,}')
    info = re.compile(r'!!![\s]?info\n[\s]{4,}')
    tip = re.compile(r'!!![\s]?tip\n[\s]{4,}')
    src = re.sub(warning, "> ⚠ 注意：", src)
    src = re.sub(failure, "> ❌ 失败：", src)
    src = re.sub(danger, "> 🚨 危险：", src)
    src = re.sub(info, "> ℹ️ 信息：", src)
    src = re.sub(tip, "> 💡 提示：", src)
    return src


for file in files:
    f = open(os.path.join(WHERE_SCRIPT, file + ".md"), "r", encoding='UTF-8')
    contents[file] = f.read()
    contents[file] = process_to_emoji(contents[file])
    f.close()
    readme_template = readme_template.replace("{{%s}}" % file, contents[file])

# f = open(os.path.join(WHERE_SCRIPT, "readme.md"), "w", encoding='UTF-8')
# f.write(readme_template)
# f.close()

f = open(os.path.join(WHERE_SCRIPT, "../demo/readme.md"), "w", encoding='UTF-8')
f.write(readme_template.replace("readme.assets", "../docs/readme.assets"))
f.close()

print("Done!")
