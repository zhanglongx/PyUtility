#! python3
# coding: utf-8

'''
Make a summary of monthly assess

summary.py input accept a path contains one-year assess .xlsx file.
It use panadas do all read / merge operations.
'''

import os, re
import glob, argparse
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import pandas as pd

TITLE='summary'
STICKY_FULL = tk.N + tk.S + tk.W + tk.E 
PAD_DEFAULT = 5

PATH='d:\\Users\\zhlx\\Documents\\stuff\\7.部门工作\\2019'
LISTS=('考核等级', '考核分数')

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

        _tab_list = []
        _month_list = []
        for f in glob.iglob(self._path + '/**/月度考核表_*.xls', recursive=True):
            try:
                _month = re.search(r'(\d+)月', f).group(0)
            except:
                Warning('%s: filename is invalid' % f)
                continue

            _month_list.append(_month)

            # FIXME: header is hard-coded
            _month_tab = pd.read_excel(f, header=2, index_col=0, usecols='B:F')

            # drop index as nan:
            # https://stackoverflow.com/questions/19670904/trying-to-drop-nan-indexed-row-in-dataframe
            _month_tab = _month_tab[_month_tab.index.notnull()]
            _month_tab.replace('B', np.NaN, inplace=True)
            _month_tab.dropna(0, how='all', inplace=True)

            # FIXME: the only NaN is grade
            _month_tab.fillna(' ', inplace=True)

            _tab_list.append(_month_tab)

        _tab = pd.concat(_tab_list, axis=1, keys=_month_list, names=['月份', '分类'], sort=True)

        _tab = _tab.loc[slice(None), (slice(None), _col)]
        _tab.columns = _tab.columns.droplevel(level=1) 

        _output = _col + '\n--------\n' + _tab.to_string(col_space=4, index_names=False)
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