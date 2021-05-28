# %%

import os
import argparse as parse
from pprint import pprint as pp

import tkinter as tk
import json

root = tk.Tk()
root.withdraw()


parser = parse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    "-p",
    "--prefix",
    help="Prefix of snippet",
)
parser.add_argument(
    "-d",
    "--delete",
    nargs="?",
    default=1,
    help="Flag to delete the prefix from snippets",
)
parser.add_argument(
    "-l",
    "--language",
    default="p",
    help="Which language to choose",
)
group.add_argument(
    "-al",
    "--available-language",
    nargs="?",
    default=1,
    help="View all the available langauge in snippets",
)
group.add_argument(
    "-fc", "--from-clipboard", nargs="?", default=1, help="Parse options from clipboard"
)

args = parser.parse_args()
pre_ = "t"
d_ = 1
afile_ = 1
fname_ = 1
options_ = {"d": d_, "p": pre_, "al": afile_, "l": fname_}
cu_ = args.from_clipboard
base_ = "/home/smaran/.config/Code/User/snippets/"


def parse_data():
    global options_, pre_, d_, fname_, fname_, afile_
    # print(options_)
    data = "0"
    if cu_ is None:
        data = parse_cu()
    else:
        options_ = {
            "p": args.prefix,
            "d": args.delete,
            "al": args.available_language,
            "l": args.language,
        }

    pre_ = options_["p"]
    d_ = options_["d"]
    afile_ = options_["al"]
    fname_ = options_["l"]
    # print(options_)
    return data


def parse_cu():
    global options_

    ofd = root.clipboard_get()

    of, data = ofd.split("_", 1)
    data = data[:-1].strip()
    # print(data)

    o, *flags = of.strip().rsplit("::")

    o = o.split(":")
    os, vals = o[::2], o[1::2]

    for o, val in zip(os, vals):
        options_[o] = val
    for flag in flags:
        options_[flag] = None
    print(options_)
    return data


def gt_fnm():
    fname = "python.json"
    ret = f"{gt_nm(fname_, 1)}.json"
    ret = ret if not ret == "None.json" else fname
    return ret


"""________________adding files and there shortcuts_______________"""


def parse_fms(files):
    return {file.rsplit(".", 1)[0]: file[:2] for file in files}


"""________________Processing file name_______________"""


def gt_nm(fname, wp_flg=0):  # with prefix flag
    nm = {
        "python": "p",
        "cpp": "cpp",
        "java": "j",
        "ruby": "rb",
        "lisp": "ls",
        "javascript": "js",
        "markdown": "md",
    }
    nm.update(parse_fms(show_file(1)))
    if wp_flg:
        if fname in nm.values():
            return list(nm.keys())[list(nm.values()).index(fname)]
        else:
            return None
    ret = ""
    if fname in nm.keys():
        ret = nm[fname.lower()]
    else:
        ret = fname[:2]
    return ret


def show_file(ret_files=0):
    files = []
    for entry in os.scandir(base_):
        if entry.is_file():
            files.append(entry.name)

    if ret_files:
        return files

    print(f'Available langauge and there flags are:\n{"":=<50}')
    for file in files:
        fname = file.rsplit(".", 1)[0]
        print(f"{fname:-<50}{gt_nm(fname)}")
    print(f'{"":=<50}')


def update(data="0"):
    file = f"/home/smaran/.config/Code/User/snippets/{gt_fnm()}"

    if data == "0":
        data = root.clipboard_get().strip()

    data = eval(
        f""" {{\r\n\"prefix\": \"{pre_}\",\r\n\"body\":\'\'\'{data}\'\'\',\r\n\"description\": \"Go nuts\"\r\n}} """
    )

    a = dict()
    with open(file, "r") as f:

        # print(a, pre_, data, d_)
        a = json.load(f)
        a[pre_] = data
        if d_ is None:
            del a[pre_]

    with open(file, "w") as f:
        print(f"updating file:{file}")
        json.dump(a, f)

    print("Success!!")


def main():
    data = parse_data()
    # print(data)
    if afile_ is None:
        show_file()
    else:
        update(data)


if __name__ == "__main__":
    main()
