import os
import re
import shutil
from unicodedata import normalize

re_src = re.compile(r'src="(resources/[^"]+)"')
re_resource_img = r'{"type": "image", "url": "resources/([^"]+)"}'

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
    [shutil.copy, shutil.copytree][os.path.isdir(src)](src, dst)

os.chdir("../drzavno2018")
true, false = True, False
ids = {}
for naloga in os.listdir("."):
    dir = naloga + "/"
    try_remove(dir + ".DS_Store")
    try_remove(dir + "resources/.DS_Store")
    if os.path.exists(dir + "task.html"):
        contents = open(dir +"index.html", encoding="utf-8").read()
        manifest = eval(open(dir + "Manifest.json", encoding="utf-8").read())
        if normalize("NFC", manifest["title"]) != normalize("NFC", naloga):
            print("Ime naloge ni enako direktoriju ({} != {}); "
                  "upoštevam direktorij".format(manifest["title"], naloga))
        resources = {mo.group(1) for mo in re_src.finditer(contents)}

        manifest["task"] = [x for x in manifest["task"]
                            if x["url"] not in resources]
        unfixed = [x["url"] for x in manifest["task"] if x["type"] == "image"
                   and x["url"].endswith(".png")]
        if unfixed:
            print("Nevključene slike v manifestu {}: {}".
                  format(naloga, ", ".join(unfixed)))

        unfixed_res = [x for x in os.listdir(dir + "resources")
                   if "resources/" + x not in resources]
        rep_unfixed_res = [x for x in unfixed_res if x.endswith(".png")]
        if rep_unfixed_res:
            print("Nevključene slike v poddirektoriju {}/resources: {}".
                  format(dir, ", ".join(rep_unfixed_res)))
        ids[manifest["id"]] = naloga

missing = set()
linkscript = open("link_tasks", "wt")
linkscript.write("rm -rf skupine\n")
linkscript.write("mkdir skupine\n")
for line in open("groups.txt"):
    if not line.strip():
        continue
    name, tasks = line.split()
    name = name.strip()
    tasks = ["18{:03}".format(int(tid)) for tid in tasks.split(",")]
    group_dir = "__group-{}/".format(name)
#    try_mkdir(group_dir)
    linkscript.write("mkdir skupine/{}\n".format(name))
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
