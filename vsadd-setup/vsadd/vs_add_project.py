# -*- coding: utf-8 -*-

import os
import argparse
import subprocess as sub
import xml.etree.ElementTree as ET

from abc import (ABCMeta, abstractmethod)

class _base():
    def __init__(self, path='.', extra=None):
        self.path  = path
        self.extra = extra

    @abstractmethod
    def insert(self, vs_file):
        raise NotImplementedError

    def __collect(self, types=None):
        p = sub.Popen(['git', 'ls-files', '--recurse-submodules'], stdout=sub.PIPE, \
                      cwd=self.path)     
        (out, _) = p.communicate()

        if p.returncode == 0:
            files = out.decode('utf-8').splitlines()
        else:
            files = []

        if self.extra: 
            # extra files
            extras = []
            for e in self.extra:
                for (root, _, subfiles) in os.walk(os.path.join(self.path, e)):
                    extras.extend([os.path.join(root, f) for f in subfiles])
            
            # check extra files only
            files.extend([os.path.relpath(f, self.path) for f in extras if os.path.splitext(f)[1] in types])

        def __uniq(x):
            return list(set(x))

        # It's in Windows world anyway :(
        return __uniq([f.replace('/', '\\') for f in files])

    def __modify(self, vs_file, files):
        vs_file = os.path.join(self.path, vs_file)
        if not os.path.exists(vs_file):
            raise OSError('%s not exists' % vs_file)

        ET.register_namespace('', 'http://schemas.microsoft.com/developer/msbuild/2003')

        # <Project/>
        vs   = ET.parse(vs_file)
        root = vs.getroot()

        b_found = 0
        for e in root.findall('{http://schemas.microsoft.com/developer/msbuild/2003}ItemGroup'):
            if e.get('Label') == 'ProjectConfigurations':
                continue

            if e.find('InterpreterReference'):
                continue

            if b_found:
                root.remove(e)

            # remove previous
            e.clear()

            try:
                [e.append(sube) for sube in [self.add(f) for f in files if not f == '']]
            except TypeError:
                # not files to insert
                pass

            b_found = 1

        if not b_found:
            Warning("can't find ItemGroup, done with nothing")
            return

        vs.write(vs_file, encoding='utf-8', xml_declaration=True)

    @abstractmethod
    def add(self, f):
        raise NotImplementedError

class vcxproj(_base):
    def __init__(self, path='.', extra=None):
        return super().__init__(path=path, extra=extra)

    def insert(self, vs_file):
        files = super()._base__collect(types=['Makefile', '.c', '.h', '.cpp', '.hpp', '.cu'])

        self._base__modify(vs_file, files)

    def add(self, f):
        return ET.Element('ClCompile', attrib={'Include' : f})

class pyproj(_base):
    def __init__(self, path='.', extra=None):
        return super().__init__(path=path, extra=extra)

    def insert(self, vs_file):
        files = super()._base__collect(types=['.py'])

        self._base__modify(vs_file, files)

    def add(self, f):
        if os.path.splitext(f)[1] in ['.py']:
            return ET.Element('Compile', attrib={'Include' : f})
        else:
            return ET.Element('Content', attrib={'Include' : f})

def main(argv=None):
    # Get command line arguments
    parser = argparse.ArgumentParser(description='''add git files and extra files to vs project(.vcxproj, .pyproj)''')

    parser.add_argument('-e', '--extra', type=str, nargs=1, help='extra dirs')
    parser.add_argument('path',  default='.', type=str, nargs='?', help='path contains vs project file')

    args = parser.parse_args()

    path  = args.path
    extra = args.extra

    if not os.path.exists(path):
        raise OSError('%s not exists' % path)

    for f in os.listdir(path):
        if os.path.splitext(f)[1] == '.vcxproj':
            vcxproj(path=path, extra=extra).insert(f)
        elif os.path.splitext(f)[1] == '.pyproj':
            pyproj(path=path, extra=extra).insert(f)

if __name__ == '__main__':
    main()
