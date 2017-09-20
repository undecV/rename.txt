#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import json

# import terminaltables


__author__ = "undecV"
__copyright__ = "Copyright 2017, undecV"
__credits__ = ["undecV"]
__license__ = ""
__version__ = "1.0.0"
__maintainer__ = ""
__email__ = ""
__status__ = ""

PROJ_NAME = "rename.txt"
FILE_PATH = os.path.dirname(__file__)
FILE_NAME = os.path.splitext(os.path.basename(__file__))[0]
DESCRIPTION = "Rename files or dirs via your text editor."


opt = {"LS_FILE_PATH":  "./RENAME.json",
       "TEXT_EDITOR_PATH": "D:\\Program Files (x86)\\Notepad++\\notepad++.exe",
       "TEXT_EDITOR_ARGS": "{LS_FILE_PATH}"}


def main(argv):
    _, args = arg_parse(argv)

    # LS
    items = []
    items_dir = []
    items_base = []

    for path in args.path[1:]:
        if os.path.exists(path):
            items.append(path)
            dirname, basename = os.path.split(path)
            items_dir.append(dirname)
            items_base.append(basename)
        else:
            print("[WARNING] Path not exists: {0}".format(path))

    items_count = len(items)
    if items_count == 0:
        print("[ERROR] Too few available path.")
        exit(0)

    if args.edit_path:
        json_content = json.dumps(items, sort_keys=True, indent=0, ensure_ascii=False)
    else:
        json_content = json.dumps(items_base, sort_keys=True, indent=0, ensure_ascii=False)

    print(json_content)

    try:
        ls_file = open(opt["LS_FILE_PATH"], "w", encoding="utf-8")
        ls_file.write(json_content)
        ls_file.close()
    except IOError:
        print("[ERROR] File write failed.")
        exit(-1)

    os.system('"{0}" {1}'.format(opt["TEXT_EDITOR_PATH"],
                                 opt["TEXT_EDITOR_ARGS"].format(LS_FILE_PATH=opt["LS_FILE_PATH"])))
    print("Edit, and save the file `{0}`, then hit `ENTER` key...".format(opt["LS_FILE_PATH"]))
    input()

    # Load edited items
    items_e = []
    try:
        ls_file = open(opt["LS_FILE_PATH"], "r", encoding="utf-8")
        items_e = json.load(ls_file)
        ls_file.close()
    except IOError:
        print("[ERROR] File read failed.")
        exit(-1)

    if len(items_e) != items_count:
        print("[ERROR] Vary in amount.")
        exit(-1)

    # List
    # items     items_dir       items_base
    # items_e   items_e_dir     items_e_base
    items_e_dir = []
    items_e_base = []

    if args.edit_path:
        for item_e in items_e:
            dirname, basename = os.path.split(item_e)
            items_e_dir.append(dirname)
            items_e_base.append(basename)
    else:
        items_e_base = items_e.copy()
        items_e_dir = items_dir
        for i in range(0, len(items_e)):
            items_e[i] = os.path.join(items_e_dir[i], items_e_base[i])

    # Make the table
    if args.edit_path:
        for i in range(0, items_count):
            print("{0:03d}/{1:03d} - {2}\n       -> {3}".format(i, items_count, items[i], items_e[i]))
    else:
        for i in range(0, items_count):
            print("{0:03d}/{1:03d} - {2}\n       -> {3}".format(i, items_count, items_base[i], items_e_base[i]))
        # table_data = [["Index", "Src", "Dst"]]
        # for i in range(0, items_count):
        #     table_data.# append(["{0:03d}/{1:03d}".format(i, items_count), items_base[i], items_e_base[i]])
        # table = terminaltables.AsciiTable(table_data)
        # table.outer_border = False
        # print(table.table)
    print()

    # Confirmation
    if yes(input("Is it correct? Yes or not: ")) is False:
        print("[EXIT] Canceled.\n")
        exit(0)

    # Rename
    for i in range(0, items_count):
        print("{0:03d}/{1:03d} - ".format(i, items_count), end='')
        if items[i] == items_e[i]:
            print("Not changed.")
            continue
        if os.path.exists(items_e[i]):
            print("[ERROR] New name already be used.")
            continue
        try:
            os.rename(items[i], items_e[i])
        except OSError:
            print("[ERROR] Cannot rename the file.")
            continue
        print("OK.")

    try:
        os.remove(opt["LS_FILE_PATH"])
    except IOError:
        print("[ERROR] Cannot remove the file.")
    print("Done.")


def arg_parse(argv):
    parser = argparse.ArgumentParser(description="{description}".format(description=DESCRIPTION),
                                     epilog="Present by {author}.".format(author=__author__))
    parser.add_argument("path", metavar="PATH", type=str, nargs='+',
                        help="Path of files witch need to be renamed.")
    # parser.add_argument("-y", "--yes", action="store_true",
    #                     help="Ignore confirmation step, **WARNING!** something irreversible may happen.")
    parser.add_argument("-ep", "--edit_path", action="store_true", dest="edit_path",
                        help="Enable path editing mode.")
    # parser.add_argument("-l", "--list", action="store_true",
    #                     help="Log the list of file which rename successfully.")
    parser.add_argument("-b", "--bat", "--batch", action="store_true", dest="bat",
                        help="Make a simple batch file in this script dir. "
                             "It can let you easy to work with windows, "
                             "by drag and drop the files into the batch file icon.")
    parser.add_argument("-v", "--ver", "--version", action="store_true", dest="ver",
                        help="Show the version message of this script.")
    args = parser.parse_args(argv)

    if args.ver:
        print_version()
        exit(0)

    if args.bat:
        arg_flags = []
        if args.edit_path:
            arg_flags.append("ep")
        # if args.yes:
        #     arg_flags.append("y")
        make_bat(arg_flags)
        exit(0)

    if len(args.path) == 1:  # sys.argv[0] must be the path of this script.
        parser.print_help()
        exit(0)

    return parser, args


def make_bat(arg_flags):
    flags_name = ""
    flags_str = ""
    for arg_flag in arg_flags:
        flags_name = flags_name + "_" + arg_flag
        flags_str = flags_str + " -" + arg_flag

    bat_path = os.path.join(FILE_PATH, FILE_NAME + flags_name + ".bat")
    print("Batch file: {0}".format(bat_path))

    content = "@echo off\npy {0} %*{1}\npause\n".format(os.path.abspath(__file__), flags_str)
    try:
        bat = open(bat_path, "w")
        bat.write(content)
        bat.close()
    except IOError:
        print("[ERROR] Cannot write batch file.\n")
        return
    print(content)

    print("Done.\n")


def print_version(file=sys.stdout):
    print("\n{name} {ver}\n".format(name=PROJ_NAME, ver=__version__) +
          "{description}\n".format(description=DESCRIPTION) +
          "Present by {author}.\n".format(author=__author__), file=file)


def yes(string):
    yes_list = "y", "yes", "true", "t"
    if string.lower() in yes_list:
        return True
    else:
        return False


if __name__ == '__main__':
    main(sys.argv)
