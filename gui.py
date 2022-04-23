# encoding: utf-8

import codecs
import ctypes
from distutils.command.config import config
import json
import webbrowser
import sys
from tkinter import *
from tkinter import scrolledtext, filedialog, messagebox
from tkinter.ttk import *
import os
import subprocess
import processer

WHERE_SCRIPT = os.path.split(os.path.realpath(__file__))[0]


class myStdout():  # 重定向类
    def __init__(self):
        # 将其备份
        self.stdoutbak = sys.stdout
        self.stderrbak = sys.stderr
        # 重定向
        sys.stdout = self
        sys.stderr = self

    def write(self, info):
        # info信息即标准输出sys.stdout和sys.stderr接收到的输出信息
        debug_scrolledtext.insert('end', info)  # 在多行文本控件最后一行插入print信息
        debug_scrolledtext.update()  # 更新显示的文本，不加这句插入的信息无法显示
        # 始终显示最后一行，不加这句，当文本溢出控件最后一行时，不会自动显示最后一行
        debug_scrolledtext.see(END)

    def restoreStd(self):
        # 恢复标准输出
        sys.stdout = self.stdoutbak
        sys.stderr = self.stderrbak


# 输出重定向
mystd = myStdout()
# 创建窗口，main_window可替换成自己定义的窗口
main_window = Tk()
# 调用api设置成由应用程序缩放
ctypes.windll.shcore.SetProcessDpiAwareness(1)
# 调用api获得当前的缩放因子
ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
# 设置缩放因子
main_window.tk.call('tk', 'scaling', ScaleFactor/72)
main_window.resizable(0, 0)

BASE_DIR = StringVar()
MARKDOWN_FILE = StringVar()
METADATA_FILE = StringVar()
REF_FILE = StringVar()
OUTPUT_FILE = StringVar()
NO_BLANK_BACK_COVER = IntVar()


def select_file(*, defaultextension=None, filetypes=[]):
    '''
    选择文件
    '''
    file_path = filedialog.askopenfilename(
        defaultextension=defaultextension, filetypes=filetypes)
    return file_path


def select_dir():
    '''
    选择目录
    '''
    dir_path = filedialog.askdirectory()
    return dir_path


def save_as():
    '''
    另存为 
    '''
    dir_path = filedialog.asksaveasfilename(initialfile="result", defaultextension=".docx", filetypes=[
        ("Word 文档 (*.docx)", ".docx")])
    return dir_path


def set_base_dir(*, overwrite=None):
    '''
    设置基础目录
    '''
    if overwrite is None:
        BASE_DIR.set(select_dir())
        for file in os.listdir(BASE_DIR.get()):
            if (os.path.splitext(file)[-1][1:] == "md"):
                set_markdown_file(overwrite=os.path.join(BASE_DIR.get(), file))
            elif (os.path.splitext(file)[-1][1:] == "yaml"):
                set_metadata_file(overwrite=os.path.join(BASE_DIR.get(), file))
            elif (os.path.splitext(file)[-1][1:] == "bib"):
                set_ref_file(overwrite=os.path.join(BASE_DIR.get(), file))
    else:
        BASE_DIR.set(overwrite)
    entry_base_dir.after_idle(entry_base_dir.xview_moveto, 1)


def set_markdown_file(*, overwrite=None):
    '''
    设置 markdown 文件
    '''
    MARKDOWN_FILE.set(select_file(defaultextension=".md", filetypes=[
        ("Markdown (*.md)", ".md"), ("Markdown (*.markdown)", ".markdown"), ("全部 (*.*)", ".*")]) if overwrite is None else overwrite)
    entry_markdown_file.after_idle(entry_markdown_file.xview_moveto, 1)


def set_metadata_file(*, overwrite=None):
    '''
    设置元数据文件
    '''
    METADATA_FILE.set(select_file(defaultextension=".yaml", filetypes=[
        ("YAML (*.yaml)", ".yaml"), ("全部 (*.*)", ".*")]) if overwrite is None else overwrite)
    entry_metadata_file.after_idle(entry_metadata_file.xview_moveto, 1)


def set_ref_file(*, overwrite=None):
    '''
    设置 BibTeX 参考文献引文文件
    '''
    REF_FILE.set(select_file(defaultextension=".yaml", filetypes=[
        ("BibTeX Ref (*.bib)", ".bib"), ("全部 (*.*)", ".*")]) if overwrite is None else overwrite)
    entry_ref_file.after_idle(entry_ref_file.xview_moveto, 1)


def set_output_file(*, overwrite=None):
    '''
    设置输出文件
    '''
    OUTPUT_FILE.set(save_as() if overwrite is None else overwrite)
    entry_output_file.after_idle(entry_output_file.xview_moveto, 1)


def generate():
    '''
    调用 processer.py 进行处理
    '''
    print("\n*** 开始生成... ***\n")
    if (BASE_DIR.get() == ""
        or MARKDOWN_FILE.get() == ""
        or METADATA_FILE.get() == ""
            or OUTPUT_FILE.get() == ""):
        messagebox.showerror('错误', '存在尚未填充的字段。请填充所有带星号（*）的字段。')
        return
    gui_config = {
        "base_dir": BASE_DIR.get(),
        "markdown_file": MARKDOWN_FILE.get(),
        "metadata_file": METADATA_FILE.get(),
        "ref_file": REF_FILE.get(),
        "output_file": OUTPUT_FILE.get(),
        "no_blank_back_cover": NO_BLANK_BACK_COVER.get()
    }
    with open(os.path.join(WHERE_SCRIPT, ".gui_config.json"), 'w', encoding='utf-8') as gui_config_json:
        json.dump(gui_config, gui_config_json, indent=4, ensure_ascii=False)
    command = ('python "%s" ' % os.path.join(WHERE_SCRIPT, 'processer.py')
               + '-F "%s" ' % MARKDOWN_FILE.get()  # 输入 markdown 文件
               + ('-B "%s" ' %
                  REF_FILE.get() if REF_FILE.get() != "" else '')  # 引文文件
               + '-M "%s" ' % METADATA_FILE.get()  # 元数据文件
               + '-O "%s" ' % OUTPUT_FILE.get()  # 输出文件
               + ('--no-blank-back-cover ' if REF_FILE.get()
                  == 1 else '')  # 是否生成空白封底
               )
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         text=True)
    while subprocess.Popen.poll(p) is None:
        if(p.stdout is not None):
            print(p.stdout.read())
        # elif(p.stderr is not None):
        #     print(p.stderr.read())
    print("****************************\n\n")
    if(subprocess.Popen.poll(p) == 0):
        messagebox.showinfo('成功', 'docx 生成成功，位置：%s' % OUTPUT_FILE.get())
    else:
        messagebox.showerror('错误', '生成失败。')


def open_project_site():
    '''
    打开项目主页
    '''
    webbrowser.open(
        "https://github.com/foldblade/XUJC-thesis-markdown", new=0, autoraise=True)


def open_document_site():
    '''
    打开文档站
    '''
    webbrowser.open(
        "https://foldblade.github.io/XUJC-thesis-markdown", new=0, autoraise=True)


def generate_scaffold():
    '''
    生成脚手架
    '''
    dest = filedialog.askdirectory(title="选择目标文件夹")
    if (dest == ''):
        return
    if(len(os.listdir(dest)) != 0):
        messagebox.showerror('错误', '目标目录不为空。')
        return
    print("*** 开始生成脚手架... ***\n")
    os.removedirs(dest)
    command = 'python "%s" --new "%s"' % (
        os.path.join(WHERE_SCRIPT, 'processer.py'), dest)
    p = subprocess.Popen(command, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         text=True)
    while subprocess.Popen.poll(p) is None:
        if(p.stdout is not None):
            print(p.stdout.read())
        # elif(p.stderr is not None):
        #     print(p.stderr.read())
    print("****************************\n\n")
    if(subprocess.Popen.poll(p) == 0):
        messagebox.showinfo('成功', '脚手架生成成功，位置：%s' % dest)
    else:
        messagebox.showerror('错误', '生成失败。')


def check_update():
    '''
    检查更新
    '''
    maybe_update = processer.check_update()

    if(maybe_update) is not None:
        print("最新版本是: v%s" % maybe_update)
        print(
            "前往下载页：https://github.com/Foldblade/XUJC-thesis-markdown/releases/latest")
        response = messagebox.askquestion(
            '更新可用', '您当前使用的版本是：v%s，发现新版本：v%s，是否前往下载页？' % (processer.VERSION, maybe_update))
        if(response == 'yes'):
            webbrowser.open(
                "https://github.com/Foldblade/XUJC-thesis-markdown/releases/latest", new=0, autoraise=True)
            main_window.destroy()


main_menu = Menu(main_window)
# 新增命令菜单项，使用 add_command() 实现
main_menu.add_command(label="项目主页", command=open_project_site)
main_menu.add_command(label="查看文档", command=open_document_site)
main_menu.add_command(label="生成脚手架", command=generate_scaffold)
# 显示菜单
main_window.config(menu=main_menu)

main_window.after_idle(check_update)

# 组件
main_window.title('XUJC-thesis-markdown')
frame_main_window = Frame(main_window)
frame_main_window.pack(side='top', anchor='center', expand='yes')
label_base_dir = Label(frame_main_window, text='选择基础目录 *')
label_markdown_file = Label(frame_main_window, text='Markdown 文件 *')
label_metadata_file = Label(frame_main_window, text='元数据文件 *')
label_ref_file = Label(frame_main_window, text='BibTeX 格式引文文件  ')
label_output_file = Label(frame_main_window, text='输出 docx 文件另存为 *')
entry_base_dir = Entry(frame_main_window, width=50, textvariable=BASE_DIR)
entry_markdown_file = Entry(
    frame_main_window, width=50, textvariable=MARKDOWN_FILE)
entry_metadata_file = Entry(
    frame_main_window, width=50, textvariable=METADATA_FILE)
entry_ref_file = Entry(frame_main_window, width=50, textvariable=REF_FILE)
entry_output_file = Entry(frame_main_window, width=50,
                          textvariable=OUTPUT_FILE)
button_base_dir = Button(frame_main_window, text='...',
                         width=3, command=set_base_dir)
button_markdown_file = Button(
    frame_main_window, text='...', width=3, command=set_markdown_file)
button_metadata_file = Button(
    frame_main_window, text='...', width=3, command=set_metadata_file)
button_ref_file = Button(frame_main_window, text='...',
                         width=3, command=set_ref_file)
button_output_file = Button(frame_main_window, text='...',
                            width=3, command=set_output_file)
button_generate = Button(frame_main_window, text='生成', command=generate)
check_button_no_blank_back_cover = Checkbutton(
    frame_main_window, text="不要在封底添加空白页", variable=NO_BLANK_BACK_COVER)
debug_scrolledtext = scrolledtext.ScrolledText(
    frame_main_window, width=20, height=10)
debug_scrolledtext.insert(INSERT, "就绪。\n")

# 布局
label_base_dir.grid(row=0, column=0, pady=3, padx=3, sticky="e")
label_markdown_file.grid(row=1, column=0, pady=3, padx=3, sticky="e")
label_metadata_file.grid(row=2, column=0, pady=3, padx=3, sticky="e")
label_ref_file.grid(row=3, column=0, pady=3, padx=3, sticky="e")
label_output_file.grid(row=4, column=0, pady=3, padx=3, sticky="e")
entry_base_dir.grid(row=0, column=1, pady=3, padx=3)
entry_markdown_file.grid(row=1, column=1, pady=3, padx=3)
entry_metadata_file.grid(row=2, column=1, pady=3, padx=3)
entry_ref_file.grid(row=3, column=1, pady=3, padx=3)
entry_output_file.grid(row=4, column=1, pady=3, padx=3)
button_base_dir.grid(row=0, column=2, pady=3, padx=3)
button_markdown_file.grid(row=1, column=2, pady=3, padx=3)
button_metadata_file.grid(row=2, column=2, pady=3, padx=3)
button_ref_file.grid(row=3, column=2, pady=3, padx=3)
button_output_file.grid(row=4, column=2, pady=3, padx=3)
check_button_no_blank_back_cover.grid(row=5, column=1, columnspan=2, pady=3,
                                      padx=3, sticky="we")
button_generate.grid(row=6, column=0, columnspan=3, pady=3,
                     padx=3, sticky="nswe")
debug_scrolledtext.grid(row=7, column=0, columnspan=3, pady=3,
                        padx=3, sticky="nswe")


if os.path.exists(os.path.join(WHERE_SCRIPT, ".gui_config.json")):
    with open(os.path.join(WHERE_SCRIPT, ".gui_config.json"), "r", encoding="utf-8") as f:
        gui_config_json = json.load(f)
    MARKDOWN_FILE.set(gui_config_json["markdown_file"])
    main_window.update()
    set_base_dir(overwrite=gui_config_json["base_dir"])
    set_markdown_file(overwrite=gui_config_json["markdown_file"])
    set_metadata_file(overwrite=gui_config_json["metadata_file"])
    set_ref_file(overwrite=gui_config_json["ref_file"])
    set_output_file(overwrite=gui_config_json["output_file"])
    NO_BLANK_BACK_COVER.set(gui_config_json["no_blank_back_cover"])

main_window.mainloop()
