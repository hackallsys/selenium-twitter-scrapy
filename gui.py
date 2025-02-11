import tkinter as tk
from tkinter import scrolledtext
import sys
import subprocess





class TextRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, str):
        self.widget.insert(tk.END, str)
        self.widget.see(tk.END)

    def flush(self):
        pass


def query_info():
    username = entry.get()
    result = f"你查询的X用户名是: {username}"
    print(result)

    try:
        # 这里假设要运行的脚本文件名为 main.py，你可以根据实际情况修改
        script_path = "main.py"
        # 运行脚本文件，并将用户名作为 --search-user 参数传递，捕获输出
        process = subprocess.Popen(['venv\\Scripts\\python.exe', script_path, '--search-user', username],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        output, _ = process.communicate()
        print(f"脚本运行输出:\n{output}")
    except Exception as e:
        print(f"运行脚本时出错: {e}")



root = tk.Tk()
root.title("用户名查询")

label = tk.Label(root, text="用户名:")
label.grid(row=0, column=0, padx=5, pady=10)

entry = tk.Entry(root)
entry.grid(row=0, column=1, padx=5, pady=10)

button = tk.Button(root, text="查询", command=query_info)
button.grid(row=0, column=2, padx=5, pady=10)

output_label = tk.Label(root, text="输出信息:")
# 将 output_label 放置在第 1 行第 0 列
output_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

output_text = scrolledtext.ScrolledText(root, width=40, height=10)
# 让 output_text 跨 3 列，从第 2 行第 0 列开始
output_text.grid(row=2, column=0, columnspan=3, padx=5, pady=10)

sys.stdout = TextRedirector(output_text)

root.mainloop()

sys.stdout = sys.__stdout__