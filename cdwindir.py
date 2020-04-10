#! /usr/bin/python3
import os, platform
import argparse

def make_path(args):
    '''
    XXX: non-greedy match searching, 
         so A1/B1/C1 will be priority than A1B1/C1
    '''
    if args.debug:
        print(args.path)

    s = args.path

    if platform.system() == 'Windows':
        # Debug on Windows only
        s = s.replace( '\\', '' )
    else:
        s = '/mnt/' + args.path
        s = s.replace( ':', '/' )

    while(1):
        if os.path.isdir(s):
            break

        if s[-1] == '/':
            i = s[:-1].rfind('/')
            if i == -1:
                raise ValueError

            # Input:  A1B1C2
            # Actual: A1B1/C2
            # Now:    A1/B1/C1
            s = s[:i] + s[i+1] + '/' + s[i+2:-1]
            continue

        i = s.rfind('/')
        if i == -1:
            s = s[0] + '/' + s[1:]
            continue

        if os.path.isdir(s[:i+1]):
            left = s[:i+1]
        else:
            left = s[:i]

        right = s[i+1:]

        s = left + right[0] + '/' + right[1:]

    print(s)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='win dir path')
    parser.add_argument("-d", "--debug", help="enable debug", action="store_true")
    args = parser.parse_args()

    make_path(args)

if __name__ == '__main__':
    main()