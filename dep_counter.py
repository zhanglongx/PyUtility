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
    '董家炜': 'dongjiawei@sumavision.cn',
    '张迪':   'zhangdi@sumavision.cn',
    '赵晨辉': 'zhaochenhui@sumavision.cn',
    '韩飞':   'hanfei@sumavision.cn',
    '梁彪':   'liangbiao@sumavision.cn',
    '李学良': 'lixueliang@sumavision.cn',
    '马辉辉': 'mahuihui@sumavision.cn',
    '李树超': 'lishuchao@sumavision.cn',
    '冯凯凯': 'fengkaikai@sumavision.cn',
    '王健':   'wangjian@sumavision.cn',
    '王炳建': 'wangbingjian@sumavision.cn',
    '杨历凡': 'yanglifan@sumavision.cn',
    '庞志远': 'pangzhiyuan@sumavision.cn',
    '闫小超': 'yanxiaochao@sumavision.cn',
    '闫勇':   'yanyong@sumavision.cn',
    '王凯':   'wangkai@sumavision.cn',
    '刘灿':   'liucan@sumavision.cn',
    '李士勇': 'lishiyong@sumavision.cn',
    '张向辉': 'zhangxianghui@sumavision.cn',
    '程炜':   'chengwei@sumavision.cn',
    '魏永彬': 'weiyongbin@sumavision.cn',
    '王博':   'wangbo@sumavision.cn',
    '赵亚洋': 'zhaoyayang@sumavision.cn',
    '赵宁':   'zhaoning@sumavision.cn',
    '李绪晨': 'lixuchen@sumavision.cn',
    '卢文雄': 'luwenxiong@sumavision.cn',
    '付书山': 'fushushan@sumavision.cn',
    '姜东超': 'jiangdongchao@sumavision.cn'}

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
