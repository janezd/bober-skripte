import os
import re
import shutil
import time
from unicodedata import normalize

re_src = re.compile(r'src="(resources/[^"]+)"')
re_resource_img = r'{"type": "image", "url": "resources/([^"]+)"}'

year = time.gmtime().tm_year % 100
if time.gmtime().tm_mon < 7:
    year -= 1

def try_remove(path):
    try:
        os.remove(path)
    except:
        pass


def try_mkdir(path):
    try:
        os.mkdir(path)
    except:
        pass


def try_link(what, where):
    try:
        os.symlink(what, where)
    except:
        pass


def copy(name, src, dst):
    src, dst = os.path.join(src, name), os.path.join(dst, name)
    if os.path.isdir(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)
    else:
        shutil.copy(src, dst)
        
DEST_DIR = "/Users/janez/Downloads/bober-naloge/solsko2022"
try_mkdir(DEST_DIR)
os.chdir("../solsko2022")
true, false = True, False
ids = {}
for dir in os.listdir("."):
    dest_dir = os.path.join(DEST_DIR, dir)
    index_file = os.path.join(dir, "index.html")
    if not os.path.exists(index_file):
        continue
    try_mkdir(dest_dir)
    index = open(index_file).read()
    index = index.replace("../task.css", "/static/css/task.css")
    open(os.path.join(dest_dir, "index.html"), "wt").write(index)
    copy("Manifest.json", dir, dest_dir)
    copy("resources", dir, dest_dir)

    manifest = eval(open(os.path.join(dir, "Manifest.json")).read())
    ids[manifest["id"]] = dir


missing = set()
linkscript = open(os.path.join(DEST_DIR, "link_tasks"), "wt")
linkscript.write("rm -rf skupine\n")
linkscript.write("mkdir skupine\n")
for line in open("groups.txt"):
    if not line.strip():
        continue
    name, tasks = line.split(maxsplit=1)
    name = name.strip()
    tasks = [f"{year}{int(tid):03}" for tid in tasks.split(",")]
    group_dir = f"__group-{name}/"
#    try_mkdir(group_dir)
    linkscript.write(f"mkdir skupine/{name}\n")
    for task in tasks:
        if task not in ids:
            missing.add(task)
            continue
        task = ids[task]
        task = normalize("NFC", task)
        linkscript.write('ln -s "../../{}" "skupine/{}/{}"\n'.format(task, name, task))
        #try_link("../" + task, group_dir + task)


if missing:
    print("Manjkajoči prevodi:" + ", ".join(map(str, missing)))
