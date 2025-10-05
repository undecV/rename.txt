import os
import json
import colorama
from colorama import Fore

from common.json_yaml_style import JSON_STYLE
from common.yes import yes

colorama.init(autoreset=True)

def colored(color: str, s: str):
    return color + s + Fore.RESET

WARNING = colored(Fore.YELLOW, 'WARNING')
ERROR = colored(Fore.RED, 'ERROR')

RENAME_FILE = 'rename.json'
TEXT_EDITOR_PATH = 'C:\\Program Files\\Microsoft VS Code\\code.exe'
TEXT_EDITOR_ARGS = '{RENAME_FILE}'.format(**locals())


def main(argv):
    # filter invalid argv
    args = []
    for c, arg in enumerate(argv[1:]):
        if not os.path.exists(arg):
            print('[{}] argv[{:0d}]: {} not exists.'.format(WARNING, c+1, arg))
            continue
        if os.path.exists(RENAME_FILE) and os.path.samefile(arg, RENAME_FILE):
            print('[{}] argv[{:0d}]: {} is the same as "RENAME_FILE".'.format(WARNING, c+1, arg))
            continue
        args.append(os.path.abspath(arg))
    if len(args) == 0:
        print('No any valid value.')
        exit()

    # Generate rename file
    edit = [os.path.basename(arg) for arg in args]
    body = json.dumps([os.path.basename(arg) for arg in args], **JSON_STYLE)
    if os.path.exists(RENAME_FILE):
        print('[{}] "rename_file" already exists.'.format(WARNING))
    with open(RENAME_FILE, 'w', encoding='utf-8') as fp:
        fp.write(body)

    # Open editor
    cmd = 'start "{0}" {1}'.format(TEXT_EDITOR_PATH, TEXT_EDITOR_ARGS)
    print(cmd)
    os.system(cmd)

    # Wait for user edit
    print('Edit, save and close the file.')
    print('Then back to this script window and')
    input('press <ENTER> key to continue...')

    # Read editor
    with open(RENAME_FILE, 'r', encoding='utf-8') as fp:
        try: 
            edited = json.load(fp)
        except:
            print('[{}] JSON parse failed.'.format(ERROR))
            exit()

    if len(edited) != len(args):
        print('[{}] Data format invalid.'.format(ERROR))
        exit()

    # List and filter changes
    changed = []
    for c in range(len(args)):
        print('{:8d}: '.format(c), end='')
        if edit[c] == edited[c]:
            print(colored(Fore.GREEN, 'not changed.'))
        else:
            changed.append(c)
            print('{}\n{}{}'.format(colored(Fore.RED, edit[c]),
                '->'.center(10), colored(Fore.RED, edited[c])))
    
    # Exit when not any changed
    if len(changed) == 0:
        print(colored(Fore.GREEN, 'not changed.'))
        exit()

    # Confirm
    inp = input('Please confirm the changes (yes): ')
    if not yes(inp):
        print(colored(Fore.RED, 'BREAK'))
        exit()

    # Rename
    for c in changed:
        print('{:8d}: '.format(c), end='')
        new_name = os.path.join(os.path.dirname(args[c]), edited[c])
        if os.path.exists(new_name):
            print('[{}] "new_name" already exists.'.format(ERROR))
            continue
        try:
            os.rename(args[c], new_name)
        except Exception:
            print('[{}] Rename failed.'.format(ERROR))
            continue
        print(colored(Fore.GREEN, 'OK.'))

    # Remove rename file
    try:
        os.remove(RENAME_FILE)
    except IOError:
        print('[{}] Remove "RENAME_FILE" failed.'.format(ERROR))

    print(colored(Fore.GREEN, 'Done.'))


if __name__ == "__main__":
    import sys
    main(sys.argv)
