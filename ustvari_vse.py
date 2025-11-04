import time
import os
import csv

def preberi_csv(ime_datoteke):
    datoteka = open(ime_datoteke, 'r', newline='', encoding='utf8')
    bralnik = csv.reader(datoteka, delimiter='\t')
    seznam = []
    for vrstica in bralnik:
        seznam.append(vrstica)
    datoteka.close()
    return seznam[1:]

def try_mkdir(s):
    try:
        os.mkdir(s)
    except FileExistsError:
        pass

def sestavi_nalogo(podatki):
    year = time.gmtime().tm_year % 100
    if time.gmtime().tm_mon < 7:
        year -= 1
    if 3 <= time.gmtime().tm_mon <= 11:
        path = f"../solsko20{year}"
    else:
        path = f"../drzavno20{year}"

    title = podatki[1]
    taskid = int(podatki[0])
    country = podatki[2].upper()
    direction = podatki[3]
    no_answers = int(podatki[4])
    correct = ord(podatki[5].strip()) - 96

    answer_template = open("answer.html.tpl").read()
    four_answers = [answer_template.format(year=year, taskid=taskid, ansnr=i) for i in range(1, no_answers + 1)]
    if direction == "n":
        answers = "\n" + "\n".join(four_answers)
    elif direction == "v":
        answers = "    <center><table>\n        <tr>\n" \
                  "        <td>\n" + \
                  "        </td>\n        <td>\n".join(four_answers) + \
                  "        </td>\n" \
                  "        </tr>\n        </table></center>\n"
    else:
        first_part = no_answers//2
        answers = "    <center><table>\n        <tr>\n" \
                  "        <td>\n" + \
                  "        </td>\n        <td>\n".join(four_answers[:first_part]) + \
                  "        </td>\n        </tr><tr>\n        <td>\n" + \
                  "        </td>\n        <td>\n".join(four_answers[first_part:]) + \
                  "        </td>\n" \
                  "        </tr>\n        </table></center>\n"

    outdir = os.path.join(path, title)
    try_mkdir(outdir)
    try_mkdir(os.path.join(outdir, "resources"))
    for name in ("index.html", "Manifest.json"):
        contents = open(name + ".tpl", encoding="utf-8").read().format_map(vars())
        open(os.path.join(outdir, name), "wt", encoding="utf-8").write(contents)
    
    print(f"Naloga {title} je uspešno kreirana.")



### 

NALOGE = "../naloge.csv" # ime datoteke s podatki o nalogah, ločilo je TAB
vse_naloge = preberi_csv(NALOGE)
for naloga in vse_naloge:
    sestavi_nalogo(naloga)
