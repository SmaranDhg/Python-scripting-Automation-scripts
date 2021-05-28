#! /usr/bin/python3

# %%
import os
import sys
from os import system
import argparse
import shutil
import re
from sys import argv

try:
    import retrieve
except Exception as e:
    system("python -m pip install retrieve")
    import retrieve

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-f", "--file", nargs="?", default="", help="Name of file to run")
group.add_argument("-s", "--setup", nargs="?", default=1, help="During start and reset")
parser.add_argument("--files", nargs="+", default="", help="Name of files to run")
parser.add_argument(
    "-rs",
    "--reset",
    default=1,
    nargs="?",
    help="If something went wrong and you want to reinstall setup!",
)
parser.add_argument(
    "-up",
    "--update",
    default=1,
    nargs="?",
    help="Updates existing commands and adds newones if available",
)
parser.add_argument(
    "-c",
    "--command",
    default="",
    nargs="*",
    help="Ex  cpp:\n[g++ -std=17 #cpp# -o out && ./out #args# && rm out] python:[python #py# #args#]",
)
parser.add_argument(
    "-a",
    "--args",
    default="",
    nargs="*",
    help="arguments for the programs",
)

_command = ""
_cargs = ""

argv = " ".join(argv[1:]).replace("--command", "-c").replace("--args", "-a").split(" ")
print(argv)
if "-c" in argv:
    _command = " ".join(argv[argv.index("-c") + 1 :])
    argv = []
elif "-a" in argv:
    _cargs = " ".join(argv[argv.index("-a") + 1 :])
    argv = argv[: argv.index("-a")]

_args = parser.parse_args(argv)
_fname = _args.file
_reset = not _args.reset
_setup = not _args.setup
_update = not _args.update
if _args.files:
    print(_args.files)
    _fname = " ".join(_args.files)


_commandpathgt = "https://raw.githubusercontent.com/SmaranDhg/Python-scripting-Automation-scripts/master/_generic_code_runner/commands"

_arguments = "$2 $3 $4 $5 $6 $7 $8 $9"
_cp = "cp"
_com = ""
_commandpath = ""
_clear = "clear"
_ptfrm = "g"  # general platform


class CommandNotFound(ValueError):
    pass


class IncorrectFileName(ValueError):
    pass


class InvalidCommandFormat(ValueError):
    pass


def __reset():
    if os.path.exists(_commandpath):
        shutil.rmtree(_commandpath)


# sets new command to the a file type
def _setcommand():
    global _command, _ptfrm
    print(_command)
    try:
        print(_command)
        _command = _command.replace("#args#", ";")
        ftype = _command.split("#")[1]
        _command = re.sub(r"#[a-zA-Z]+#", "`", _command)
    except:
        raise InvalidCommandFormat(
            "\nInvalid command format!!\nplease enter commands in following format.\n\n#cpp#------->Place where file name will be placed\n#args#------->Place where arguments for file will be placed(optional).\n\n cpp: [g++ -std=17 #cpp# -o out && ./out #args# && rm out]\n python: [python #py# #args#]"
        )
    ret = ""
    exists = 0

    with open(f"{_commandpath}commands") as f:
        for lin in f:
            if len(lin.strip()):
                ptfrm, command = lin.split(" ", 1)

                file, command = command.split(" ", 1)
                if file == ftype:
                    ret += f"{_ptfrm} {file} {_command}\n"
                    exists = 1
                ret += f"{ptfrm} {file} {command}\n"
    if not exists:
        ret += f"{_ptfrm} {ftype} {_command}\n"
    with open(f"{_commandpath}commands", "w") as f:
        f.write(ret)

    raise ValueError(f"Finished setting command to file type [{ftype}  {_command}]")


def __update():
    dest = f"{_commandpath}commands"
    if os.path.exists(dest):
        os.remove(dest)
    retrieve.retrieve.download(_commandpathgt, dest)
    print("Update Complete!!")


def _fetch_essential():
    global _arguments, _cp, _com, _commandpath, _clear, _ptfrm
    if sys.platform.startswith("win"):
        _arguments = _arguments.replace("$", "%")
        _commandpath = f"{os.environ['HOMEPATH']}\\run\\"
        _cp = "copy"
        _com = ".bat"
        _clear = "cls"
        _ptfrm = "w"
        if _setup:
            print("Preparing for windows")
            print(f"Environment to path;c:\\{_commandpath[1:]}")
            system(f'setx /m path "%PATH%;c:\\{_commandpath[1:]}"')
    else:
        _arguments += " ${10} ${11} ${12} ${13} ${14} ${15} ${16}"
        _commandpath = f"{os.environ['HOME']}/run/"
        _ptfrm = "l"
        if _setup:
            print("Preparing for linux")
            system(f"echo PATH=$PATH:{_commandpath}>>~/.bashrc")


"""---------------------------Installtion---------------------------"""


def _fetch_file_to_dir():
    global _arguments, _cp, _com, _commandpath

    if not os.path.exists(_commandpath):
        os.mkdir(_commandpath)
        retrieve.retrieve.download(_commandpathgt, f"{_commandpath}commands")
        with open(f"{_commandpath}run{_com}", "w") as f:
            if _com == "":
                f.write(
                    f"""

function op()
{{
if [ $1 == -c ]; then
   python3 {_commandpath}run.py -c {_arguments}
elif [ $1 == --files ]; then
    python3 {_commandpath}run.py --files  {_arguments}
elif [ $2 ==  ]; then
    python3 {_commandpath}run.py   -f $1
else 
   python3 {_commandpath}run.py -f $1 -a {_arguments}
fi

}}
op $1 {_arguments}
              
                """
                )
                system(f"chmod +x {_commandpath}run")
            else:
                _commandpath = _commandpath.replace("/", "\\")
                f.write(
                    f"""
                \n@echo off
                \nif "%1" == "-c" (
                \npython {_commandpath}run.py -c {_arguments}
                \n) else if "%1" == "--files" (
                    python {_commandpath}run.py --files %1 {_arguments}
                \n)
                \nelse (
                       \nif "%2" == "" (
                           \npython {_commandpath}run.py -f %1
                       \n)\nelse (
                \npython {_commandpath}run.py -f %1 -a {_arguments}\n)

                \n)
                """
                )

        print(f"copying file to {_commandpath}")
        system(f"{_cp} run.py {_commandpath}")

    _commandpath = f"{_commandpath}/commands"

    if _setup:
        print("Installation Complete!!")


# %%


"""---------------------------Prepare the command---------------------------"""


def __gtcommand(ext, compath):
    ret = ""
    with open(compath, "r") as f:
        for comm in f:
            comm = comm.strip()
            if len(comm):
                ptfrm, comm = comm.split(" ", 1)
                key, value = comm.split(" ", 1)
                if ext == key:  # checking the extension if its okay or not
                    if ptfrm == _ptfrm:
                        return value.strip()
                    elif ptfrm == "g":
                        ret = value.strip()

    if not ret == "":
        return ret
    raise CommandNotFound(f"Command not found for file type '{ext}'!!")


"""---------------------------Get path of file---------------------------"""


def __command():
    if not "." in _command:
        return __gtcommand(_command.lower(), _commandpath)

    ext = _fname.rsplit(".", 1)[1]
    return __gtcommand(ext, _commandpath)


def __gt_files(foldername="."):
    ret = []
    for root, folders, files in os.walk(foldername):
        if _fname in files:
            ret.append((root, _fname.split(" ", 1)[0]))
    return ret


"""________________Handle if multiple file exist in same Hierarchy_______________"""


def __manage_dups(files):
    cntr = 1
    print(f"Choose which one to run!!\n")

    for folder, file in files:
        print(f"[ {cntr} ] {folder}/{file}")
        cntr = cntr + 1

    print("q(quit)")
    value = input()
    if value == "q":
        raise ValueError("Halted!!")

    value = int(value) - 1
    if abs(value) < len(files):
        return "{}/{}".format(*files[value])
    else:
        system(_clear)
        print("Not an option!!")
        return __manage_dups(files)


def __run():
    files = __gt_files()
    if len(files) == 0:
        raise IncorrectFileName(
            f"{_fname} No such file exist in directory tree, please check file name again!!"
        )
    fpath = "{}/{}".format(*files[0])
    if len(files) > 1:
        fpath = __manage_dups(files)
    system(f"{__command().replace('`',fpath).replace(';',_cargs)}")


def __runfiles():
    system(f"{__command().replace('`',_fname).replace(';',_cargs)}")
    raise ValueError()


if __name__ == "__main__":
    try:
        _fetch_essential()
        if _command != "":
            _setcommand()
        if _reset:
            __reset()
        if _update:
            __update()
        else:
            _fetch_file_to_dir()
            if _args.files:
                __runfiles()
            if not _setup:
                __run()
    except ValueError as e:
        print(e)
