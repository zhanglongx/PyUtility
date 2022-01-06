#/usr/bin/python3

import codecs
import os
import winreg as reg

# names of all overlay icons that shall be boosted:

# The full identifiers menu
# https://en.wikipedia.org/wiki/List_of_shell_icon_overlay_identifiers

boost = """
    Tortoise1Normal
    Tortoise2Modified
    Tortoise3Conflict
    Tortoise6Deleted
    Tortoise7Added
    Tortoise8Ignored
    Tortoise9Unversioned
    DropboxExt01
    DropboxExt02
    DropboxExt07
    OneDrive4
"""

boost = set(boost.split())

backup_filename = 'IconOverlayBackup.reg'

key = (r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion'
       r'\Explorer\ShellIconOverlayIdentifiers')
sub_key = key.split('\\', 1)[1]

def main():

    with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, sub_key) as base:
        backup = []
        names = set()
        deletes = []
        renames = []
        i = 0
        while True:
            try:
                name = reg.EnumKey(base, i)
                value = reg.QueryValue(base, name)
            except OSError:
                break
            backup.append((name, value))
            core = name.strip()
            if core in names:
                deletes.append(name)
            else:
                names.add(core)
                if core in boost:
                    core = ' ' + core
                if core != name:
                    renames.append((name, core))
            i += 1

        if deletes or renames:
            print('Write backup file', backup_filename)
            with codecs.open(backup_filename, 'w', 'utf_16_le') as backup_file:
                wr = backup_file.write
                wr('\ufeff')
                wr('Windows Registry Editor Version 5.00\r\n\r\n')
                wr('[{}]\r\n\r\n'.format(key))
                for name, value in backup:
                    wr('[{}\\{}]\r\n'.format(key, name))
                    wr('@="{}"\r\n\r\n'.format(value))

            for name in deletes:
                print('Delete', repr(name))
                reg.DeleteKey(base, name)
            for old_name, new_name in renames:
                print('Rename', repr(old_name), 'to', repr(new_name))
                value = reg.QueryValue(base, old_name)
                reg.CreateKey(base, new_name)
                reg.SetValue(base, new_name, reg.REG_SZ, value)
                reg.DeleteKey(base, old_name)

            # print('Restart Windows Explorer')
            # if not os.system('taskkill /F /IM explorer.exe'):
            #     os.system('start explorer.exe')

        else:
            print('Nothing to rename')

if __name__ == '__main__':
    main()

    print("Hit Enter to continue ...")
    input()
