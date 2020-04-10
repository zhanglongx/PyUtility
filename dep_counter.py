#! python3
# coding: utf-8

'''
Find missing person(s) on a given list.

dep_counter.py input accept a list, format is not important.

eg. :
    1. split-ed by <cf> (strings copied from Excel directly usually 
       has this format):
       XX1
       XX2
       ...
       XXn

    2. split-ed by <space>:
       XX1 XX2 ... XXn

    3. or maybe other format
       ...

Then make comparison with the built-in person list, output the missing
person(s) on the input list and copy their email to clipboard

TODO: 
1. mail the missing person directly?
'''

import tkinter as tk
import re

(WIN_W, WIN_H) = (320, 240)
STICKY_FULL = tk.N + tk.S + tk.W + tk.E 
PAD_DEFAULT = 5

ALL_NAMES={
    '董家炜': 'dongjiawei@dvt.dvt.com',
    '赵晨辉': 'zhaochenhui@dvt.dvt.com',
    '李威扬': 'liweiyang@dvt.dvt.com',
    '王瑞霞': 'wangruixia@dvt.dvt.com',
    '韩飞':   'hanfei@dvt.dvt.com',
    '李学良': 'lixueliang@dvt.dvt.com',
    '柴立宝': 'chailibao@dvt.dvt.com',
    '马辉辉': 'mahuihui@dvt.dvt.com',
    '李树超': 'lishuchao@dvt.dvt.com',
    '李勇':   'liyong@dvt.dvt.com',
    '候本栋': 'houbendong@dvt.dvt.com',
    '冯凯凯': 'fengkaikai@dvt.dvt.com',
    '李新':   'lixin_40173@dvt.dvt.com',
    '王炳建': 'wangbingjian@dvt.dvt.com',
    '申胜军': 'shenshengjun@dvt.dvt.com',
    '姜东超': 'jiangdongchao@dvt.dvt.com'}

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self._master = master
        self._master.title('dep_counter')

        self._master.rowconfigure(0, weight=1)
        self._master.columnconfigure(0, weight=1)

        self.grid(row=0, column=0, sticky=STICKY_FULL)

        self._create_widgets()

        self._input.focus()
        self._master.bind('<Return>', func=self._run)

    def _create_widgets(self):
        # input
        self._input = tk.Text(self)
        self._input.grid(row=0, column=0)

        # button
        self._run_button = tk.Button(self, text='Run')
        self._run_button['command'] = self._run
        self._run_button.grid(row=1, column=0)

        for c in self.winfo_children(): 
            c.grid_configure(padx=PAD_DEFAULT, pady=PAD_DEFAULT)

    def _run(self, *args):
        _in_list = self._input.get(1.0, tk.END)

        # FIXME: duplicate name
        _missing = []
        for n in ALL_NAMES:
            _reg = r'%s' % n
            if len(re.findall(_reg, _in_list)) == 0:
                _missing.append(n)

        # display missing list
        self._input.delete(1.0, tk.END)
        self._input.insert(1.0, '\n'.join(_missing))

        # update email to clipboard
        self.clipboard_clear()
        self.clipboard_append(';'.join([ALL_NAMES[m] for m in _missing]))

        # summary report
        self._input.insert(tk.INSERT, '\n-----\n%d email(s) have been copied to clipboard' % len(_missing))

def main():
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
