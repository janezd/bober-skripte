import time
import os


def try_mkdir(s):
    try:
        os.mkdir(s)
    except FileExistsError:
        pass

year = time.gmtime().tm_year % 100
if time.gmtime().tm_mon < 7:
    year -= 1
if 3 <= time.gmtime().tm_mon <=11:
    path = f"../solsko20{year}"
else:
    path = f"../drzavno20{year}"


title = input("Naslov naloge: ")
taskid = int(input("Id naloge: "))
country = input("Država: ").upper()
direction = input("Smer odgovorov [v/n/2]: ")
correct = ord(input("Pravilni odgovor [a/b/c/d/...]: ").strip()) - 96


answer_template = open("answer.html.tpl").read()
four_answers = [answer_template.format(year=year, taskid=taskid, ansnr=i) for i in range(1, 10)]
if direction == "n":
    answers = "\n".join(four_answers)
elif direction == "v":
    answers = "        <center><table><tr>\n" \
              "        <td>\n" + \
              "        </td>\n        <td>\n".join(four_answers) + \
              "        </td>\n" \
              "        </tr></table></center>\n"
else:
    answers = "        <center><table><tr>\n" \
              "        <td>\n" + \
              "\n      </td>\n        <td>\n".join(four_answers[:2]) + \
              "          </td></tr><tr><td>\n" + \
              "\n      </td>\n        <td>\n".join(four_answers[2:4]) + \
              "          </td>\n" \
              "        </tr></table></center>\n"

outdir = os.path.join(path, title)
try_mkdir(outdir)
try_mkdir(os.path.join(outdir, "resources"))
for name in ("index.html", "Manifest.json"):
    contents = open(name + ".tpl", encoding="utf-8").read().format_map(vars())
    open(os.path.join(outdir, name), "wt", encoding="utf-8").write(contents)
