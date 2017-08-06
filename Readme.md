# Rename via TXT

Rename files or dirs via your text editor.

批量重命名檔案，通過你的文字編輯器。


## Operating environment

Python 3.x

Windows


## How to use

- Install - 安裝
  
  1. Download `RenameViaTxt.py`.
  
     下載 `RenameViaTxt.py`。
     
  1. Enter the cmd - 輸入指令

     ```shell
     py RenameViaTxt.py -b 
     ```

     And:

     還有：

     ```shell
     py RenameViaTxt.py -b -ep
     ```

     Then you will see `RenameViaTxt.bat` and `RenameViaTxt_ep.bat`.

     之後你會看到 `RenameViaTxt.bat` 和 `RenameViaTxt_ep.bat` 兩個文件。

- Usage - 使用

  1. drag and drop files which you want to renamed into `RenameViaTxt.bat` or `RenameViaTxt_ep.bat`.
  
     拖放你想要重命名的檔案到 `RenameViaTxt.bat` 或 `RenameViaTxt_ep.bat`。
     
  1. This script will generate a json file `./RENAME.json` on the operation path.
  
     腳本會生成一個 json 檔案 `./RENAME.json` 在你的工作目錄。
     
  1. Edit, and save the file `./RENAME.json`, then hit `ENTER` key.
  
     編輯，之後保存 `./RENAME.json` 檔案，然後按 `ENTER`。
     
  1. Files will be renamed automatically.
  
     檔案會被自動重命名。

## Help

```
usage: RenameViaTxt.py [-h] [-ep] [-b] [-v] PATH [PATH ...]

Rename files or dirs via your text editor.
批量重命名文件，通過你的文字編輯器。

positional arguments:
  PATH                  Path of files witch need to be renamed.
                        需要被重命名的檔案全路徑。

optional arguments:
  -h, --help            show this help message and exit
                        顯示幫助信息。
  -ep, --edit_path      Enable path editing mode.
                        打開路徑編輯模式。
  -b, --bat, --batch    Make a simple batch file in this script dir. It can
                        let you easy to work with windows, by drag and drop
                        the files into the batch file icon.
                        在該腳本的同一目錄下生成一個批處理文件，使得你可以容易的
                        在 Windows 的環境下操作，只需要拖動需要被解碼的檔案到這
                        個批處理文件上即可。
  -v, --ver, --version  Show the version message of this script.
                        顯示腳本的版本訊息。

Present by undecV.
```
