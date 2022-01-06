# python
# -*- coding: utf-8 -*-

import os, sys, shutil, time, json, argparse
import platform
import re
import zipfile as zip
import subprocess as sub
from docx import Document

TMP = '.tmp'

# README:
# 1. 检查配置文件，如achieve.json文件，是否含有不需要存档的项目，
#    是否有新项目没有加入
# 
# 2. 保证所有的项目处于正确的分支下
#
# 3. 执行本程序

class achieve:
    def __init__(self):
        self.date = time.strftime('%Y%m%d', time.localtime())

    def run(self, jsonfile):
        with open(jsonfile) as f:
            config = json.load(f)

        if os.path.exists(TMP):
            shutil.rmtree(TMP)
        
        os.mkdir(TMP)

        root_doc = {}

        for p in config['projects']:
            _name = p['name']

            _uri = p['uri']

            if not os.path.exists(os.path.join(_uri, '.git')):
                raise ValueError('%s is not a git repository' % _uri)

            # For version
            # FIXME: using dynamic action
            _ = sub.Popen(['git', 'pull', '--rebase'], cwd=_uri)
            _.wait()

            if 'version' in p:
                _ = re.search(r'\d\.\d\.\d', p['version'])
                if not _ is None:
                    _ver = _[0]
                else:
                    try:
                        _version_file = os.path.join(_uri, p['version'])
                        _ver = self.__version(file=_version_file, 
                                              pattern=r'_version\[.*(\d\.\d\.\d)')
                    except OSError:
                        _ver = 'n/a'
            else:
                _ver = 'n/a'

            print('packing %s %s ... ' % (_name, _ver))

            os.mkdir(os.path.join(TMP, _name))

            _zip = os.path.join(TMP, _name, _name + '.zip')

            self.__export(uri=_uri, output=_zip, extra=None, update=True)

            self.__docx(_name, False, **self.__check_dir(uri=_uri, ver=_ver, **p['dirs']))

            # for final doc
            root_doc[_name] = p['descript']

        self.__docx('readme-' + self.date + '-研发三部', True, **root_doc)

    def __export(self, uri, output, extra=None, **kwargs):
        '''
        export a local git repository files into output file in zip format
        @params:
        uri: {str}
            git repository
        output: {str}
            output file name
        extra: {list[str] or str}
            extra directories
        update: {boolean}
            reserved
        '''
        files = self.__git_lsfiles(uri=uri, extra=extra, **kwargs)

        with zip.ZipFile(output, 'w') as z:
            for f in files:   
                try:
                    z.write(os.path.join(uri, f), f)
                except OSError:
                    # XXX: skip link file
                    continue

    def __git_lsfiles(self, uri, extra=None, **kwargs):
        '''
        behavior like `git ls-files`, additional with extra directories
        @params:
        uri: {str}
            git repository
        extra: {list[str]}
            extra directories in uri, must use os.path.join() if has more than one
            depth 
        update: {boolean}
            reserved
        '''
        if not os.path.exists(os.path.join(uri, '.git')):
            raise ValueError('%s is not a git repository' % uri)

        # Add git control-ed files
        p = sub.Popen(['git', 'ls-files'], stdout=sub.PIPE, cwd=uri)
        (files, _) = p.communicate()

        files = files.decode('utf-8').splitlines()

        # Add extra 
        extra_files = []
        if not extra is None:
            print('extra maybe not be updated', file=sys.stderr)
            if isinstance(extra, str):
                extra = [extra]

            for e in extra:
                extra_files += self.__find(path=os.path.join(uri, e))

        # use abspath to remove duplicate files
        all = [os.path.abspath(os.path.join(uri, f)) for f in files] + extra_files
        files = [os.path.relpath(f, start=uri) for f in list(set(all))]

        return files

    def __check_dir(self, uri, ver, **key):
        r = {}

        for k in key:
            if os.path.exists(os.path.join(uri, k)):
               r[k] = key[k]
               r[k]['version'] = ver

        return r

    def __docx(self, name, is_root=False, **key):

        if len(key) == 0:
            return

        doc = Document()

        # first col in key
        title = list(key[list(key.keys())[0]])

        table = doc.add_table(rows=len(key)+1, cols=len(title)+1)
        row = 0

        for k in key:
            col = 0
            table.rows[row].cells[col].text = k

            for t in title:
                col += 1
                table.rows[row].cells[col].text = key[k][t]

            row += 1

        table.style = 'TableGrid'

        if is_root == True:
            doc.save(os.path.join(TMP, name + '.docx'))
        else:
            doc.save(os.path.join(TMP, name, name + '.docx'))

    def __find(self, path, exclude_dir='.git', exclude_ext=['.o']):
        '''
        Unix-like find, empty dir will be skiped
        return *absolute* path
        @params:
        path: {str}
            find files in path
        exclude_dir: {str}
            exclude files dirname contains <exclude_dir>
        exclude_ext: {list[str]}
            exclude files when extension is in <exclude_ext>
        '''
        output = []
        for (root, dirs, files) in os.walk(path):
            if exclude_dir in root.split(os.sep):
                continue

            [output.append(os.path.join(root, f)) for f in files \
                if not os.path.splitext(f)[-1] in exclude_ext]

        return output

    def __version(self, file, pattern):
        '''
        search version info in file
        @params:
        file: {str}
            file to search
        pattern: {str}
            regular expression pattern to search version
        '''
        if not os.path.exists(file):
            raise OSError('%s not exists' % file)

        try:
            with open(file, mode='r', encoding='utf-8') as f:
                text = f.read()
        except UnicodeDecodeError:
            with open(file, mode='r', encoding='gb2312') as f:
                text = f.read()

        g = re.search(pattern, text, flags=re.M) 
        if g: 
            return g[1]

if __name__ == '__main__':
    if platform.system() == 'Windows':
        raise OSError('Windows is not supported, due to make in git-pull stage')

    parser = argparse.ArgumentParser(description='''achieve rd achiever automaticlly\n
                                                    acheive_example.txt will be a good start
                                                 ''')
    parser.add_argument('jsonfile', default='achieve.json', type=str, nargs='?', help='.json config file(see acheive_example.txt)')

    jsonfile = parser.parse_args().jsonfile

    a = achieve()
    a.run(jsonfile)