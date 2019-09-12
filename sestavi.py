import os, zipfile
import re

re_country = re.compile(r'"country": "(..)",')

head = open("head.html", encoding="utf-8").read()

base = "../drzavno2018/"
for naloga in os.listdir(base):
    dir = base + naloga + "/"
    if os.path.exists(dir + "task.html"):
        contents = open(dir +"task.html", encoding="utf-8").read().format(head)
        manifest = open(dir + "Manifest.json", encoding="utf-8").read()
        open(dir + "index.html", "wt", encoding="utf-8").write(contents)
#        zip = zipfile.ZipFile("../pakirano/" + naloga + ".zip", "w")

        all_resources = ''.join(
            ',\n        {{"type": "image", "url": "resources/{}"}}'.format(fname)
            for fname in os.listdir(dir + "resources") if fname[0] != ".")
        manifest = manifest.replace(
            ',\n        {"type": "image", "url": "resources/FIX_ME"}',
            all_resources)
        open(dir + "Manifest.json", "wt", encoding="utf-8").write(manifest)

#        for name in ("index.html", "Manifest.json", "solution.html"):
#            zip.write(dir + name, name)
#        for name in os.listdir(dir + "resources"):
#            zip.write(dir + "resources/" + name, "resources/" + name)
