import threading
import pyperclip
import time
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, Menu, Toplevel, Checkbutton, IntVar
from pynput import keyboard

class AutoTyper:
    def __init__(self, master):
        self.master = master
        self.content = StringVar(value="请输入刷屏内容")
        self.frequency_ms = StringVar(value="1000")  # 默认频率为1000毫秒（1秒）
        self.repeat_count = StringVar(value="100")  # 默认刷屏次数为100次
        self.show_suffix_var = IntVar(value=0)  # 默认不显示后缀
        self.copy_content = ""
        self.running = False
        self.count = 0  # 用于记录当前刷屏次数
        self.suffix_number = 0  # 用于记录后缀的数字

        # 设置窗口
        self.master.title("刷屏器")
        self.master.geometry("350x250")

        # 创建控件
        Label(master, text="内容：").pack()
        self.content_entry = Entry(master, textvariable=self.content)
        self.content_entry.pack()
        Label(master, text="频率(毫秒)：").pack()
        self.frequency_entry = Entry(master, textvariable=self.frequency_ms)
        self.frequency_entry.pack()
        Label(master, text="刷屏次数：").pack()
        self.repeat_count_entry = Entry(master, textvariable=self.repeat_count)
        self.repeat_count_entry.pack()
        self.show_suffix_checkbox = Checkbutton(master, text="显示刷屏次数后缀", variable=self.show_suffix_var, onvalue=1, offvalue=0)
        self.show_suffix_checkbox.pack()
        self.start_button = Button(master, text="开始", command=self.start_typing)
        self.start_button.pack()

        # 创建菜单
        self.create_menu()

    def create_menu(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        # 文件菜单
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="退出或结束刷屏", command=self.quit)

        # 编辑菜单
        edit_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="编辑", menu=edit_menu)
        edit_menu.add_command(label="编辑内容和频率", command=self.edit_settings)

        # 帮助菜单
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="帮助", command=lambda: messagebox.showinfo("帮助", "请访问https://github.com/GY-GZW/Screen-swipe/issues\n您可以把问题提交到这里"))

        # 关于菜单
        about_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="关于", menu=about_menu)
        about_menu.add_command(label="关于", command=lambda: messagebox.showinfo("关于", "果园编程(原果园工作室)制作"))
        # 更新菜单
        up_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="更新", menu=up_menu)
        up_menu.add_command(label="更新", command=lambda: messagebox.showinfo("更新", "3.9.0（更新显示后缀功能）"))

    def edit_settings(self):
        self.settings_window = Toplevel(self.master)
        self.settings_window.title("编辑设置")
        self.settings_window.geometry("350x300")

        Label(self.settings_window, text="内容：").pack()
        self.content_entry_settings = Entry(self.settings_window, textvariable=self.content)
        self.content_entry_settings.pack()

        Label(self.settings_window, text="频率(毫秒)：").pack()
        self.frequency_entry_settings = Entry(self.settings_window, textvariable=self.frequency_ms)
        self.frequency_entry_settings.pack()

        Label(self.settings_window, text="刷屏次数：").pack()
        self.repeat_count_entry_settings = Entry(self.settings_window, textvariable=self.repeat_count)
        self.repeat_count_entry_settings.pack()

        self.show_suffix_checkbox_settings = Checkbutton(self.settings_window, text="显示刷屏次数后缀", variable=self.show_suffix_var, onvalue=1, offvalue=0)
        self.show_suffix_checkbox_settings.pack()

        Button(self.settings_window, text="保存", command=self.save_settings).pack()

    def save_settings(self):
        # 这里可以添加保存设置的逻辑，如果需要的话
        self.settings_window.destroy()

    def start_typing(self):
        if not self.running:
            self.copy_content = self.content.get()
            if self.copy_content:
                self.count = int(self.repeat_count.get())
                if self.count > 0:
                    messagebox.showinfo("提示", "按下确定后2秒内点击聊天窗口以获取句柄，之后将开始刷屏")
                    self.start_button.config(text="停止")
                    threading.Thread(target=self.wait_and_type).start()
                else:
                    messagebox.showwarning("警告", "刷屏次数必须大于0")
            else:
                messagebox.showwarning("警告", "请输入刷屏内容")
        else:
            self.stop_typing(False)

    def wait_and_type(self):
        time.sleep(2)  # 等待2秒
        self.running = True
        self.suffix_number = 1  # 重置后缀数字
        self.type_content()

    def type_content(self):
        while self.running and self.count > 0:
            if self.show_suffix_var.get() == 1:  # 判断是否显示后缀
                typed_content = f"{self.copy_content}{self.suffix_number}"
                self.suffix_number += 1
            else:
                typed_content = self.copy_content
            pyperclip.copy(typed_content)
            keyboard.Controller().type(typed_content)
            keyboard.Controller().type('\n')
            time.sleep(float(self.frequency_ms.get()) / 1000.0)  # 将毫秒转换为秒
            self.count -= 1  # 刷屏次数减1
        if self.count == 0 and self.running:
            self.stop_typing(True)  # 刷屏次数完成后停止

    def stop_typing(self, normal_stop):
        self.running = False
        self.start_button.config(text="开始")
        if normal_stop:
            messagebox.showinfo("完成", "刷屏已完成")
        else:
            messagebox.showinfo("紧急停止", "已紧急停止")

    def quit(self):
        self.stop_typing(False)
        self.master.destroy()

if __name__ == "__main__":
    root = Tk()
    app = AutoTyper(root)
    root.mainloop()
