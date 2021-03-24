import tkinter as tk
import win32ui
from train import predict

window = tk.Tk()#设置窗口
window.geometry('250x120')#窗口大小
window.title('文本过滤器')#窗口标题
tk.Label(window, text='文件:', ).place(x=10, y=10)#文件标签
tk.Label(window, text='类别:', ).place(x=10, y=50)#类别标签
var_file_name = tk.StringVar()#文件名变量
tk.Entry(window,textvariable=var_file_name).place(x=70,y=10)#文件名文本框
var_class = tk.StringVar()#类别变量
tk.Entry(window, textvariable=var_class).place(x=70,y=50)#类别名文本框

def do_predict():#点击打开按钮运行
    dlg = win32ui.CreateFileDialog(1) # 1表示打开文件对话框
    dlg.SetOFNInitialDir('C:/') # 设置打开文件对话框中的初始显示目录
    dlg.DoModal()
    filename = dlg.GetPathName() #得到选择文件名
    result = predict(filename)[0]#预测文件
    var_class.set (result)   # 显示类别		
    var_file_name.set(filename.split('\\')[-1]) #分割路径，显示文件名
tk.Button(window,text='打开',command=do_predict).place(x=110, y=80)#打开按钮
window.mainloop()#显示窗口