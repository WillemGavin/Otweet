import tkinter as tk
import tweetDataCollection

win =tk.Tk()
# 设置主窗口
win.geometry('280x200')
win.title("Otweet")
# win.iconbitmap()
win.resizable(0,0)
# 新建文本标签
period_label = tk.Label(win,text="周      期：")
write_mode_label = tk.Label(win,text="写入方式：")
save_dir_label = tk.Label(win,text="输出目录：")
from_account_label = tk.Label(win,text="账户名称：")
proxy_label = tk.Label(win,text="代      理：")
information = tk.StringVar()
information_label = tk.Label(win, textvariable=information)
# grid()控件布局管理器，以行、列的形式对控件进行布局，后续会做详细介绍
period_label.grid(row=0)
write_mode_label.grid(row=1)
save_dir_label.grid(row=2)
from_account_label.grid(row=3)
proxy_label.grid(row=4)
information_label.grid(row=5, columnspan=2)

# 为文本标签，创建输入框控件
period_entry = tk.Entry(win)
period_entry.insert(0, "7")
write_mode_entry = tk.Entry(win)
write_mode_entry.insert(0, "a+")
save_dir_entry = tk.Entry(win)
save_dir_entry.insert(0, "Desktop/outputs")
from_account_entry = tk.Entry(win)
from_account_entry.insert(0, "@bitcoin")
proxy_entry = tk.Entry(win)
proxy_entry.insert(0, "None")

# 获取输入框的值
def run_scrape():
    update_information("正在爬取，请稍后……")
    period = period_entry.get()
    write_mode = write_mode_entry.get()
    save_dir = save_dir_entry.get()
    from_account = from_account_entry.get()
    proxy = proxy_entry.get()
    result = tweetDataCollection.tweet_data_collection(period=int(period), write_mode=write_mode, save_dir=save_dir, from_account=from_account, proxy=proxy)
    if result:
        update_information("数据获取完成！")

def update_information(information_msg):
    information.set(information_msg)
    information_label.update()

# 对控件进行布局管理，放在文本标签的后面
period_entry.grid(row=0, column=1)
write_mode_entry.grid(row=1, column=1)
save_dir_entry.grid(row=2, column=1)
from_account_entry.grid(row=3, column=1)
proxy_entry.grid(row=4, column=1)

button1 = tk.Button(text="提  交",command=run_scrape)

button1.grid(row=6, columnspan=2)
# 显示主窗口
win.mainloop()