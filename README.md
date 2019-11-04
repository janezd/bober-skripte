## Skripte za sestavljanje in pakiranje naloga za tekmovanje Bober

**Disclaimer**: te skripte sem na hitro napisal, ko sem jih potreboval. Določene grozne stvari (npr. inline css v vsaki nalogi) tudi niso moja ideja, temveč so podedovane iz predprejšnjega tekmovalnega sistema. Znal bi narediti tudi lepše. :)

**Pomembno**: V skriptah hardcodan direktorij. V `ustvari.py`, `sestavi.py` in `pakiraj.py` je direktorij `../solsko2018` oz. `../drzavno2018` (oz. druga letnica). To je očitno potrebno spremeniti pred vsakim tekmovanjem.

### Ustvarjanje naloge

Novo nalogo sestavimo tako, da poženemo `ustvari.py`.

```
Naslov naloge: Bober preskuša kilave skripte
Id naloge: 123
Država: si
Smer odgovorov [v/n/2]: v
Pravilni odgovor [a/b/c/d/...]: e
```

- Id je poljubna, največ trimestna številka. K temu se bo pripela letnica. V praksi je to kar zaporedna številka naloge v tabeli izbranih nalog.

- Država je dvočrkovna koda; na podlagi tega s k nalogi v sistemu pripne gif.

- Smer odgovorov določi obliko tabele z odgovori - lahko so postavljeni vodoravno ali navpično ali 2x2. Vodoravnih ali navpičnih odgovorov je 10, vendar jih lahko ročno brišemo ali dodajamo.

Skripta bo znotraj `solsko2018` (oz. ustrezno popravljenega imena) direktorija naredila poddirektorij, katerega ime je ime naloge. V njem bodo 

- Manifest.json, iz katerega sistem ob uvozu razbere podatke o nalogi
- poddirektorij resources, kamor damo slike, ki sodijo k nalogi
- task.html, v katerega vpišemo besedilo naloge.

### Vpisovanje besedila naloge

Nič posebnega, samo urejaš `task.html`. Edina finta: če hočeš uporabljati `{` in `}` moraš pisati `{{` in `}}`. Opravičujem se, ker sem len.

**Pomembno:** vse slike je potrebno dati v poddirektorij resources in tam morajo biti že, ko poženeš naslednjo skripto, `sestavi.py`.

### "Sestavljanje" naloge

Nato je potrebno poklicati `sestavi.py`. Ta vzame `task.html` in vanje vstavi `head.html` ter to shrani kot `index.html`. To je zdaj končna naloga.

`index.html` pogledamo v brskalniku, popravimo napake **tako da spreminjamo `task.html` in ponovno poženemo `sestavi.py`. In ta proces ponavljamo.

`sestavi.py` tudi doda slike v `Manifest.json`, vendar to stori samo prvič. Zato je pomembno, da so slike v `resources` že pred prvim poganjanjem `sestavi`.

**Opazka:** `sestavi.py` doda k `task.html` samo nek javascript iz predprejšnjega tekmovalnega sistema, ki ga Polž najbrž odstrani. Poleg tega vsebuje CSS, ki bi lahko bil v ločeni datoteki. Prav tako mislim, da Polž ignorira navedbe slik v `Manifest.json`, temveč sam pogleda, kaj je v `resources`. Torej je zelo možno, da bi se bilo skripte `sestavi.py` zelo preprosto znebiti.

### Pakiranje naloge

Da pripravimo naloge za uvoz v sistem, je potrebno pognati `pakiraj.py`. Ta pričakuje, da bo v `solsko2018` (oz. ustreznem direktoriju) datoteka `groups.txt` v takšni obliki:

```
solsko-2018-razred_6_7  13,14,15,16,17,18,23,24,25,26,27,28,29,30,31
solsko-2018-razred_8_9  13,14,15,23,24,25,26,27,28,29,30,32,33,34,35,36
solsko-2018-srednja     23,24,25,26,27,32,33,34,35,36,37,38,39,40,41,42,43
```

Za vejicami ni presledkov, ker

```
    name, tasks = line.split()
    tasks = tasks.split(",")
```

Ne pravim, da ne bi bilo lepše drugače.

`pakiraj.py` naredi malo preverjanja, potem pa pripravi bash skripto`link_tasks`, ki se požene ob hooku v uvozu v sistem.


### Uvoz v sistem

Kloniram git imenik

git clone ssh://bober.acm.si/home/j/bober-naloge.git

, notri dodam naloge in naredim push. Ob pushu se pozene hook, ki naredi sledece.

```
cd /home/j/bober-naloge
git pull

for competition in $(ls -d */); do
    cd $competition;
    sh link_tasks;
    bash -c '\
        ls skupine;\
        for skupina in skupine/* ; do\
            echo $skupina;\
    done'
    cd ..
done
/usr/bin/docker exec -it production_web_1 /home/bober/bober/import_tasks.sh
```

Torej je potrebno v imeniku /home/j/bober-naloge nastaviti pravi branch. Trenutno je nastavljen na '2018-drzavno', kar je verjetno narobe.
