#! python3
# coding: utf-8

'''
Make a summary of monthly assess

summary.py input accept a path contains one-year assess .xlsx file.
It use panadas do all read / merge operations.
'''

import os, re
import glob
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import pandas as pd

from tabulate import tabulate

TITLE='summary'
STICKY_FULL = tk.N + tk.S + tk.W + tk.E 
PAD_DEFAULT = 5

PATH='d:\\Users\\zhlx\\Dropbox\\Work\\Administrant\\7.部门工作\\2022'
#LISTS=('考核等级', '考核分数')
LISTS=('考核等级')

class summary(tk.Frame):
    def __init__(self, path, master=None):
        super().__init__(master)

        self._path = path

        self._master = master
        self._master.title(TITLE)

        self._master.rowconfigure(0, weight=1)
        self._master.columnconfigure(0, weight=1)

        self.grid(row=0, column=0, sticky=STICKY_FULL)

        self._create_widgets()

    def _create_widgets(self):
        # output
        self._wg_output = tk.Text(self)
        self._wg_output.grid(row=0, column=0, columnspan=2)

        # list-box
        self._col = tk.StringVar()
        self._wg_list = ttk.Combobox(self, textvariable=self._col)
        self._wg_list['state']  = 'readonly'
        self._wg_list['values'] = LISTS
        self._wg_list.current(0)
        self._wg_list.grid(row=1, column=0)

        # button
        self._wg_run = tk.Button(self, text='Run')
        self._wg_run['command'] = self._run
        self._wg_run.grid(row=1, column=1, sticky=tk.W)

        for c in self.winfo_children(): 
            c.grid_configure(padx=PAD_DEFAULT, pady=PAD_DEFAULT)

    def _run(self, *args):
        # FIXME: Dataframe only once
        _col = str(self._col.get())

        if not os.path.exists(self._path):
            raise OSError('%s not exists' % self._path)

        tab_list = dict()
        for f in glob.iglob(self._path + '/**/月度考核表_*.xls', recursive=True):
            try:
                month = re.search(r'(\d+)月', f).group(1)
            except:
                Warning('%s: filename is invalid' % f)
                continue

            # FIXME: header is hard-coded
            grade = pd.read_excel(f, header=2, index_col=0, usecols='B:F')

            # drop index as nan:
            # https://stackoverflow.com/questions/19670904/trying-to-drop-nan-indexed-row-in-dataframe
            grade = grade[grade.index.notnull()]
            grade.replace('B', np.NaN, inplace=True)
            grade.dropna(0, how='all', inplace=True)

            # FIXME: the only NaN is grade
            grade.fillna(' ', inplace=True)

            # FIXME: workaround to drop 'sum' row
            dropIndex = [i for i in grade.index.values if isinstance(i, int)]
            grade.drop(dropIndex, inplace=True)

            if month not in tab_list:
                tab_list[month] = grade
            else:
                tab_list[month] = pd.concat([tab_list[month], grade])

        objs = [tab_list[m] for m in tab_list]
        _tab = pd.concat(objs, axis=1, keys=tab_list.keys(), names=['月份', '分类'], sort=True)

        _tab = _tab.loc[slice(None), (slice(None), _col)]
        _tab.columns = _tab.columns.droplevel(level=1) 

        content = tabulate(_tab, headers=_tab.columns)

        _output = _col + '\n--------\n' + content
        # workaround: align table
        _output = re.sub(r'^(\w\w)\s', r'\1  ', _output, flags=re.M)

        self._wg_output.delete(1.0, tk.END)
        self._wg_output.insert(1.0, _output)

def main():
    root = tk.Tk()
    app = summary(path=PATH, master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
