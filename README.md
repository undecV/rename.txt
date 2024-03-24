# rename.txt: a text-based renamer

English | [正體中文](./README.zh-TW.md)

`rename.txt` Lets you change the file name using your favorite text editor.

> :warning: This is a pre-release version and has not been thoroughly tested.
> Please do not use it in a production environment, and be sure to back it up.

## Glances

![A screenshot of rename.txt](./doc/screenshot_1.png)

## Features

- Use your favorite text editor to batch modify file\folder names;
- Support variables through template engine [jinja2];
- Support more variables through add-ons;
- Preview and revise multiple times.
- A useless log file, useful if anything goes wrong.

[jinja2]: https://palletsprojects.com/p/jinja/

## Usage

Usage: renametxt.py [OPTIONS] [PATH]...

Options:

- `--debug`: Debug mode, print more messages.
- `-d, --dryrun`: Dryrun: test or validate code without executing the actual functionality. [default: True]
- `-o, --output FILE`: The output path of the recover log file. [default:./YYYYMMDDTHHMMSS.rename.json]
- `-h, --help`: Show this message and exit.

A tip for Windows users: drag the file to the `renametxt.bat` icon to quickly use the command.

### Steps

- Import the files and folders that need to be renamed as arguments.
  Please note that the order of the files as arguments will be used as the index number (`index`, starting from 0);
- The program will generate a temporary file, which we call **entries file**, and open it with the default text editor;
- Edit the entries file and save it; then return to the program and press any key to continue and preview the edited results.
  Note that the order of the entries will be followed by the sequence number (`sequence`, starting from 0);
- Check the edited results and choose to re-edit or start renaming.
- The program generates a recovery record and starts renaming.

### Entries file

The entries file is a JSON file, which is a list. Each entry contains an `index` number and file name. It looks like this:

```json
[
  [0, "foo.txt"],
  [1, "bar.jpg"]
]
```

Tip: Modern editors have multi-line editing functionality.

Tip: Swapping file names can be achieved by modifying the `index` number.

### Variables

Variables can be used through templates when modifying names.
Variables are generated based on each item and their metadata.

The following are some default variables:

- `self`: `pathlib.Path`, the path of the item.
- `index`: Integer, the order of the item in the parameters.
- `sequence`: Integer, the order of the item in the `entries file`.
- `size`: Integer, file size, in bytes. For folder is `0`.
- `atime`, `mtime`, `ctime`: `datetime.datetime`, Item access, modification, and creation time.
- `naturalsize.size`: `str`, from an example add-on, readable file size, for example, `8.7 KiB`.

The use of variables is based on the template engine [jinja2],
which allows us to do some simple operations and formatting when using variables.

```json
[
  [0, "DSC_{{ mtime.strftime('%Y%m%dT%H%M%S') }}_{{ '%04d' % (index+1) }}.JPG"],
  [1, "DSC_{{ mtime.strftime('%Y%m%dT%H%M%S') }}_{{ '%04d' % (index+1) }}.JPG"]
]
```

The rendered file name will be:

```log
0000 | DSC_0094.JPG
  -> | DSC_20210315T000649_0001.JPG
0001 | DSC_0087.JPG
  -> | DSC_20220320T103149_0002.JPG
```

## Miscellaneous

### Why two-step renaming?

This is a greedy method to avoid collisions when swapping two file names.

```c
c=a; a=b; b=c;
```

Temporary file names use UUID to avoid collisions.
