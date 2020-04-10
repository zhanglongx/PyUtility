#!/usr/bin/env python3
# -*- coding:utf-8 -*-
 
import os, sqlite3
from tkinter import *
from tkinter.filedialog import (askopenfilename, asksaveasfilename, askdirectory)
from tkinter.ttk import *
 
file_dict = {}
DEFAULT_DB = r'd:\Users\zhlx\AppData\Roaming\baidu\BaiduNetdisk\users\53eb214008e09e15044b661ce42bdaff'

def select_db_file():
    _init_dir = DEFAULT_DB if os.path.exists(DEFAULT_DB) else '/'

    db_file = askopenfilename(initialdir = _init_dir,
                              title="请选择BaiduYunCacheFileV0.db文件", 
                              filetypes=[('db', '*.db')])
    db.set(db_file)
 
def select_save_file():
    save_file = asksaveasfilename(filetypes=[('文件', '*.txt')])
    f.set(save_file+".txt")
 
def select_cmp_dict():
    cmp_path = askdirectory(mustexist=True)
    d.set(cmp_path)
 
def query_baiduyun_filelist():
    _file = db.get()
    if not os.path.exists(_file):
        return

    conn = sqlite3.connect(_file)
    cursor = conn.cursor()
    cursor.execute("select * from cache_file")
    while True:
        value = cursor.fetchone()
        if not value:
            break
        path = value[2]
        name = value[3]
        if path not in file_dict:
            file_dict[path] = []
            file_dict[path].append(name)
        else:
            file_dict[path].append(name)

    conn.close()

    baidu_dict['values'] = sorted([k for k in file_dict.keys()])

def compare_local():
    _local = d.get()
    _remote = baidu_dict.get()

    if _remote == '':
        query_baiduyun_filelist()
        _remote = '/'

    # FIXME: dict == file will also be true
    print('Only in Local:\n')
    diff = [f for f in os.listdir(_local) if not f in file_dict[_remote]]
    [print("%s" % d) for d in diff]

    print("\n")
    print('Only in Remote:\n')
    diff = [f for f in file_dict[_remote] if not f in os.listdir(_local)]
    [print("%s" % d) for d in diff]

root = Tk()
root.title('百度云文件列表比较工具')

db_select = Button(root, text=' 选择DB文件 ',command=select_db_file)
db_select.grid(row=1,column=1,sticky=W,padx=(2,0),pady=(2,0))
db = StringVar()
db_path = Entry(root,width=80,textvariable = db)
db_path['state'] = 'readonly'
db_path.grid(row=1,column=2,padx=3,pady=3,sticky=W+E)

baidu_dict = Combobox(values='/', postcommand=query_baiduyun_filelist)
baidu_dict.grid(row=1, column=3, padx=1, pady=3, sticky=W+E)

cmp_directory = Button(root, text='选择对比目录', command=select_cmp_dict)
cmp_directory.grid(row=2, column=1, sticky=W, padx=(2,0), pady=(2,0))
d = StringVar()
cmp_path = Entry(root, width=80, textvariable=d)
cmp_path['state'] = 'readonly'
cmp_path.grid(row=2, column=2, padx=3, pady=3, sticky=W+E)

create_btn = Button(root, text=' 比较 ',command=compare_local)
create_btn.grid(row=3,column=1,columnspan=2,pady=(0,2))

root.columnconfigure(3, weight=1)
root.mainloop()
